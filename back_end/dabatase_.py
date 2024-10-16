from fastapi import HTTPException
from psycopg2.extensions import connection
import psycopg2
from psycopg2.extras import RealDictCursor
import os,dotenv

dotenv.load_dotenv()
conn:connection = psycopg2.connect(
  host=os.getenv("POSTGRES_HOST"),
  dbname=os.getenv("POSTGRES_DB"),
  user=os.getenv("POSTGRES_USER"),
  password=os.getenv("POSTGRES_PASSWORD"),
  cursor_factory=RealDictCursor
)
def get_db():
  try:
        # Open a cursor to perform database operations
        cursor = conn.cursor()
        yield cursor
        # Commit the transaction if everything is successful
        conn.commit()
        print("commit over!")
  except Exception as e:
        # Rollback the transaction in case of error
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
  finally:
        # Close the cursor after the request is done
        cursor.close()