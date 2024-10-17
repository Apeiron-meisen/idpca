"use client"
import React from 'react'
import useScrollNavigation from './useScrollNavigation'
import { useIssueContext } from '@/app/utils/IssueContext'
export default function Action() {
  useScrollNavigation ()
  const {issue_id, setIssue_id} = useIssueContext()

  console.log("actiono issue_id: " + issue_id)
  return (
    
    <div>Action</div>
  )
}
