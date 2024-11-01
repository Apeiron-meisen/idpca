from typing import Generator
from fastapi import FastAPI,WebSocket,HTTPException,Depends
from fastapi.requests import Request
from fastapi.middleware.cors import CORSMiddleware
from back_end.utils.openai_ import call_openai
from back_end.deprecated.dabatase_ import get_db
from psycopg2.extensions import cursor
from back_end.deprecated.data_type import Issue, Plan,Action,Evaluation,Advice
from back_end.utils.prompt import PLAN_TEMPLATE
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# @app.get("/fetch_issue_description_from_issue_id")
# def fetch_issue_description_from_issue_id(issue_id:str, db:cursor=Depends(get_db)):
#   print("issue_id: ", issue_id)
#   try:
#     db.execute(
#       query="SELECT description FROM issues WHERE id = %s",
#       vars=(issue_id,)
#     )
#     description:str = db.fetchone()["description"]
#     return {"description":description}
#   except Exception as e:
#     print(e)
    
# @app.get("/fetch_issue_title_from_issue_id")
# def fetch_issue_description_from_issue_id(issue_id:str, db:cursor=Depends(get_db)):
#   print("issue_id: ", issue_id)
#   try:
#     db.execute(
#       query="SELECT description FROM issues WHERE id = %s",
#       vars=(issue_id,)
#     )
#     description:str = db.fetchone()["description"]
#     return {"description":description}
#   except Exception as e:
#     print(e)

# @app.websocket("/generate_content")
# async def generate_content(websocket:WebSocket)->None:
#   await websocket.accept()
#   request_message = []
#   while True:
#     user_message= await websocket.receive_text()
#     print(user_message)
#     arr = user_message.split(',')
#     request_message.append({"role":"system","content":"あなたは専門的なプロジェクトマネージャーです。課題内容と計画タイトルに基づいてアクションプランを作成してください。"})
#     request_message.append({"role":"user","content":PLAN_TEMPLATE.format(issue_content = arr[0],directive=arr[1])})
#     async for char in call_openai(request_message):
#       if char:
#         await websocket.send_text(char)
  
# @app.post("/save_issue")
# def save_issue(issue:Issue, db:cursor=Depends(get_db)):
#   try:
#     db.execute(
#       query="INSERT INTO issues (title, description) VALUES (%s, %s) RETURNING id",
#       vars=(issue.title, issue.description)
#     )
#     id:str = db.fetchone()["id"]
#     print("insert OK, id is : ", id)
#     return id
#   except Exception as e:
#     raise HTTPException(status_code=500, detail=str(e))
# 
# @app.post("/save_plan")
# def save_plan(plan: Plan, db:cursor=Depends(get_db)):
#   try:
#     db.execute(
#       query="INSERT INTO plans (title, content, issue_id) VALUES (%s, %s, %s)",
#       vars=(plan.title, plan.content, plan.issue_id)
#     )
#   except Exception as e:
#     raise HTTPException(status_code=500, detail=str(e))

@app.post('/save_plan_generated_from_chatGPT')
def save_plan_generated_from_chatGPT(plan: Plan, db:cursor=Depends(get_db)):
  try:
    db.execute(
      query="INSERT INTO plans (title, content, issue_id) VALUES (%s, %s, %s)",
      vars=(plan.title, plan.content, plan.issue_id)
    )
  except Exception as e:
    raise HTTPException(status_code=500, detail=str(e))
# @app.post('/save_action')
# def save_action(action:Action,db:cursor=Depends(get_db)):
#   try:
#     db.execute(
#       query="INSERT INTO actions (title,content,issue_id) VALUES (%s, %s,%s)",
#       vars=(action.title,action.content, action.issue_id)   
#     )   
#   except Exception as e:
#     raise HTTPException(status_code=500, detail=str(e))  
# @app.post("/save_evaluation")
# def save_evaluation(evaluation: Evaluation, db:cursor=Depends(get_db)):
#   print("evaluation saved:  " )
#   try:
#     db.execute(
#       query="INSERT INTO evaluations (title, content, issue_id) VALUES (%s, %s, %s)",
#       vars=(evaluation.title, evaluation.content, evaluation.issue_id)
#     )
#     print("success!")
#   except Exception as e:
#     raise HTTPException(status_code=500, detail=str(e))
# @app.post("/save_advice")
# def save_evaluation(advice: Advice, db:cursor=Depends(get_db)):
#   try:
#     db.execute(
#       query="INSERT INTO advice (title, content, issue_id) VALUES (%s, %s, %s)",
#       vars=(advice.title, advice.content, advice.issue_id)
#     )
#   except Exception as e:
#     raise HTTPException(status_code=500, detail=str(e))


# # @app.get("/fetch_issues")
# # def fetch_issues(db:cursor=Depends(get_db)):
#   try:
#     db.execute(query="SELECT * FROM issues")
#     for row in db.fetchall():
#       yield {"id": row["id"], "title": row["title"], "description": row["description"]}
    
#   except Exception as e:
#     raise HTTPException(status_code=500, detail=str(e))
# @app.get('/fetch_plans')
# def fetch_plans(db:cursor=Depends(get_db)):
#     try:
#         db.execute(query="SELECT * FROM plans")
#         for row in db.fetchall():
#             yield {"id": row["id"], "title": row["title"], "content": row["content"], "issue_id": row["issue_id"]}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
# @app.get("/fetch_actions")
# def fetch_plans(db:cursor=Depends(get_db)):
#     try:
#         db.execute(query="SELECT * FROM actions")
#         for row in db.fetchall():
#             yield {"id": row["action_id"],"title": row["title"],"content": row["content"], "issue_id": row["issue_id"]}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
# @app.get("/fetch_evaluations")
# def fetch_evaluations(db:cursor=Depends(get_db)):
#     try:
#         db.execute(query="SELECT * FROM evaluations")
#         for row in db.fetchall():
#             yield {"id": row["id"],"title": row["title"],"content": row["content"], "issue_id": row["issue_id"]}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
  import uvicorn
  uvicorn.run("fastapi_server:app", host="localhost", port=8000,reload=True)