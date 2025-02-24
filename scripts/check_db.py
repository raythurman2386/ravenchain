from sqlalchemy import inspect, create_engine
from config.settings import settings

engine = create_engine(settings.DATABASE_URL)
inspector = inspect(engine)

print("Database Tables:")
for table_name in inspector.get_table_names():
    print(f"\nTable: {table_name}")
    print("Columns:")
    for column in inspector.get_columns(table_name):
        print(f"  - {column['name']}: {column['type']}")
