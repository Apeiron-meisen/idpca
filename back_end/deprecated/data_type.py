from pydantic import BaseModel
class Issue(BaseModel):
  title: str
  description: str

class Plan(BaseModel):
  issue_id: int
  title: str
  content:str
  
class Action(BaseModel):
  issue_id: int
  title: str
  content: str
  
class Evaluation(BaseModel):
  issue_id: int
  title: str
  content: str
  
class Advice(BaseModel):
  issue_id: int
  title:str
  content: str