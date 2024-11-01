from pydantic import BaseModel
class PlanSave(BaseModel):
  title: str
  content: str
  issue_id: int

class PlanResponse(BaseModel):
  issue_id:int
  title: str
  content: str
  class Config:
    from_attributes = True