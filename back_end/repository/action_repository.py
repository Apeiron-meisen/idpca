from sqlalchemy.orm import Session
from back_end.schema.action_schema import ActionSave
from back_end.model.models import ActionModel,IssueModel
from sqlalchemy_crud_plus import CRUDPlus
from sqlalchemy.ext.asyncio import AsyncSession
class ActionRepository(CRUDPlus[ActionModel]):
  
  async def save_action(self, db:AsyncSession,action:ActionSave,issue:IssueModel):
    print(issue.__dict__)
    new_action =  ActionModel(title=action.title, content=action.content)
    new_action.issues.append(issue)
    db.add(new_action)

  async def fetch_actions(self,db:AsyncSession):
    return await self.select_models(db)
    
action_dao = ActionRepository(ActionModel)
  