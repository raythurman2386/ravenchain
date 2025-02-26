# RavenChain

A modern, Python-based blockchain implementation focusing on simplicity, security, and scalability. RavenChain demonstrates core blockchain concepts while providing a foundation for building decentralized applications.

## 🚀 Features

### Current Features
- ✅ Core blockchain implementation with proof-of-work mining
- ✅ Secure wallet management with ECDSA cryptography
- ✅ Transaction system with digital signatures
- ✅ Bitcoin-style address generation
- ✅ Interactive command-line interface
- ✅ Persistent wallet storage
- ✅ Chain validation and integrity checking
- ✅ Mining rewards system
- ✅ FastAPI-based REST API
- ✅ Database persistence with PostgreSQL
- ✅ Docker containerization

### Planned Features
- 🔄 Peer-to-peer networking
- 📊 Block explorer web interface
- 📜 Smart contract support
- 🔍 UTXO model implementation
- 🔒 Enhanced security features
- ⚡ Performance optimizations

## 🛠 Technology Stack

- **Language**: Python 3.13+
- **Cryptography**: `ecdsa`, `hashlib`
- **Storage**: PostgreSQL for blockchain persistence
- **Backend**: FastAPI for REST API endpoints
- **Frontend**: React 19 with TypeScript (planned)
- **Future Stack**:
  - WebSocket for real-time updates
  - Redis for caching
  - Elasticsearch for block/transaction search (optional)

## 🏗 Project Structure

```
ravenchain/
├── ravenchain/              # Core package
│   ├── __init__.py
│   ├── block.py            # Block implementation
│   ├── blockchain.py       # Main blockchain logic
│   ├── transaction.py      # Transaction handling
│   └── wallet.py           # Wallet management
├── api/                    # FastAPI backend
│   ├── __init__.py
│   ├── main.py            # API entry point
│   ├── routes/            # API route handlers
│   │   ├── block_routes.py
│   │   ├── mining_routes.py
│   │   ├── transaction_routes.py
│   │   └── wallet_routes.py
│   └── database/          # Database models and config
│       └── models.py
├── config/                # Configuration
│   ├── settings.py        # App settings
│   └── logging.py         # Logging setup
├── scripts/               # Utility scripts
├── tests/                 # Test suite
├── Dockerfile            # Docker build file
├── docker-compose.yml    # Docker services config
└── requirements.txt      # Python dependencies
```

## 🚀 Quick Start

### Prerequisites

- Python 3.13 or higher
- pip (Python package installer)

OR

- Docker
- Docker Compose

### Installation

#### Using Python (Traditional Setup)

```bash
# Clone the repository
git clone https://github.com/yourusername/ravenchain.git
cd ravenchain

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -e .
```

#### Using Docker 🐳

```bash
# Clone the repository
git clone https://github.com/yourusername/ravenchain.git
cd ravenchain

# Build and start the containers
docker-compose up --build

# Or run in detached mode
docker-compose up -d
```

The Docker setup provides:
- Isolated development environment
- Consistent dependencies across platforms
- Easy setup for future features (API, database)
- Production-ready container configuration

### Running Tests with Docker

```bash
# Run tests in a new container
docker-compose run --rm ravenchain pytest

# Run tests with coverage
docker-compose run --rm ravenchain pytest --cov=ravenchain
```

## 🎯 Roadmap

### Phase 1: Core Infrastructure Enhancement
- [x] Basic blockchain implementation
- [x] Wallet management system
- [x] Command-line interface
- [x] Transaction handling
- [x] Unit test coverage
- [x] Documentation improvements

### Phase 2: Data Persistence & API 
- [x] Implement PostgreSQL for blockchain storage
- [x] Design and implement FastAPI REST API
  - [x] Block endpoints
  - [x] Transaction endpoints
  - [x] Wallet endpoints
  - [x] Mining endpoints
- [x] API documentation with Swagger/OpenAPI
- [x] Request rate limiting
- [x] API authentication system

### Phase 3: Networking & Distribution (Current)
- [ ] P2P network implementation
  - [ ] Node discovery protocol
  - [ ] Block synchronization
  - [ ] Transaction broadcasting
- [ ] Consensus mechanism improvements
- [ ] Network state management
- [ ] Peer management system

### Phase 4: Smart Contracts & Advanced Features (Next)
- [ ] Basic smart contract engine
- [ ] Contract deployment system
- [ ] Standard contract templates
- [ ] Contract execution environment
- [ ] Gas fee implementation

### Phase 5: Performance & Security
- [ ] UTXO model implementation
- [ ] Merkle tree optimization
- [ ] Chain pruning
- [ ] Advanced security features
  - [ ] Double-spend protection
  - [ ] Sybil attack prevention
  - [ ] DDoS mitigation
- [ ] Performance benchmarking

### Phase 6: User Interface & Tools
- [ ] Block explorer web interface
- [ ] Wallet GUI application
- [ ] Network monitoring tools
- [ ] Development tools and SDKs

## 🧪 Testing

```bash
pytest tests/
```

## 📖 API Documentation

The REST API will provide the following endpoints:

```
# Authentication Endpoints
POST   /api/v1/auth/register       # Register a new user
POST   /api/v1/auth/login          # Login and get tokens
POST   /api/v1/auth/refresh        # Refresh access token
GET    /api/v1/auth/me             # Get current user info
PUT    /api/v1/auth/me             # Update current user info

# Admin Endpoints
GET    /api/v1/admin/users         # List all users (admin only)
GET    /api/v1/admin/users/{id}    # Get user details (admin only)
PUT    /api/v1/admin/users/{id}    # Update user (admin only) 
DELETE /api/v1/admin/users/{id}    # Delete user (admin only)

# Block Endpoints
GET    /api/v1/blocks              # List blocks
GET    /api/v1/blocks/{hash}       # Get block details
GET    /api/v1/blocks/latest       # Get latest block

# Transaction Endpoints
GET    /api/v1/transactions        # List transactions
POST   /api/v1/transactions        # Create transaction

# Wallet Endpoints
GET    /api/v1/wallets/{address}   # Get wallet info

# Mining Endpoints
POST   /api/v1/mine                # Mine new block
```

Detailed API documentation is available via Swagger UI at `/docs`.

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with Python's cryptographic libraries
- Inspired by blockchain technology principles
- Community contributions and feedback

## 📞 Contact

Ray Thurman - [@raythurman2386](https://github.com/raythurman2386)

Project Link: [https://github.com/raythurman2386/ravenchain](https://github.com/raythurman2386/ravenchain)
