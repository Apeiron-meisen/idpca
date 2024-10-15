from fastapi import FastAPI,WebSocket,HTTPException
from fastapi.requests import Request
from fastapi.middleware.cors import CORSMiddleware
from openai_ import call_openai
from dabatase_ import get_db_connection
from psycopg2.extensions import connection, cursor
from data_type import Issue
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

  
@app.post("/issue")
def store_issue(issue:Issue):
  db_connection:connection = get_db_connection()
  db_cursor:cursor  = db_connection.cursor()
  try:
    db_cursor.execute(
      query="INSERT INTO issues (title, description) VALUES (%s, %s) RETURNING id",
      vars=(issue.title, issue.description)
    )
    db_connection.commit()
    print("insert OK")
  except Exception as e:
    db_connection.rollback()
    raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
  import uvicorn
  uvicorn.run("fastapi_server:app", host="localhost", port=8000,reload=True)