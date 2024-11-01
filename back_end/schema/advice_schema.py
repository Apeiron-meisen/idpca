from pydantic import BaseModel
class AdviceSave(BaseModel):
  title: str
  content: str
  issue_id: int

class AdviceResponse(BaseModel):
  issue_id:int
  title: str
  content: str
  class Config:
    from_attributes = True