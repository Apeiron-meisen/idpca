from sqlalchemy.orm import Session
from back_end.schema.issue_schema import IssueSave
from back_end.model.models import IssueModel
from sqlalchemy_crud_plus import CRUDPlus
from sqlalchemy.ext.asyncio import AsyncSession
class IssueRepository(CRUDPlus[IssueModel]):
  # def __init__(self, db: Session):
  #   self.db = db
  
  async def save_issue(self, db:AsyncSession,issue:IssueSave)->int:
    new_issue = IssueModel(**issue.model_dump())
    print(new_issue)
    db.add(new_issue)
    await db.commit()
    await db.refresh(new_issue)
    return new_issue.id

  async def fetch_issues(self,db:AsyncSession):
    return await self.select_models(db)

  async def fetch_issue_from_issue_id(self, db:AsyncSession, issue_id:int):
    return await self.select_model(db,issue_id)
  
issue_dao = IssueRepository(IssueModel)
  