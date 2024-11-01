from fastapi import APIRouter,WebSocket
from back_end.service.openai_service import openai_service
router = APIRouter()

@router.websocket("/generate_content")
async def generate_content(websocket:WebSocket):
  await websocket.accept()
  request_message = []
  while True:
    user_message = await websocket.receive_text()
    user_info_list = user_message.split(",")
    #メッセージの最後に計画、評価、アドバイスの接続を付けます。
    if user_info_list.pop() == 'plan':
      await openai_service.generate_plan(user_info_list,request_message,websocket)
    elif user_info_list.pop() == 'evaluation':
      await openai_service.generate_evaluation(user_info_list,request_message,websocket)
    elif user_info_list.pop() == 'advice':
      await openai_service.generate_advice(user_info_list,request_message,websocket)
    else:
      raise Exception("接続をつけてください")
  
    