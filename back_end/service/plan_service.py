from back_end.repository.plan_repository import plan_dao
from back_end.schema.plan_schema import PlanSave
from back_end.model.models import PlanModel
from back_end.utils.database import session
from back_end.schema.plan_schema import PlanResponse

class PlanService:
  # def __init__(self,db:Session) -> None:
  #   self.plan_respository = PlanRepository(db)
  @staticmethod
  async def save_plan(*, plan:PlanSave)->None:
    async with session.begin() as db:
      await plan_dao.save_plan(db,plan)
  @staticmethod
  async def fetch_plans()->list[PlanModel]:
    async with session.begin() as db:
      response_list = list()
      plans:list[PlanModel] =  await plan_dao.fetch_plans(db)
      for plan in plans:
        response_list.append(PlanResponse.model_validate(plan,from_attributes=True))
      return response_list

    
plan_service = PlanService()