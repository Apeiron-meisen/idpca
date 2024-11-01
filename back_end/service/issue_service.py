from back_end.repository.issue_repository import issue_dao
from back_end.schema.issue_schema import IssueSave
from back_end.model.models import IssueModel
from back_end.utils.database import session
from back_end.schema.issue_schema import IssueResponse

class IssueService:
  # def __init__(self,db:Session) -> None:
  #   self.issue_respository = IssueRepository(db)
  @staticmethod
  async def save_issue(*, issue:IssueSave)->int:
    async with session() as db:
      issue_id =  await issue_dao.save_issue(db,issue)
      return issue_id
  @staticmethod
  async def fetch_issues()->list[IssueModel]:
    async with session.begin() as db:
      response_list = list()
      issues:list[IssueModel] =  await issue_dao.fetch_issues(db)
      for issue in issues:
        response_list.append(IssueResponse.model_validate(issue))
      return response_list
  @staticmethod
  async def fetch_issue_title_from_issue_id(issue_id:int)->str:
    async with session.begin() as db:
      issue =  await issue_dao.fetch_issue_from_issue_id(db, issue_id)
      return issue.title
  @staticmethod
  async def fetch_issue_description_from_issue_id(issue_id:int)->str:
    async with session.begin() as db:
      issue =  await issue_dao.fetch_issue_from_issue_id(db, issue_id)
      return issue.description  
    
issue_service = IssueService()