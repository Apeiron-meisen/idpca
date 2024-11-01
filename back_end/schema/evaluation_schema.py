from pydantic import BaseModel
class EvaluationSave(BaseModel):
  title: str
  content: str
  issue_id: int

class EvaluationResponse(BaseModel):
  issue_id:int
  title: str
  content: str
  class Config:
    from_attributes = True