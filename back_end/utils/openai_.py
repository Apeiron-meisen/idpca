import dotenv,os
from openai import AsyncOpenAI
import asyncio
dotenv.load_dotenv()
openai_async_client = AsyncOpenAI(api_key=os.getenv('OPENAI_API_KEY'))

async def call_openai(messages:list):
  
  #如何使用异步调用OpenAI
  response = await openai_async_client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages = messages,
    stream=True,
    # max_completion_tokens=80,
  )
  async for chunk in response:
    # print(chunk.choices[0].delta.content, end='',flush=True)
    yield chunk.choices[0].delta.content

if __name__ == '__main__':
  asyncio.run(call_openai([
        {"role": "system", "content": "You are a helpful assistant."},
        {'role': 'user', 'content': 'tell me more about large language models'},
    ]))


