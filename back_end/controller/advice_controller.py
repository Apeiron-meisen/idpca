from fastapi import APIRouter, Depends
from back_end.service.advice_service import advice_service
from back_end.schema.advice_schema import AdviceSave,AdviceResponse
router = APIRouter()

@router.post('/save_advice')
async def save_advice(advice:AdviceSave)->None:
  await advice_service.save_advice(advice=advice)

@router.get('/fetch_advices', response_model=list[AdviceResponse])
async def fetch_advices():
  return await advice_service.fetch_advices() 
