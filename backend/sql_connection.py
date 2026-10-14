import os
import mysql.connector
from mysql.connector import Error

# Load .env if python-dotenv is installed
try:
    from dotenv import load_dotenv
    # Look for .env in current and project root directories
    load_dotenv()
    parent_env = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env')
    if os.path.exists(parent_env):
        load_dotenv(parent_env)
except ImportError:
    pass

__cnx = None


def _create_connection(user, password, host, port, database, profile_name):
    """Helper to attempt a connection with given parameters."""
    try:
        cnx = mysql.connector.connect(
            user=user,
            password=password,
            host=host,
            port=int(port),
            database=database
        )
        if cnx.is_connected():
            print(f"[DB] Successfully connected via {profile_name} "
                  f"(user: '{user}', host: {host}:{port}, database: '{database}')")
            return cnx
    except Error:
        return None
    except Exception:
        return None
    return None


def get_sql_connection(mode=None):
    """
    Returns an active MySQL connection.
    Supports:
      - 'xampp'  : Connects using XAMPP MySQL defaults (root, empty password)
      - 'direct' : Connects using Direct MySQL settings (root, password from env or default)
      - 'auto'   : Tries Direct MySQL first; if it fails, automatically tries XAMPP.
    """
    global __cnx

    # Re-use existing connection if it is still alive
    if __cnx is not None:
        try:
            if __cnx.is_connected():
                __cnx.ping(reconnect=True, attempts=2, delay=1)
                return __cnx
        except Exception:
            __cnx = None

    # Read configuration from environment or defaults
    db_mode = (mode or os.getenv("DB_MODE", "auto")).lower()
    host = os.getenv("DB_HOST", "127.0.0.1")
    port = int(os.getenv("DB_PORT", 3306))
    database = os.getenv("DB_NAME", "gs")
    user = os.getenv("DB_USER", "root")

    direct_password = os.getenv("DB_PASSWORD", "Kolkata@786")
    xampp_password = os.getenv("XAMPP_DB_PASSWORD", "")

    direct_config = {
        "user": user,
        "password": direct_password,
        "host": host,
        "port": port,
        "database": database,
        "profile_name": "Direct MySQL"
    }

    xampp_config = {
        "user": user,
        "password": xampp_password,
        "host": host,
        "port": port,
        "database": database,
        "profile_name": "XAMPP MySQL"
    }

    if db_mode == "xampp":
        attempts = [xampp_config]
    elif db_mode == "direct":
        attempts = [direct_config]
    else:  # 'auto' mode
        # Try Direct MySQL first, fallback to XAMPP MySQL
        attempts = [direct_config, xampp_config]

    for config in attempts:
        conn = _create_connection(**config)
        if conn is not None:
            __cnx = conn
            return __cnx

    print("\n" + "=" * 65)
    print("[DB ERROR] Unable to connect to MySQL database!")
    print(f"Attempted profile(s): {[cfg['profile_name'] for cfg in attempts]}")
    print(f"Target Database: '{database}', Host: {host}:{port}, User: '{user}'")
    print("\nTroubleshooting tips:")
    print(" 1. If using XAMPP: Make sure MySQL is started in XAMPP Control Panel.")
    print(" 2. If using Direct MySQL: Ensure MySQL service is running.")
    print(" 3. Ensure database 'gs' is created by importing 'database.sql'.")
    print(" 4. You can set DB_MODE=xampp or DB_MODE=direct in a .env file.")
    print("=" * 65 + "\n")

    return None