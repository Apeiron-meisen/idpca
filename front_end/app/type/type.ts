export interface IssueType{
  id?:number,
  title: string,
  description: string
}

export interface PlanType{
  id?:number,
  content:string,
  title:string,
  issue_id: number
}
export interface ActionType{
  id?:number,
  content:string,
  title:string,
  issue_id:number
}
export interface EvaluationType{
  id?:number,
  content:string,
  title: string,
  issue_id: number,
}



