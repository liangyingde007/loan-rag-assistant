'use strict';
const form=document.querySelector('#question-form');
const question=document.querySelector('#question');
const submit=document.querySelector('#submit');
const status=document.querySelector('#status');
const answerContainer=document.querySelector('#answer');
const answerCard=document.querySelector('.answer-card');
const answerState=document.querySelector('#answer-state');
const sectionsContainer=document.querySelector('#document-sections');
const examples={early:'提前还款是否收取违约金？',term:'贷款期限如何确定？',docs:'申请需要准备哪些材料？',correction:'材料不全时怎样补正？',combined:'还款日期和还款方式在哪里看？',deduction:'扣款失败后查询什么记录？',numeric:'提前还款违约金是多少？',missing:'公积金贷款审批多久能通过？'};
const stateLabels={answered:'已找到依据',not_found:'暂无依据',insufficient:'依据不足'};
let busy=false;
let currentDocument=null;
function element(tag,className,text){const node=document.createElement(tag);if(className)node.className=className;if(text!==undefined)node.textContent=text;return node;}
function renderDocument(doc){
  currentDocument=doc;sectionsContainer.replaceChildren();
  document.querySelector('#document-meta').textContent='版本 '+doc.version+' · '+doc.sections.length+' 个章节';
  document.querySelector('.document-title div>span').textContent='演示文档 · 版本 '+doc.version;
  for(const section of doc.sections){
    const details=element('details','document-section');details.id='section-'+section.id;
    const summary=element('summary');summary.append(element('span','',String(section.position).padStart(2,'0')),document.createTextNode(section.title));
    details.append(summary,element('p','',section.text));sectionsContainer.append(details);
  }
}
async function loadDocument(){
  const controller=new AbortController();const timer=setTimeout(()=>controller.abort(),15000);
  try{const response=await fetch('/api/documents/demo-loan-v1',{signal:controller.signal});if(!response.ok)throw new Error('知识库暂时无法载入。');renderDocument(await response.json());}
  catch(error){sectionsContainer.replaceChildren(element('p','document-loading','知识库暂时无法载入。'));const retry=element('button','source-link','重新载入');retry.type='button';retry.addEventListener('click',loadDocument);sectionsContainer.append(retry);document.querySelector('#document-meta').textContent='知识库载入失败';}
  finally{clearTimeout(timer);}
}
async function locateSource(citation){
  if(!currentDocument)await loadDocument();
  const details=document.getElementById('section-'+citation.section_id);
  if(!details){status.className='status error';status.textContent='原文暂时无法定位，请重新载入知识库。';return;}
  document.querySelectorAll('.document-section.selected').forEach(node=>node.classList.remove('selected'));
  details.open=true;details.classList.add('selected');
  details.querySelector('summary').focus({preventScroll:true});
  details.scrollIntoView({behavior:window.matchMedia('(prefers-reduced-motion:reduce)').matches?'auto':'smooth',block:'center'});
}
function renderAnswer(data){
  const result=element('div');result.append(element('p','question-recap','问题：'+data.question),element('p','answer-text',data.answer));
  if(data.citations.length){
    result.append(element('h3','citation-heading','原文依据 · '+data.citations.length+' 个引用'));
    const citations=element('div','citations');
    for(const citation of data.citations){
      const card=element('article','citation');const top=element('div','citation-top');
      top.append(element('span','citation-number','['+citation.number+']'),element('strong','',citation.title),element('span','citation-version','章节 '+citation.position+' · v'+citation.version));
      const button=element('button','','定位到原文');button.type='button';button.setAttribute('aria-label','定位到原文：'+citation.title);button.addEventListener('click',()=>locateSource(citation));
      card.append(top,element('p','',citation.text),button);citations.append(card);
    }
    result.append(citations);
  }
  const trace=element('details','trace');trace.append(element('summary','','查看检索过程'));
  const list=element('ol');data.trace.forEach((step,index)=>{const item=element('li');const text=element('div');text.append(element('h4','',step.label),element('p','',step.detail));item.append(element('span','step',String(index+1).padStart(2,'0')),text);list.append(item);});trace.append(list);result.append(trace);
  answerContainer.replaceChildren(result);answerState.className='badge '+data.status;answerState.textContent=stateLabels[data.status];
  document.querySelectorAll('.document-section.selected').forEach(node=>node.classList.remove('selected'));
}
function setBusy(value){busy=value;submit.disabled=value;submit.textContent=value?'正在检索…':'检索并回答';answerCard.setAttribute('aria-busy',String(value));document.querySelectorAll('[data-example]').forEach(button=>button.disabled=value);}
async function run(){
  if(busy||!form.reportValidity())return;
  const text=question.value.trim();if(!text){status.className='status error';status.textContent='请先输入问题。';question.focus();return;}
  status.className='status';status.textContent='正在检索示例文档…';setBusy(true);
  const controller=new AbortController();const timer=setTimeout(()=>controller.abort(),20000);
  try{
    const response=await fetch('/api/chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({question:text}),signal:controller.signal});
    if(!response.ok)throw new Error(response.status===422?'问题未通过校验，请检查内容和长度。':'服务暂时不可用，请稍后重试。');
    const data=await response.json();renderAnswer(data);status.textContent=stateLabels[data.status]+'，可查看回答与原文。';
    if(window.matchMedia('(max-width:720px)').matches)answerCard.scrollIntoView({behavior:window.matchMedia('(prefers-reduced-motion:reduce)').matches?'auto':'smooth',block:'start'});
  }catch(error){status.className='status error';status.textContent=error.name==='AbortError'?'请求超时，请稍后重试。':error instanceof TypeError?'连接失败，请检查网络后重试。':error.message;}
  finally{clearTimeout(timer);setBusy(false);}
}
form.addEventListener('submit',event=>{event.preventDefault();run();});
document.querySelectorAll('[data-example]').forEach(button=>button.addEventListener('click',()=>{question.value=examples[button.dataset.example];run();}));
loadDocument();
question.value=examples.docs;
run();
