from pydantic import BaseModel
class ActionSave(BaseModel):
  title: str
  content: str
  issue_id: int

class ActionResponse(BaseModel):
  id:int
  title: str
  content: str
  class Config:
    from_attributes = True