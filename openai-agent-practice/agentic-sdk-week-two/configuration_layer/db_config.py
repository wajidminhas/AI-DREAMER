import os
from urllib.parse import urlparse
import psycopg2
from psycopg2.extras import RealDictCursor

def get_db_connection():
    """
    Parses DATABASE_URL on-the-fly to establish a secure connection 
    to the pgvector instance without exposing credentials.
    """
    db_url = os.environ.get("DATABASE_URL")
    if not db_url:
        raise ValueError("Critical Configuration Error: DATABASE_URL environment variable is missing.")
    
    try:
        # Standardize URL handling for psycopg2 compatibility
        # If using 'postgresql://', urlparse handles it natively
        parsed = urlparse(db_url)
        
        # Safely extract parts
        username = parsed.username
        password = parsed.password
        database = parsed.path.lstrip('/')
        hostname = parsed.hostname
        port = parsed.port or 5432
        
        # Re-inject sslmode parameters from query string if present
        # urlparse aggregates queries into .query (e.g., 'sslmode=require')
        connection_kwargs = {
            "dbname": database,
            "user": username,
            "password": password,
            "host": hostname,
            "port": port
        }
        
        # Simple extraction for sslmode query parameter if present
        if parsed.query:
            queries = dict(q.split('=') for q in parsed.query.split('&') if '=' in q)
            if 'sslmode' in queries:
                connection_kwargs['sslmode'] = queries['sslmode']

        return psycopg2.connect(
            **connection_kwargs,
            cursor_factory=RealDictCursor
        )
        
    except Exception as e:
        raise RuntimeError(f"Failed to parse database connection string or connect to server: {str(e)}")

def init_vector_db():
    """Ensures pgvector extension and the required tables are ready."""
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("CREATE EXTENSION IF NOT EXISTS vector;")
            cur.execute("""
                CREATE TABLE IF NOT EXISTS documentation_chunks (
                    id SERIAL PRIMARY KEY,
                    content TEXT NOT NULL,
                    embedding vector(1536) NOT NULL
                );
            """)
            conn.commit()
            print("[Database] Connection successful. Table structures verified securely.")
    except Exception as e:
        print(f"[Database Error] Initialization failed: {e}")
        conn.rollback()
    finally:
        conn.close()