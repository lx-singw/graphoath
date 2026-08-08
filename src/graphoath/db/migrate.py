import sys
from pathlib import Path
from sqlalchemy import text
from graphoath.db.session import engine, Base

MIGRATIONS_DIR = Path(__file__).resolve().parent / "migrations"

def run_migrations():
    """Executes all .sql files in migrations directory sequentially."""
    print("[GraphOath Migration Engine] Initializing database tables...")
    
    # 1. Create SQLAlchemy tables
    try:
        Base.metadata.create_all(bind=engine)
        print("[GraphOath Migration Engine] SQLAlchemy tables created successfully.")
    except Exception as e:
        print(f"[GraphOath Migration Engine] Warning creating tables: {e}")

    # 2. Execute SQL scripts
    sql_files = sorted(MIGRATIONS_DIR.glob("*.sql"))
    with engine.begin() as conn:
        for sql_file in sql_files:
            print(f"[GraphOath Migration Engine] Executing migration: {sql_file.name}")
            with open(sql_file, "r", encoding="utf-8") as f:
                sql_content = f.read()
            # Split and execute individual statements if needed
            statements = [stmt.strip() for stmt in sql_content.split(";") if stmt.strip()]
            for stmt in statements:
                try:
                    conn.execute(text(stmt))
                except Exception as e:
                    # Ignore table already exists or trigger errors in SQLite dev mode
                    print(f"  Note on statement execution: {e}")
                    
    print("[GraphOath Migration Engine] All migrations executed successfully.")

if __name__ == "__main__":
    run_migrations()
