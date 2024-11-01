from back_end.repository.evaluation_repository import evaluation_dao
from back_end.schema.evaluation_schema import EvaluationSave
from back_end.model.models import EvaluationModel
from back_end.utils.database import session
from back_end.schema.evaluation_schema import EvaluationResponse

class EvaluationService:
  @staticmethod
  async def save_evaluation(*, evaluation:EvaluationSave)->None:
    async with session.begin() as db:
      await evaluation_dao.save_evaluation(db,evaluation)
  @staticmethod
  async def fetch_evaluations()->list[EvaluationModel]:
    async with session.begin() as db:
      response_list = list()
      evaluations:list[EvaluationModel] =  await evaluation_dao.fetch_evaluations(db)
      for evaluation in evaluations:
        response_list.append(EvaluationResponse.model_validate(evaluation,from_attributes=True))
      return response_list

    
evaluation_service = EvaluationService()