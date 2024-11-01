from fastapi import APIRouter, Depends
from back_end.service.plan_service import plan_service
from back_end.schema.plan_schema import PlanSave,PlanResponse
router = APIRouter()

@router.post('/save_plan')
async def save_plan(plan:PlanSave)->None:
  await plan_service.save_plan(plan=plan)

@router.get('/fetch_plans', response_model=list[PlanResponse])
async def fetch_plans():
  return await plan_service.fetch_plans() 
