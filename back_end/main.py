from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from controller import issue_controller,plan_controller,action_controller,evaluation_controller,advice_controller
app = FastAPI()
app.include_router(issue_controller.router,tags=["Issues"])
app.include_router(plan_controller.router,tags=["Plans"])
app.include_router(action_controller.router,tags=["Actions"])
app.include_router(evaluation_controller.router,tags=["Evaluation"])
app.include_router(advice_controller.router,tags=["Advices"])

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

if __name__ == "__main__":
  import uvicorn

  uvicorn.run("main:app", host="localhost", port=8000,reload=True)