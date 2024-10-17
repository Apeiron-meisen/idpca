'use client'
import React ,{useContext,useState ,useEffect,createContext}from 'react'
import { LayoutProps } from '../layout'
const issue_context = createContext<{issue_id:string,setIssue_id:React.Dispatch<React.SetStateAction<string>>}>({
  issue_id: '',
  setIssue_id: () => {} 
})

export function useIssueContext(){
  return useContext(issue_context)
}

export default function IssueProvider({children}:LayoutProps) {
  const [issue_id, setIssue_id] = useState<string>("1")
  const value={
    issue_id,
    setIssue_id
  }
  return (
    <issue_context.Provider value={value}>{children}</issue_context.Provider>
  )
}

