from fastapi import FastAPI,WebSocket,HTTPException,Depends
from fastapi.requests import Request
from fastapi.middleware.cors import CORSMiddleware
from openai_ import call_openai
from dabatase_ import get_db
from psycopg2.extensions import cursor
from data_type import Issue, Plan
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

  
@app.post("/save_issue")
def store_issue(issue:Issue, db:cursor=Depends(get_db)):
  try:
    db.execute(
      query="INSERT INTO issues (title, description) VALUES (%s, %s) RETURNING id",
      vars=(issue.title, issue.description)
    )
    id:str = db.fetchone()["id"]
    print("insert OK, id is : ", id)
    return id
  except Exception as e:
    raise HTTPException(status_code=500, detail=str(e))

@app.post("/save_plan")
def store_plan(plan: Plan, db:cursor=Depends(get_db)):
  try:
    db.execute(
      query="INSERT INTO plans (title, content, issue_id) VALUES (%s, %s, %s)",
      vars=(plan.title, plan.content, plan.issue_id)
    )
  except Exception as e:
    raise HTTPException(status_code=500, detail=str(e))
@app.get("/fetch_issues")
def fetch_issues(db:cursor=Depends(get_db)):
  try:
    db.execute(query="SELECT * FROM issues")
    for row in db.fetchall():
      yield {"id": row["id"], "title": row["title"], "description": row["description"]}
    
  except Exception as e:
    raise HTTPException(status_code=500, detail=str(e))
@app.get('/fetch_plans')
def fetch_plans(db:cursor=Depends(get_db)):
  try:
    db.execute(query="SELECT * FROM plans")
    for row in db.fetchall():
      yield {"id": row["id"], "title": row["title"], "content": row["content"], "issue_id": row["issue_id"]}
  except Exception as e:
    raise HTTPException(status_code=500, detail=str(e))
  

if __name__ == "__main__":
  import uvicorn
  uvicorn.run("fastapi_server:app", host="localhost", port=8000,reload=True)