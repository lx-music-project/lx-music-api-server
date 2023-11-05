/*! 
 * @name 测试接口
 * @description 几乎软件的所有功能都可用
 * @version v1.0.0
 * @author helloplhm-qwq 
 */

// 脚本写的很简单，也不包含日志
let HOST = "http://xx" // 在这里填入你的服务端地址，需要协议，不需要加末尾的/
let KEY = "" // 在这里填入你的服务端配置的请求key

let{EVENT_NAMES,on,send,request,utils,version}=window.lx;let f=(u,o)=>{return new Promise((resolve,reject)=>{request(u,o,(err,resp)=>{if(err)return reject(err);resolve(resp);});});};let a=async (s,m,q)=>{let r=await f(`${HOST}/${s}/${m.hash?m.hash:m.songid}/${q}`,{method:"GET",headers:{"Content-Type":"application/json","User-Agent":`${window.lx.env != "mobile" ? "lx music request" : "lx music mobile request"}`, "X-Request-Key":KEY},});let{body:p}=r;if(p.code!=200||p.req.code!=200)throw new Error(p.req.message??p.message??"failed");return p.req.url;};let q=["128k"];let s=["kw","kg","tx","wy","mg"];let si={};s.forEach(i=>si[i]={name:i,type:"music",actions:["musicUrl"],qualitys:q});on(EVENT_NAMES.request,({source:t,info:m})=>{return s.includes(t)?a(t,m.musicInfo,m.type).then(data=>Promise.resolve(data)).catch(e=>Promise.reject(e)):Promise.reject('failed');});send(EVENT_NAMES.inited,{status:!0,openDevTools:!1,sources:si});