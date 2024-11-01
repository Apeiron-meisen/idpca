"use client"
import React,{useState, useEffect,ChangeEvent} from 'react'
import useScrollNavigation from './useScrollNavigation'
import { useIssueContext } from '@/app/utils/IssueContext'
import { ActionType } from '@/app/type/type'
export default function Action() {
  useScrollNavigation ()
  const {issue_id, setIssue_id} = useIssueContext()
  const [input_action, setInput_action] = useState<ActionType>({content: '',title: '',issue_id: +issue_id})
  const [management, setManagement] = useState<boolean>(false)
  const [fetch_actions, setFetch_actions] = useState<ActionType[]>([])
  const [selected_action, setSelected_action] = useState<ActionType>({content: '',title: '',issue_id: +issue_id})

  useEffect(()=>{

    if(management){
      // const response = await fetch()
      const fetch_from_db = async ()=>{
        console.log('start')
        const response = await fetch('http://localhost:8000/fetch_actions')
        console.log('end')
        if(!response.ok){
          console.log(response.statusText)
          throw new Error('Failed to fetch actions');
        }else{
          const data = await response.json()
          console.log("data: " + JSON.stringify(data))
          setFetch_actions(data)
        }
      }
      
      fetch_from_db() 
    }
  },[management])

  console.log("action issue_id: " + issue_id)

  function toggle_management_mode(){
    setManagement(previous_mode => !previous_mode)
  }
  function handle_content_change_in_management_mode(action:ActionType):void{
    
    setIssue_id(action.issue_id.toString())
    setSelected_action(action)
  }
  function handle_input_change(event: ChangeEvent<HTMLInputElement | HTMLTextAreaElement>){
    const {name,value } = event.target
    //
    setInput_action({...input_action,[name]:value})
  }
  async function store_action(){
    const response = await fetch('http://localhost:8000/save_action',{
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(input_action)
     })
     if(!response.ok) {throw new Error(`HTTP error! status: ${response.status}`)}
     else {
       alert("データが格納されました。")
     }
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
          <h2 className='w-full text-center text-indigo-400'>行動管理</h2>
          <div className='flex h-screen'> 
            <div className='flex-none w-1/4 bg-gray-200 p-2'>
              <h2 className='text-lg font-bold'>行動タイトル</h2> 
              <div> 
              {fetch_actions.map((action,index)=>{
                return(
                  <button  onClick={
                    ()=>{
                    handle_content_change_in_management_mode(action)
                  
                  }
                  } key={index} className='flex flex-col gap-2 sm:gap-4 md:gap-8 hover:opacity-60 duration-200'>
                    <p>{action.title}</p>
                  </button>
                )
              })}

              </div>
            </div>
            <div className='flex flex-col gap-1 sm:gap-3 md:gap-5 py-2'>
              <p>行動タイトル：{selected_action.id?selected_action.title:selected_action.title}</p>
              <p>行動内容：</p>
              <p>{selected_action.id?selected_action.content:selected_action.content}</p>

            </div>
          </div>
        </div>
      ) : (
        // Normal mode content (e.g., input form)
        <div className={'flex flex-col gap-2 sm:gap-5 md:gap-6 justify-center items-center'}>
          <div className='flex flex-1'>
            <div className={'text-indigo-400 w-[200px] py-2'}>行動タイトル</div>
            <input type='text' name="title" value={input_action?.title} onChange={handle_input_change} className='w-full max-w-[400px] px-2 py-1 border border-solid border-indigo-400 outline-none'/>
          </div>
          <div className='text-indigo-400'>行動内容</div>
          <textarea name="content" value={input_action?.content} onChange={handle_input_change} 
          className='border border-solid border-indigo-400 w-full  h-[100px] focus:outline-none focus:ring-2 focus:ring-blue-500'
          />
          <button onClick={store_action} className='border-indigo-600 border-solid border-2 rounded-full overflow-hidden w-[150px]'>格納</button>
          
        </div>
      )}
    </div>
  )
}
