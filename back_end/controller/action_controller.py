from fastapi import APIRouter
from back_end.service.action_service import action_service
from back_end.schema.action_schema import ActionSave,ActionResponse
router = APIRouter()

@router.post('/save_action')
async def save_action(action:ActionSave)->None:
  await action_service.save_action(action=action)

@router.get('/fetch_actions', response_model=list[ActionResponse])
async def fetch_actions():
  return await action_service.fetch_actions() 
