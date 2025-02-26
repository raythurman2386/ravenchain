from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from api.auth.utils import (
    get_db,
    get_password_hash,
    verify_password,
    authenticate_user,
    create_access_token,
    create_refresh_token,
    get_current_active_user,
    get_admin_user,
    SECRET_KEY,
    ALGORITHM,
)
from api.auth.schemas import UserCreate, UserResponse, UserUpdate, Token, RefreshToken, UserDB
from api.database.models import User
from api.dependencies import logger, limiter
from typing import List

authRouter = APIRouter()


@authRouter.post("/auth/register", response_model=UserResponse)
@limiter.limit("5/minute")
async def register_user(request: Request, user_data: UserCreate, db: Session = Depends(get_db)):
    """Register a new user"""
    # Check if username already exists
    existing_user = db.query(User).filter(User.username == user_data.username).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Username already registered"
        )

    # Check if email already exists
    existing_email = db.query(User).filter(User.email == user_data.email).first()
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered"
        )

    # Create new user
    hashed_password = get_password_hash(user_data.password)
    db_user = User(
        username=user_data.username,
        email=user_data.email,
        hashed_password=hashed_password,
        wallet_address=user_data.wallet_address,
    )

    # Make the first user an admin
    if db.query(User).count() == 0:
        db_user.is_admin = True
        logger.info(f"Creating first user {user_data.username} as admin")

    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        logger.info(f"User {user_data.username} registered successfully")
        return db_user
    except Exception as e:
        db.rollback()
        logger.error(f"Error registering user: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error registering user"
        )


@authRouter.post("/auth/login", response_model=Token)
@limiter.limit("10/minute")
async def login(
    request: Request,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    """Login and get access token"""
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        logger.warning(f"Failed login attempt for username: {form_data.username}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_active:
        logger.warning(f"Inactive user attempted login: {form_data.username}")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Inactive user")

    # Generate tokens
    access_token = create_access_token(data={"sub": user.username})
    refresh_token = create_refresh_token(data={"sub": user.username})

    # Update last login
    user.last_login = datetime.now()
    db.commit()

    logger.info(f"User {form_data.username} logged in successfully")
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}


@authRouter.post("/auth/refresh", response_model=Token)
@limiter.limit("10/minute")
async def refresh_token(
    request: Request, refresh_token_data: RefreshToken, db: Session = Depends(get_db)
):
    """Refresh access token using refresh token"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(refresh_token_data.refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        logger.warning("Invalid refresh token used")
        raise credentials_exception

    user = db.query(User).filter(User.username == username).first()
    if user is None or not user.is_active:
        logger.warning(f"Token refresh attempted for non-existent or inactive user: {username}")
        raise credentials_exception

    # Generate new tokens
    access_token = create_access_token(data={"sub": username})
    refresh_token = create_refresh_token(data={"sub": username})

    logger.info(f"Tokens refreshed for user {username}")
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}


@authRouter.get("/auth/me", response_model=UserResponse)
async def get_me(current_user: User = Depends(get_current_active_user)):
    """Get current user info"""
    return current_user


@authRouter.put("/auth/me", response_model=UserResponse)
async def update_me(
    user_update: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Update current user info"""
    # Update user fields if provided
    if user_update.email:
        # Check if email already exists
        existing_email = (
            db.query(User)
            .filter(User.email == user_update.email, User.id != current_user.id)
            .first()
        )
        if existing_email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered"
            )
        current_user.email = user_update.email

    if user_update.password:
        current_user.hashed_password = get_password_hash(user_update.password)

    if user_update.wallet_address is not None:
        current_user.wallet_address = user_update.wallet_address

    try:
        db.commit()
        db.refresh(current_user)
        logger.info(f"User {current_user.username} updated profile")
        return current_user
    except Exception as e:
        db.rollback()
        logger.error(f"Error updating user: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error updating user"
        )


# Admin-only routes
@authRouter.get("/admin/users", response_model=List[UserResponse])
@limiter.limit("5/minute")
async def get_all_users(
    request: Request,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    admin_user: User = Depends(get_admin_user),
):
    """Get all users (admin only)"""
    users = db.query(User).offset(skip).limit(limit).all()
    return users


@authRouter.get("/admin/users/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int, db: Session = Depends(get_db), admin_user: User = Depends(get_admin_user)
):
    """Get user by ID (admin only)"""
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


@authRouter.put("/admin/users/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int,
    user_update: UserUpdate,
    db: Session = Depends(get_db),
    admin_user: User = Depends(get_admin_user),
):
    """Update user by ID (admin only)"""
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    # Update user fields if provided
    if user_update.email:
        # Check if email already exists
        existing_email = (
            db.query(User).filter(User.email == user_update.email, User.id != user_id).first()
        )
        if existing_email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered"
            )
        user.email = user_update.email

    if user_update.password:
        user.hashed_password = get_password_hash(user_update.password)

    if user_update.is_active is not None:
        user.is_active = user_update.is_active

    if user_update.wallet_address is not None:
        user.wallet_address = user_update.wallet_address

    try:
        db.commit()
        db.refresh(user)
        logger.info(f"Admin {admin_user.username} updated user {user.username}")
        return user
    except Exception as e:
        db.rollback()
        logger.error(f"Error updating user: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error updating user"
        )


@authRouter.delete("/admin/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: int, db: Session = Depends(get_db), admin_user: User = Depends(get_admin_user)
):
    """Delete user by ID (admin only)"""
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    # Prevent deleting yourself
    if user.id == admin_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Cannot delete your own account"
        )

    try:
        db.delete(user)
        db.commit()
        logger.info(f"Admin {admin_user.username} deleted user {user.username}")
    except Exception as e:
        db.rollback()
        logger.error(f"Error deleting user: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error deleting user"
        )
