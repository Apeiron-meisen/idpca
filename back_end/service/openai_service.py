from fastapi import WebSocket
from back_end.utils.prompt import PLAN_TEMPLATE,EVALUTION_TEMPLATE,ADVICE_TEMPLATE
from back_end.utils.openai_ import call_openai
class OpenaiService:
  @staticmethod
  async def generate_plan(user_info_list:list[str],request_message:list[str],websocket:WebSocket):
    request_message.append({"role":"system","content":"あなたは専門的なプロジェクトマネージャーです。課題内容と計画タイトルに基づいてアクションプランを作成してください。"})
    request_message.append({"role":"user","content":PLAN_TEMPLATE.format(issue_content = user_info_list[0],directive=user_info_list[1])})
    async for char in call_openai(request_message):
      if char:
        await websocket.send_text(char)
  
  @staticmethod
  async def generate_evaluation(user_info_list:list[str],request_message:list[str],websocket:WebSocket):
    request_message.append({"role":"system","content":"あなたは専門的なプロジェクトマネージャーです。課題内容に基づいて今までの行動を評価してください。"})
    request_message.append({"role":"user","content":EVALUTION_TEMPLATE.format(issue_content = user_info_list[0],directive=user_info_list[1],action_content=user_info_list[2])})
    async for char in call_openai(request_message):
      if char:
        await websocket.send_text(char)
  
  @staticmethod
  async def generate_advice(user_info_list:list[str],request_message:list[str],websocket:WebSocket):
    request_message.append({"role":"system","content":"あなたは専門的なプロジェクトマネージャーです。課題内容と評価に基づいてアドバイスをしてください。"})
    request_message.append({"role":"user","content":ADVICE_TEMPLATE.format(issue_content = user_info_list[0],directive=user_info_list[1],action_content=user_info_list[2])})
    async for char in call_openai(request_message):
      if char:
        await websocket.send_text(char)

openai_service = OpenaiService()