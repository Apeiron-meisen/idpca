from pydantic import BaseModel
class IssueSave(BaseModel):
  title: str
  description: str

class IssueIDResponse(BaseModel):
  id:int
  class Config:
    from_attributes = True
class IssueResponse(BaseModel):
  id:int
  title: str
  description: str
  class Config:
    from_attributes = True