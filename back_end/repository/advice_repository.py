from sqlalchemy.orm import Session
from back_end.schema.advice_schema import AdviceSave
from back_end.model.models import AdviceModel
from sqlalchemy_crud_plus import CRUDPlus
from sqlalchemy.ext.asyncio import AsyncSession
class AdviceRepository(CRUDPlus[AdviceModel]):
  # def __init__(self, db: Session):
  #   self.db = db
  
  async def save_advice(self, db:AsyncSession,advice:AdviceSave)->int:
    new_advice = AdviceModel(**advice.model_dump())
    db.add(new_advice)

  async def fetch_advices(self,db:AsyncSession):
    return await self.select_models(db)
    
advice_dao = AdviceRepository(AdviceModel)
  