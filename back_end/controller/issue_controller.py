from fastapi import APIRouter, Depends
from back_end.service.issue_service import issue_service
from back_end.schema.issue_schema import IssueSave,IssueIDResponse,IssueResponse
router = APIRouter()



@router.post('/save_issue',response_model=IssueIDResponse)
async def save_issue(issue:IssueSave):
  issue_id:int =  await issue_service.save_issue(issue=issue)
  return {"id": issue_id}

@router.get('/fetch_issues', response_model=list[IssueResponse])
async def fetch_issues():
  return await issue_service.fetch_issues() 

@router.get("/fetch_issue_title_from_issue_id",response_model=str)
async def fetch_issue_title_from_issue_id(issue_id:int):
  return await issue_service.fetch_issue_title_from_issue_id(issue_id)
@router.get("/fetch_issue_description_from_issue_id",response_model=str)
async def fetch_issue_description_from_issue_id(issue_id:int):
  return await issue_service.fetch_issue_description_from_issue_id(issue_id)