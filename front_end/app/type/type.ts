export interface IssueType{
  id?:number,
  title: string,
  description: string
}

export interface PlanType{
  id?:number
  content:string,
  title:string
  issue_id: number
}

