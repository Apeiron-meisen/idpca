from psycopg2.extensions import connection
import psycopg2
from psycopg2.extras import RealDictCursor
import os,dotenv
def get_db_connection()->connection:
  dotenv.load_dotenv()
  conn:connection = psycopg2.connect(
    host=os.getenv("POSTGRES_HOST"),
    dbname=os.getenv("POSTGRES_DB"),
    user=os.getenv("POSTGRES_USER"),
    password=os.getenv("POSTGRES_PASSWORD"),
    cursor_factory=RealDictCursor
  )
  return conn