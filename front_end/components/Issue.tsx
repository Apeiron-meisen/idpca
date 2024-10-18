'use client'
import React,{useState,ChangeEvent, useEffect, } from 'react'
import { IssueType } from '@/app/type/type'
import useScrollNavigation from './useScrollNavigation'
import { useIssueContext } from '@/app/utils/IssueContext'

export default function Issue() {
  useScrollNavigation ()
  const {setIssue_id} = useIssueContext()
  // console.log("side issue_id: ", issue_id)
  //需要用json事先初始化
  const [input_issue, setInput_issue] = useState<IssueType>({title: '',description: ''})
  const [fetch_issues, setFetch_issues] = useState<IssueType[]>([])
  const [management, setManagement] = useState<boolean>(false)
  const [selected_issue, setSelected_issue] = useState<IssueType>({title: '',description:''})


  //useEffect 
  useEffect(()=>{

    if(management){
      // const response = await fetch()
      const fetch_from_db = async ()=>{
        const response = await fetch('http://localhost:8000/fetch_issues')
        if(!response.ok){
          throw new Error('Failed to fetch issues');
        }else{
          const data = await response.json()
          setFetch_issues(data)
        }
      }
      fetch_from_db() 
    }else{
      // setSelected_issue(0)
    }
    
  },[management])
  //不需要设置参数，全局共享state
  async function store_issue(){
    //post the backend server
    const response = await fetch('http://localhost:8000/save_issue',{
     method: 'POST',
     headers: {
       'Content-Type': 'application/json'
     },
     body: JSON.stringify(input_issue)
    })
    if(!response.ok) {throw new Error(`HTTP error! status: ${response.status}`)}
    else {
      const issue:number = await response.json()
      setIssue_id(issue.toString())
      alert("データが格納されました。")
    }
    }

  function handle_input_change(event: ChangeEvent<HTMLInputElement | HTMLTextAreaElement>){
    const {name,value } = event.target
    //
    setInput_issue({...input_issue,[name]:value})
  }
  function toggle_management_mode(){
    setManagement(previous_mode => !previous_mode)
  }
  function handle_content_change_in_management_mode(issue:IssueType):void{
    
    setIssue_id(issue.id?issue.id.toString():"")
    setSelected_issue(issue)
  }


  return (
    <div className="p-1 sm:p-2 md:p-4 h-screen overflow-hidden">
      <button
        onClick={toggle_management_mode}
        className="sm:mb-2 md:mb-4 sm:px-2 md:px-4 sm:py-1 md:py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600"
      >
        {management ? 'Exit Management' : 'Enter Management'}
      </button>

      {management ? (
        // Management mode content (e.g., menu for modifying or deleting)
        <div className='h-full w-screen'>
          <h2 className='w-full text-center text-indigo-400'>課題管理</h2>
          <div className='flex h-screen'> 
            <div className='flex-none w-1/4 bg-gray-200 p-2'>
              <h2 className='text-lg font-bold'>課題タイトル</h2> 
              <div> 
              {fetch_issues.map((issue,index)=>{
                return(
                  <button  onClick={
                    ()=>{
                    handle_content_change_in_management_mode(issue)
                  
                  }
                  } key={index} className='flex flex-col gap-2 sm:gap-4 md:gap-8 hover:opacity-60 duration-200'>
                    <p>{issue.title}</p>
                  </button>
                )
              })}

              </div>
            </div>
            <div className='flex flex-col gap-1 sm:gap-3 md:gap-5 py-2'>
              <p>課題タイトル：{selected_issue.id?selected_issue.title:input_issue.title}</p>
              <p>課題内容：</p>
              <p>{selected_issue.id?selected_issue.description:input_issue.description}</p>

            </div>
          </div>
        </div>
      ) : (
        // Normal mode content (e.g., input form)
        <div className={'flex flex-col gap-2 sm:gap-5 md:gap-6 justify-center items-center'}>
          <div className='flex flex-1'>
            <div className={'text-indigo-400 w-[200px] py-2'}>課題タイトル</div>
            <input type='text' name="title" value={input_issue?.title} onChange={handle_input_change} className='w-full max-w-[400px] px-2 py-1 border border-solid border-indigo-400 outline-none'/>
          </div>
          <div className='text-indigo-400'>課題内容</div>
          <textarea name="description" value={input_issue?.description} onChange={handle_input_change} 
          className='border border-solid border-indigo-400 w-full  h-[100px] focus:outline-none focus:ring-2 focus:ring-blue-500'
          />
          <button onClick={store_issue} className='border-indigo-600 border-solid border-2 rounded-full overflow-hidden w-[150px]'>格納</button>
          
        </div>
      )}
    </div>
  )
}
