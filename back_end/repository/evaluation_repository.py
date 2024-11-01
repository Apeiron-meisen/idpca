from sqlalchemy.orm import Session
from back_end.schema.evaluation_schema import EvaluationSave
from back_end.model.models import EvaluationModel
from sqlalchemy_crud_plus import CRUDPlus
from sqlalchemy.ext.asyncio import AsyncSession
class EvaluationRepository(CRUDPlus[EvaluationModel]):
  # def __init__(self, db: Session):
  #   self.db = db
  
  async def save_evaluation(self, db:AsyncSession,evaluation:EvaluationSave)->int:
    new_evaluation = EvaluationModel(**evaluation.model_dump())
    db.add(new_evaluation)

  async def fetch_evaluations(self,db:AsyncSession):
    return await self.select_models(db)
    
evaluation_dao = EvaluationRepository(EvaluationModel)
  