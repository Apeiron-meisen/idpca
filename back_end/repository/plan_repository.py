from sqlalchemy.orm import Session
from back_end.schema.plan_schema import PlanSave
from back_end.model.models import PlanModel
from sqlalchemy_crud_plus import CRUDPlus
from sqlalchemy.ext.asyncio import AsyncSession
class PlanRepository(CRUDPlus[PlanModel]):
  # def __init__(self, db: Session):
  #   self.db = db
  
  async def save_plan(self, db:AsyncSession,plan:PlanSave)->int:
    new_plan = PlanModel(**plan.model_dump())
    db.add(new_plan)

  async def fetch_plans(self,db:AsyncSession):
    return await self.select_models(db)
    
plan_dao = PlanRepository(PlanModel)
  