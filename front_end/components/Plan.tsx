'use client'
import React,{useState, useEffect,ChangeEvent} from 'react'
import useScrollNavigation from './useScrollNavigation'
import { PlanType } from '@/app/type/type'
import { useIssueContext } from '@/app/utils/IssueContext'

export default function Plan() {
  useScrollNavigation()
  const {issue_id, setIssue_id} = useIssueContext()

  //必须要有一个useContext，这个context包含了issue1个id，1个plan id，多个action id，1个evaluate id，1个advice id。
  //转换的时候如何？改变当前issue只能在issue的管理界面。改变当前plan也只能在plan的管理页面，但是告诉你目前的issue标题。行动页面上，可以添加很多不同的行动条目。评价页面上，要么自己写评价，要么生成评价。生成评价需要issue，plan和action的内容。最后是新的课题建议，可以自己写，也可以让AI生成。
  // 数据库的ER图得写出来。issue是主键也是其他表的外键，1对1，1对多两种关系。
  const [input_plan, setInput_plan] = useState<PlanType>({content: '',title: '',issue_id: +issue_id})
  const [fetch_plans, setFetch_plans] = useState<PlanType[]>([])
  const [management, setManagement] = useState<boolean>(false)
  const [selected_plan, setSelected_plan] = useState<PlanType>({content: '',title: '',issue_id: +issue_id})

  const [socket,setSocket] = useState<WebSocket|null>(null)
  const [response_from_gpt, setResponse_from_gpt] = useState<string>('')
  const [directive, setDirective] = useState<string>('')
  //删除会导致列表的序列与issue的序列号不同。
  //得要有一个函数让它们二者一一对应。
  //解决办法是直接返回一个受点击的选定Plan对象，里面一一对应了plan和issue的id。
  useEffect(()=>{

    if(management){
      // const response = await fetch()
      const fetch_from_db = async ()=>{
        const response = await fetch('http://localhost:8000/fetch_plans')
        if(!response.ok){
          throw new Error('Failed to fetch issues');
        }else{
          const data = await response.json()
          console.log("data: " + JSON.stringify(data))
          setFetch_plans(data)
        }
      }
      fetch_from_db() 
    }
  },[management])
  //不需要设置参数，全局共享state
  //我觉得应该用泛型
  async function store_plan(){
    //post the backend server
    const response = await fetch('http://localhost:8000/save_plan',{
     method: 'POST',
     headers: {
       'Content-Type': 'application/json'
     },
     body: JSON.stringify(input_plan)
    })
    if(!response.ok) {throw new Error(`HTTP error! status: ${response.status}`)}
    else {
      alert("データが格納されました。")
    }
  }
  
  async function store_response(){
    const response = await fetch('http://localhost:8000/save_plan_generated_from_chatGPT',{
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({"title":input_plan.title,"content":response_from_gpt,"issue_id":issue_id})
     })
     if(!response.ok) {throw new Error(`HTTP error! status: ${response.status}`)}
     else {
       alert("データが格納されました。")
     }
  }

  function handle_input_change(event: ChangeEvent<HTMLInputElement | HTMLTextAreaElement>){
    const {name,value } = event.target
    //
    setInput_plan({...input_plan,[name]:value})
  }
  function toggle_management_mode(){
    setManagement(previous_mode => !previous_mode)
  }
  function handle_content_change_in_management_mode(plan:PlanType):void{
    setIssue_id(plan.issue_id.toString())
    //查找id
    setSelected_plan(plan)
  }
// ---------------------------------------------------
  // websocket + generate
  //websocket
  
  
  async function search_issue_description_by_id(id:string){
    const url:URL = new URL("http://localhost:8000/fetch_issue_description_from_issue_id");
  url.searchParams.append("issue_id", issue_id);  
    const response = await fetch(url,{
        method: 'GET',
        headers: {
          'Content-Type': 'application/json'
        }
      })
      if(!response.ok){throw new Error('Failed to fetch issues');}else{
        const data = await response.json()
        return data.description
      }
    
  }


async function generate_plan(){
    if(socket && socket.readyState === WebSocket.OPEN){
      const issue_description:string = await search_issue_description_by_id(issue_id)
      // const issue_description= await result.split(":")[1]
      console.log("plan, issue_description = ",issue_description)
      const send_content:string = issue_description+','+directive
      console.log('send_content = ',send_content)
      setResponse_from_gpt('')
      socket.send(send_content)
    }else{
      console.error('WebSocket is not open');
    }
  }
  
  function handle_directive_change(event:ChangeEvent<HTMLInputElement>){
    setDirective(event.target.value)
  }

  useEffect(()=>{
    if (!management){
      const web_socket:WebSocket = new WebSocket('ws://localhost:8000/generate_content');
      setSocket(web_socket)
      web_socket.onopen = ()=>{
        console.log('WebSocket connection opened');
      }
      web_socket.onmessage = (event) => {
        setResponse_from_gpt(cur => cur + event.data);
      };
      
      web_socket.onerror = (error) => {
        console.error('WebSocket error:', error);
      };
  
      web_socket.onclose = () => {
        console.log('WebSocket connection closed');
      };

      return ()=>{
        web_socket.close();
      }
    }
  },[directive,management])


  return (
    <div className="p-1 sm:p-2 md:p-4  overflow-hidden w-full">
      <button
        onClick={toggle_management_mode}
        className="sm:mb-2 md:mb-4 sm:px-2 md:px-4 sm:py-1 md:py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600"
      >
        {management ? 'Exit Management' : 'Enter Management'}
      </button>

      {management ? (
        // Management mode content (e.g., menu for modifying or deleting)
        <div className='h-full w-screen'>
          <h2 className='w-full text-center text-indigo-400'>計画管理</h2>
          <div className='flex h-screen'> 
            <div className='flex-none w-1/4 bg-gray-200 p-2'>
              <h2 className='text-lg font-bold'>計画タイトル</h2> 
              <div> 
              {fetch_plans.map((plan,index)=>{
                return(
                  <button  onClick={
                    ()=>{
                    handle_content_change_in_management_mode(plan)
                  
                  }
                  } key={plan.title} className='flex flex-col gap-2 sm:gap-4 md:gap-8 hover:opacity-60 duration-200 bg-indigo-300 text-white'>
                    <p>{plan.title}</p>
                  </button>
                )
              })}

              </div>
            </div>
            <div className='flex flex-col gap-1 sm:gap-3 md:gap-5 py-2'>
              <p>計画タイトル：{selected_plan.id?selected_plan.title:input_plan.title}</p>
              <p>計画内容：</p>
              <p>{selected_plan.id?selected_plan.content:input_plan.content}</p>

            </div>
          </div>
        </div>
      ) : (
        // Normal mode content (e.g., input form)
        <div className='flex md:gap-60 '>
          <div className={'flex flex-col gap-2 sm:gap-5 md:gap-6 justify-center items-center py-2'}>
            <div className='flex flex-1'>
              <div className={'text-indigo-400 w-[200px] py-2'}>計画タイトル</div>
              <input type='text' name="title" value={input_plan?.title} onChange={handle_input_change} className='w-full max-w-[400px] px-2 py-1 border border-solid border-indigo-400 outline-none'/>
            </div>
            <div className='text-indigo-400'>計画内容</div>
            <textarea name="content" value={input_plan?.content} onChange={handle_input_change} 
            className='border border-solid border-indigo-400 w-full  h-[100px] focus:outline-none focus:ring-2 focus:ring-blue-500'
            />
            <div className='flex gap-5 sm:gap-10 md:gap-20 flex-1'>
              <button onClick={store_plan} 
              className='border-indigo-600 border-solid border-2 rounded-full overflow-hidden w-[150px]'>格納</button>
            </div>
          </div>
          <div className='flex flex-col md:gap-10 '>
            <div className='flex items-center justify-between p-2 gap-4'>
              <div className='text-indigo-400'>詳細指示：</div>
              <input onBlur={handle_directive_change} type='text' className='  px-2 py-1 border border-solid border-indigo-400 outline-none'/>
              <button onClick={generate_plan} className='hover:bg-blue-600 bg-blue-500 text-white border-indigo-600 border-solid border-2 rounded-full overflow-hidden md:p-1'>自動生成</button>
            </div>
            <div className='p-4 bg-white h-full border-t overflow-auto'>
              {response_from_gpt}
            </div>
            <div className='flex gap-5 sm:gap-10 md:gap-20 flex-1 items-center justify-center'>
              <button onClick={store_response} 
              className='border-indigo-600 border-solid border-2 rounded-full overflow-hidden w-[160px] h-[30px]'>格納</button>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

