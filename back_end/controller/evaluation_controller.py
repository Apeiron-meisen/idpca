from fastapi import APIRouter, Depends
from back_end.service.evaluation_service import evaluation_service
from back_end.schema.evaluation_schema import EvaluationSave,EvaluationResponse
router = APIRouter()

@router.post('/save_evaluation')
async def save_evaluation(evaluation:EvaluationSave)->None:
  await evaluation_service.save_evaluation(evaluation=evaluation)

@router.get('/fetch_evaluations', response_model=list[EvaluationResponse])
async def fetch_evaluations():
  return await evaluation_service.fetch_evaluations() 
