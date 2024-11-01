from back_end.repository.advice_repository import advice_dao
from back_end.schema.advice_schema import AdviceSave
from back_end.model.models import AdviceModel
from back_end.utils.database import session
from back_end.schema.advice_schema import AdviceResponse

class AdviceService:
  # def __init__(self,db:Session) -> None:
  #   self.advice_respository = AdviceRepository(db)
  @staticmethod
  async def save_advice(*, advice:AdviceSave)->None:
    async with session.begin() as db:
      await advice_dao.save_advice(db,advice)
  @staticmethod
  async def fetch_advices()->list[AdviceModel]:
    async with session.begin() as db:
      response_list = list()
      advices:list[AdviceModel] =  await advice_dao.fetch_advices(db)
      for advice in advices:
        response_list.append(AdviceResponse.model_validate(advice,from_attributes=True))
      return response_list

    
advice_service = AdviceService()