from back_end.repository.action_repository import action_dao
from back_end.repository.issue_repository import issue_dao
from back_end.schema.action_schema import ActionSave
from back_end.model.models import ActionModel,IssueModel
from back_end.utils.database import session
from back_end.schema.action_schema import ActionResponse

class ActionService:
  @staticmethod
  async def save_action(*, action:ActionSave)->None:
    async with session.begin() as db:
      issue:IssueModel = await issue_dao.fetch_issue_from_issue_id(db,action.issue_id)
      await action_dao.save_action(db,action,issue)
  @staticmethod
  async def fetch_actions()->list[ActionModel]:
    async with session.begin() as db:
      response_list = list()
      actions:list[ActionModel] =  await action_dao.fetch_actions(db)
      for action in actions:
        response_list.append(ActionResponse.model_validate(action,from_attributes=True))
      return response_list

    
action_service = ActionService()