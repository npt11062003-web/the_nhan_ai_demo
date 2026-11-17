#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
THẺ NHÂN ÁI — BẢN MỘT TỆP, 0.1.1

Yêu cầu: Python 3.10 trở lên. Không cần pip, Node hoặc tệp khác.
Trong VS Code: mở tệp này, chọn Run Python File in Terminal.
Hoặc mở Terminal tại thư mục chứa tệp: python the_nhan_ai.py
Trình duyệt tự mở sau khi máy chủ sẵn sàng. Giữ Terminal đang chạy.
Dữ liệu SQLite nằm trong thư mục nhan_ai_data cạnh tệp Python này.

Các phần mã:
  1. HTML/CSS/JavaScript cho giao diện web (nhúng ngay dưới đây).
  2. Python/SQLite cho nghiệp vụ và phân quyền (class Store).
  3. HTTP API (make_handler).
  4. Khởi động, worker mô phỏng và mở trình duyệt (main).

Chỉ là demo: danh tính, xét điều kiện, xác thực và phát hành giả lập.
Không kết nối ColdKey hoặc dịch vụ phát hành thật.
"""

# ========== 1. GIAO DIỆN NHÚNG, KHÔNG CẦN TỆP BÊN NGOÀI ==========
STATIC_FILES = {}

STATIC_FILES['index.html'] = r"""<!doctype html>
<html lang="vi">
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="theme-color" content="#146c58"><title>Thẻ Nhân Ái · Không gian điều phối</title><link rel="stylesheet" href="/style.css"><script src="/app.js" defer></script></head>
<body><div id="app"></div><div id="notice" role="status" aria-live="polite"></div><dialog id="modal"><div id="modal-content"></div></dialog></body>
</html>
"""

STATIC_FILES['style.css'] = r""":root{font-family:Inter,ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;color:#193e37;background:#f5f7f5;font-synthesis:none;--green:#146c58;--muted:#6a7f77;--line:#dfe7e1;--amber:#9b631b}*{box-sizing:border-box}body{margin:0}button,input,select,textarea{font:inherit}button,a,input,select,textarea{touch-action:manipulation}button,a{ -webkit-tap-highlight-color:transparent}button{cursor:pointer;border:1px solid var(--line);background:white;color:#284c42;border-radius:9px;padding:10px 16px;font-weight:600}button:hover{background:#e9f2ec}button:disabled{opacity:.5;cursor:wait}button.primary{background:var(--green);color:white;border-color:var(--green)}button.primary:hover{background:#105443}button.danger{color:#a24137;background:#fff4ee;border-color:#f0d3c9}button.small{padding:6px 10px;font-size:12px}a{color:var(--green)}:focus-visible{outline:3px solid #f2b962;outline-offset:3px}.layout{display:grid;grid-template-columns:238px 1fr;min-height:100vh}.sidebar{background:#fdfefb;border-right:1px solid var(--line);padding:30px 22px;display:flex;flex-direction:column;position:sticky;top:0;height:100vh}.brand{display:flex;gap:10px;align-items:center;margin:0 0 40px;font-size:20px;font-weight:750;letter-spacing:-.7px}.brand-icon{background:var(--green);color:white;width:37px;height:37px;display:grid;place-items:center;border-radius:12px;font-size:25px}.subtle{color:var(--muted);font-size:13px}.brand small{display:block;font-size:10px;letter-spacing:2px;margin-top:3px;color:var(--muted)}nav{display:flex;flex-direction:column;gap:8px}nav button{text-align:left;border:0;background:transparent;padding:13px 14px;font-size:14px}nav button.active{background:#e7f0e9;color:var(--green)}nav span{display:inline-block;width:25px;color:#799284}.side-bottom{margin-top:auto;border-top:1px solid var(--line);padding-top:20px;font-size:12px;color:var(--muted);line-height:1.7}.demo-tag{font-size:10px;letter-spacing:1.5px;font-weight:750;color:var(--amber);background:#fbefd9;border:1px solid #f1dfbb;padding:4px 7px;border-radius:5px;display:inline-block}.main{min-width:0}.topbar{padding:18px 36px;display:flex;align-items:center;justify-content:space-between;background:#fffefb;border-bottom:1px solid var(--line);gap:15px}.account{display:flex;gap:10px;align-items:center}.avatar{width:34px;height:34px;border-radius:50%;background:#e5eee6;display:grid;place-items:center;font-size:12px;font-weight:bold}.account strong{font-size:12px}.account small{display:block;font-size:10px;color:var(--muted)}.content{max-width:1240px;margin:auto;padding:32px 36px 60px}.eyebrow{font-size:11px;letter-spacing:2px;text-transform:uppercase;font-weight:700;color:var(--green);margin-bottom:10px}h1,h2,h3,p{margin-top:0}h1{font-size:29px;font-weight:650;letter-spacing:-1px;margin-bottom:10px}h2{font-size:18px;font-weight:650}h3{font-size:15px}p{line-height:1.6}.heading{display:flex;justify-content:space-between;align-items:center;gap:16px;margin-bottom:28px}.heading p{color:var(--muted);font-size:13px;margin-bottom:0}.hero{position:relative;overflow:hidden;background:#e5eee5;border:1px solid #d7e2d4;border-radius:16px;display:grid;grid-template-columns:1.2fr 1fr;gap:26px;padding:30px;margin-bottom:24px}.hero:after{content:"";position:absolute;width:360px;height:360px;border:1px solid #c4d5c6;border-radius:50%;right:-160px;top:-110px;pointer-events:none}.hero h2{font-size:25px;letter-spacing:-.6px;line-height:1.3}.hero p{font-size:13px;color:#5c7769;max-width:360px}.card-art{position:relative;aspect-ratio:1.65;background:#146c58;color:#fffcef;border-radius:16px;padding:23px;max-width:365px;width:100%;box-shadow:0 12px 28px #144f4225;overflow:hidden;justify-self:end;align-self:center}.card-art:after,.card-art:before{content:"";position:absolute;width:240px;height:240px;border:1px solid #ffffff26;border-radius:50%;right:-65px;top:35px}.card-art:before{right:-100px;top:70px}.card-top{display:flex;justify-content:space-between;font-size:11px;letter-spacing:2px}.card-art h3{font-size:24px;font-weight:450;margin:30px 0 5px;letter-spacing:1px}.card-art small{font-size:10px;color:#d0e1c7}.card-foot{display:flex;justify-content:space-between;margin-top:24px;font-size:9px;letter-spacing:1px}.stats{display:grid;grid-template-columns:repeat(4,1fr);gap:15px;margin-bottom:24px}.stat{border:1px solid var(--line);border-radius:12px;background:#fffefb;padding:20px}.stat label{display:block;font-size:12px;color:var(--muted);margin-bottom:12px}.stat b{font-size:29px;font-weight:550;letter-spacing:-1px}.stat small{color:var(--muted);font-size:11px;margin-left:8px}.panel{background:#fffefb;border:1px solid var(--line);border-radius:13px;margin-bottom:22px;overflow:hidden}.panel-head{padding:20px 22px;display:flex;align-items:center;justify-content:space-between;border-bottom:1px solid var(--line);gap:12px}.panel-head h2{margin:0}.panel-body{padding:22px}.table-wrap{overflow:auto}table{width:100%;border-collapse:collapse;text-align:left;font-size:13px;white-space:nowrap}th{font-size:10px;text-transform:uppercase;letter-spacing:1px;color:var(--muted);font-weight:600;background:#f7f9f5;padding:12px 22px}td{padding:17px 22px;border-top:1px solid #edf0e9}td strong{font-size:13px;display:block;font-weight:600}td small{display:block;color:var(--muted);font-size:11px;margin-top:4px}.badge{font-size:11px;padding:5px 9px;border-radius:6px;display:inline-block;background:#eef0ed;color:#61756d;font-weight:600}.badge.waiting,.badge.processing{background:#fff0d8;color:#98681e}.badge.completed,.badge.success{background:#e3f0e6;color:#23734e}.badge.failed{background:#fae5df;color:#a14a38}.badge.unknown{background:#eee7fa;color:#72589b}.two-col{display:grid;grid-template-columns:1.4fr 1fr;gap:22px}.benefit{display:flex;gap:14px;padding:18px 0;border-bottom:1px solid var(--line)}.benefit:last-child{border-bottom:0;padding-bottom:0}.benefit-icon{width:36px;height:36px;flex-shrink:0;border-radius:10px;background:#ecf2e6;display:grid;place-items:center;color:#75885d}.benefit h3{margin:0 0 5px}.benefit p{font-size:12px;color:var(--muted);margin:0}.flow{display:flex;gap:12px;align-items:center;margin:5px 0 22px;font-size:11px;color:var(--muted)}.flow i{height:1px;background:var(--line);flex:1}.flow .current{color:var(--green);font-weight:750}.notice-box{background:#fbf3e4;color:#856129;padding:12px 15px;border-radius:8px;font-size:12px;line-height:1.6;margin-bottom:18px;border:1px solid #eee0c5}.actions{display:flex;gap:10px;flex-wrap:wrap;align-items:center}.empty{padding:35px;text-align:center;color:var(--muted);line-height:1.8;font-size:13px}.field{display:flex;flex-direction:column;gap:7px;margin-bottom:16px;font-size:12px;font-weight:650}input,select,textarea{width:100%;border:1px solid #ccd8cd;padding:11px;border-radius:8px;background:white;color:#244b3d;font-size:14px}input[type=checkbox]{width:17px;height:17px;accent-color:var(--green);flex-shrink:0}textarea{min-height:90px;resize:vertical;line-height:1.5}.field-help{font-weight:400;color:var(--muted);font-size:11px}.form-grid{display:grid;grid-template-columns:1fr 1fr;gap:0 16px}.checkbox-row{display:flex;align-items:center;gap:12px;font-size:13px;margin:10px 0;padding:10px;border:1px solid var(--line);border-radius:8px}.checkbox-row small{display:block;color:var(--muted);font-size:11px;margin-top:4px}.checkbox-row.disabled{opacity:.5}.timeline{border-left:1px solid #d9e4db;padding-left:20px;margin-left:5px}.event{position:relative;margin-bottom:23px}.event:before{content:"";position:absolute;left:-25px;top:4px;width:9px;height:9px;border-radius:50%;background:#87a38a;border:2px solid white}.event strong{font-size:12px}.event small{display:block;font-size:11px;color:var(--muted);margin:5px 0}.event details{font-size:11px;color:#5b7667}.event pre{white-space:pre-wrap;overflow-wrap:anywhere;background:#f4f7f0;padding:10px;border-radius:8px}.mono{font-family:ui-monospace,SFMono-Regular,Consolas,monospace;font-size:12px}.details-grid{display:grid;grid-template-columns:1fr 1fr;gap:18px}.details-grid dt{color:var(--muted);font-size:11px;margin-bottom:5px}.details-grid dd{margin:0;font-size:13px}.search{display:flex;gap:10px;max-width:620px;margin-bottom:24px}#notice{position:fixed;bottom:25px;left:50%;transform:translateX(-50%);z-index:30;max-width:90vw;background:#204f40;color:white;border-radius:10px;padding:14px 20px;box-shadow:0 10px 35px #0002;font-size:13px;display:none}#notice.error{background:#9b4536}dialog{border:1px solid var(--line);border-radius:16px;width:min(680px,94vw);max-height:90vh;padding:0;color:#193e37;box-shadow:0 20px 80px #1234}dialog::backdrop{background:#153d3466;backdrop-filter:blur(3px)}.modal-title{display:flex;justify-content:space-between;align-items:center;padding:22px;border-bottom:1px solid var(--line)}.modal-title h2{margin:0}.modal-body{padding:22px}.modal-actions{display:flex;justify-content:flex-end;gap:10px;padding-top:20px}.login-page{min-height:100vh;display:grid;grid-template-columns:1fr 1fr}.login-brand{background:#e5eee5;padding:9vw 6vw;display:flex;flex-direction:column;justify-content:center}.login-brand h1{font-size:48px;max-width:460px;line-height:1.15;margin-top:25px}.login-brand p{max-width:410px;color:#61796c;font-size:14px}.login-brand .card-art{align-self:flex-start;margin-top:30px;max-width:360px}.login-form{padding:60px;display:flex;flex-direction:column;justify-content:center;max-width:580px;width:100%;margin:auto}.login-form h2{font-size:25px}.login-form .field{margin:25px 0 18px}.login-form .primary{width:100%;margin-bottom:20px}.login-form footer{font-size:11px;color:var(--muted);line-height:1.8}.projection{min-height:100vh;background:#edf3eb;padding:35px 6vw}.projection header{display:flex;justify-content:space-between;align-items:center;border-bottom:1px solid #d4dfd0;padding-bottom:25px;margin-bottom:35px;gap:15px}.projection .brand{margin:0}.projection h1{font-size:40px;margin-bottom:12px}.projection .stage{display:grid;grid-template-columns:1.1fr 1fr;gap:60px;align-items:center;margin:40px 0}.projection .card-art{max-width:480px;justify-self:center}.projection .card-art h3{font-size:32px}.connection{font-size:12px;color:#4c775b}.connection.offline{color:#a24137}.projection .stats{margin:30px 0}.projection .stat{background:#ffffff80}.projection footer{font-size:11px;color:var(--muted);text-align:center;padding-top:20px}.loading{padding:80px;text-align:center;color:var(--muted)}.error-inline{color:#a24137;font-size:13px;line-height:1.5}.public-invite{background:#eef4e8;border:1px dashed #acbda3;padding:15px;border-radius:10px;word-break:break-all;font-size:12px}.program-block{margin-bottom:22px}.program-block .actions{margin-top:20px}details summary{cursor:pointer}.text-dim{color:var(--muted)}
@media(min-width:1500px){.content{padding-top:45px}.hero{padding:40px}}
@media(max-width:1000px){.layout{grid-template-columns:200px 1fr}.sidebar{padding:25px 15px}.content{padding:25px 22px}.topbar{padding:15px 22px}.hero{grid-template-columns:1fr;padding:25px}.hero .card-art{display:none}.two-col{grid-template-columns:1fr}.stat{padding:15px}.stat small{display:block;margin:5px 0 0}.projection .stage{gap:25px}}
@media(max-width:680px){.layout{display:block}.sidebar{position:static;height:auto;padding:15px;border-right:0;border-bottom:1px solid var(--line)}.sidebar .brand{margin-bottom:15px;font-size:18px}.sidebar .brand-icon{width:30px;height:30px;font-size:20px}.sidebar nav{flex-direction:row;overflow-x:auto;gap:3px}.sidebar nav button{white-space:nowrap;font-size:12px;padding:10px}.sidebar nav span{width:19px}.side-bottom{display:none}.topbar{padding:12px 16px}.topbar>.subtle{display:none}.content{padding:24px 16px 50px}.heading{align-items:flex-start;gap:12px}h1{font-size:25px}.heading .primary{padding:10px;font-size:12px}.hero{padding:22px}.hero h2{font-size:23px}.stats{grid-template-columns:repeat(2,1fr);gap:10px}.stat b{font-size:26px}.two-col{gap:0}.panel-head{padding:17px}.panel-body{padding:17px}.panel-head h2{font-size:16px}td,th{padding:14px 17px}.form-grid{grid-template-columns:1fr}.details-grid{gap:15px}.login-page{display:block}.login-brand{padding:30px 25px}.login-brand h1{font-size:31px;margin:0 0 15px}.login-brand .brand{margin:0 0 22px}.login-brand .card-art{display:none}.login-brand p{margin:0}.login-form{padding:30px 25px}.projection{padding:22px}.projection header{align-items:flex-start}.projection .brand{font-size:17px}.projection header .demo-tag{display:none}.projection .stage{grid-template-columns:1fr;gap:20px;margin:25px 0}.projection h1{font-size:29px}.projection .card-art{max-width:400px}.flow{font-size:10px;gap:6px}.search{flex-wrap:wrap}.search input{flex:1;min-width:150px}}
@media(prefers-reduced-motion:no-preference){.panel,.hero{animation:appear .25s ease-out}@keyframes appear{from{opacity:.5;transform:translateY(5px)}to{opacity:1;transform:translateY(0)}}}

fieldset{border:1px solid var(--line);border-radius:10px;padding:15px;margin:15px 0}legend{font-size:12px;font-weight:650;color:var(--muted);padding:0 5px}.login-title{margin-top:20px}select[multiple]{min-height:80px}.card-art+ .notice-box{margin-top:20px}h3{margin-top:20px}.card-art h3{margin-top:30px}.benefit h3{margin-top:0}details .mono{overflow-wrap:anywhere}
"""

STATIC_FILES['app.js'] = r"""'use strict';
const $=s=>document.querySelector(s), $$=s=>[...document.querySelectorAll(s)];
const esc=v=>String(v??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const roleNames={preparer:'Cán bộ chuẩn bị',admin:'Quản trị demo',approver:'Người phê duyệt',viewer:'Người xem trình chiếu'};
const states={draft:'Nháp',waiting:'Chờ phê duyệt',processing:'Đang phát hành',completed:'Đã có kết quả',success:'Thành công',failed:'Lỗi phát hành',unknown:'Chưa xác định',pending:'Chưa xử lý'};
let data=null,current=null,poll=null,projectionTimer=null,busy=false,activeChallenge=null;
const badge=s=>`<span class="badge ${esc(s)}">${esc(states[s]||s)}</span>`;
const when=s=>new Date(s).toLocaleString('vi-VN',{timeZone:'Asia/Ho_Chi_Minh'});
const modal=$('#modal');
function toast(message,error=false){const n=$('#notice');n.textContent=message;n.className=error?'error':'';n.style.display='block';clearTimeout(n.timer);n.timer=setTimeout(()=>n.style.display='none',6000);}
async function api(path,body){const response=await fetch('/api'+path,{credentials:'same-origin',cache:'no-store',...(body===undefined?{}:{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(body)})});let result;try{result=await response.json();}catch{throw Error('Máy chủ chưa sẵn sàng. Vui lòng kiểm tra kết nối.');}if(!response.ok){const e=Error(result.error||'Không thể hoàn tất thao tác.');e.status=response.status;throw e;}return result;}
function cardArt(name='Kết nối những điều tốt đẹp',code='THẺ NHÂN ÁI · DEMO'){return `<div class="card-art"><div class="card-top"><span>✳ NHÂN ÁI</span><span>♡</span></div><h3>Thẻ Nhân Ái</h3><small>${esc(name)}</small><div class="card-foot"><span>${esc(code)}</span><span>MÔ PHỎNG</span></div></div>`;}
const panel=(title,body,action='')=>`<section class="panel"><div class="panel-head"><h2>${title}</h2>${action}</div>${body}</section>`;
const field=(label,name,value='',type='text',extra='')=>`<label class="field">${label}<input name="${name}" type="${type}" value="${esc(value)}" ${extra}></label>`;
const textfield=(label,name,value='',extra='')=>`<label class="field">${label}<textarea name="${name}" ${extra}>${esc(value)}</textarea></label>`;
const options=(items,value)=>items.map(x=>`<option value="${esc(x.id)}" ${String(x.id)===String(value)?'selected':''}>${esc(x.name)}</option>`).join('');
const formData=form=>Object.fromEntries(new FormData(form));
function openModal(title,body){$('#modal-content').innerHTML=`<div class="modal-title"><h2>${esc(title)}</h2><button data-action="close-modal" aria-label="Đóng">×</button></div><div class="modal-body">${body}</div>`;modal.showModal();}
function closeModal(){modal.close();activeChallenge=null;}
async function cancelAuthentication(){
 const c=activeChallenge;if(!c)return;
 await api(`/batches/${c.batch_id}/cancel-auth`,{challenge:c.challenge});
 if(activeChallenge===c)activeChallenge=null;
}
async function dismissApproval(){await cancelAuthentication();closeModal();await route();}
function cancelOnPageHide(){
 const c=activeChallenge;if(!c)return;
 // keepalive may finish after tab unload. Server expiry is the fallback if the network is down.
 fetch(`/api/batches/${c.batch_id}/cancel-auth`,{method:'POST',credentials:'same-origin',keepalive:true,
   headers:{'Content-Type':'application/json'},body:JSON.stringify({challenge:c.challenge})}).catch(()=>{});
}
const submitButtons=label=>`<div class="modal-actions"><button type="button" data-action="close-modal">Hủy</button><button class="primary" type="submit">${label}</button></div>`;
function heading(title,subtitle,action=''){return `<div class="heading"><div><div class="eyebrow">KHÔNG GIAN ĐIỀU PHỐI</div><h1>${title}</h1><p>${subtitle}</p></div>${action}</div>`;}
function stats(counts){return `<div class="stats">${[['Thẻ dự kiến',counts.total,'thẻ'],['Phát hành thành công',counts.success,'thẻ'],['Lỗi phát hành',counts.failed,'thẻ'],['Chưa xác định',counts.unknown,'thẻ']].map(([label,n,unit])=>`<div class="stat"><label>${label}</label><b>${n}</b><small>${unit}</small></div>`).join('')}</div>`;}
function shell(content,section){const a=data.account;const nav=[['overview','◫','Tổng quan'],...(a.role==='preparer'?[['programs','♧','Chương trình'],['people','♙','Người thụ hưởng']]:[]),['batches','▤',a.role==='approver'?'Hồ sơ phê duyệt':'Đợt phát hành'],['results','⊙','Tra cứu kết quả']];
$('#app').innerHTML=`<div class="layout"><aside class="sidebar"><div class="brand"><div class="brand-icon">✳</div><div>Thẻ Nhân Ái<small>CÙNG NHAU SẺ CHIA</small></div></div><div class="eyebrow">QUẢN LÝ DEMO</div><nav>${nav.map(([id,icon,label])=>`<button class="${section===id?'active':''}" data-action="nav" data-value="${id}"><span>${icon}</span>${label}</button>`).join('')}</nav><div class="side-bottom"><span class="demo-tag">KHÔNG GIAN MÔ PHỎNG</span><p>Dữ liệu hư cấu.<br>Xác thực và phát hành giả lập.</p>Phiên bản ${esc(data.version)}</div></aside><main class="main"><header class="topbar"><span class="subtle">Quản lý chương trình / ${esc(nav.find(x=>x[0]===section)?.[2]||'Chi tiết đợt')}</span><div class="account"><div class="avatar">${esc(a.name.slice(0,2).toUpperCase())}</div><div><strong>${esc(a.name)}</strong><small>${esc(roleNames[a.role])}</small></div><button class="small" data-action="switch-account">Đổi vai trò</button></div></header><div class="content">${content}</div></main></div>`;}
async function loginView(){clearInterval(poll);data=null;const [accounts,meta]=await Promise.all([api('/accounts'),api('/meta')]);$('#app').innerHTML=`<div class="login-page"><div class="login-brand"><div class="brand"><div class="brand-icon">✳</div><div>Thẻ Nhân Ái<small>CÙNG NHAU SẺ CHIA</small></div></div><div class="eyebrow">MỖI TẤM THẺ, MỘT SỰ QUAN TÂM</div><h1>Kết nối sẻ chia.<br>Trao gửi yêu thương.</h1><p>Không gian điều phối chương trình hỗ trợ, phê duyệt và theo dõi phát hành Thẻ Nhân Ái.</p>${cardArt()}</div><div class="login-form"><span class="demo-tag">BẢN DEMO ${esc(meta.version)}</span><h2 class="login-title">Chào bạn, cùng bắt đầu</h2><p class="subtle">Chọn tài khoản mẫu để trải nghiệm vai trò tương ứng.</p><form id="login-form"><label class="field">Tài khoản demo<select name="account_id">${accounts.filter(x=>x.active).map(a=>`<option value="${esc(a.id)}">${esc(a.name)} — ${esc(roleNames[a.role])}</option>`).join('')}</select></label><button class="primary" type="submit">Vào không gian điều phối →</button></form><footer>Toàn bộ người thụ hưởng, dữ liệu xét duyệt và kết quả phát hành đều là giả lập. Đây là cơ chế chọn vai trò demo, chưa phải đăng nhập định danh thật.</footer></div></div>`;}
function batchRows(items){return items.length?`<div class="table-wrap"><table><thead><tr><th>Đợt phát hành</th><th>Hồ sơ</th><th>Trạng thái</th><th>Phiên bản</th><th></th></tr></thead><tbody>${items.map(b=>`<tr><td><strong>${esc(b.name)}</strong><small>${esc(b.code)}</small></td><td>${b.people.length} người</td><td>${badge(b.state)}</td><td>v${b.version}</td><td><button class="small" data-action="open-batch" data-id="${b.id}">Xem chi tiết →</button></td></tr>`).join('')}</tbody></table></div>`:`<div class="empty">Chưa có đợt trong phạm vi tài khoản này.</div>`;}
function benefitsView(program,ids=null){const benefits=(program?.benefits||[]).filter(b=>!ids||ids.includes(b.id));return benefits.map((b,i)=>`<div class="benefit"><div class="benefit-icon">${i%2?'♡':'♧'}</div><div><h3>${esc(b.name)}</h3><p>${esc(b.limit===null?'Không giới hạn':b.limit)} ${esc(b.unit)} · ${esc(b.type)}</p><p>Điều kiện: ${esc(b.condition)}</p><p>Điểm hỗ trợ: ${esc((program.points||[]).filter(p=>b.points.includes(p.id)).map(p=>p.name).join(', ')||'Chưa liên kết')}</p></div></div>`).join('');}
function overview(){const bs=data.batches;const a=data.account;if(a.role==='viewer'){shell(heading('Màn hình trình chiếu','Chỉ xem nội dung được phép công bố.')+panel('Mở phiên trình chiếu',`<div class="panel-body"><p class="subtle">Nhập mã phiên do cán bộ chuẩn bị hoặc quản trị demo cung cấp.</p><form id="projection-form" class="search"><input name="token" required placeholder="Mã phiên trình chiếu" aria-label="Mã phiên trình chiếu"><button class="primary">Mở phiên</button></form></div>`),'overview');return;}
const waiting=bs.filter(b=>b.state==='waiting').length;const counts=data.stats;const metrics=counts?[['Chương trình',counts.program_count],['Người thụ hưởng',counts.beneficiary_count],['Đợt phát hành',counts.batch_count],['Chờ phê duyệt',counts.waiting_count]]:(a.role==='approver'?[['Đợt phát hành',bs.length],['Chờ phê duyệt',waiting]]:[['Chương trình',data.programs.length],['Người thụ hưởng',data.people.length],['Đợt phát hành',bs.length],['Chờ phê duyệt',waiting]]);let program=data.programs[0];shell(heading('Tổng quan','Mỗi tấm thẻ là một kết nối với cộng đồng.')+`<div class="hero"><div><div class="eyebrow">ĐỒNG HÀNH CÙNG CỘNG ĐỒNG</div><h2>Những điều tốt đẹp<br>bắt đầu từ sự sẻ chia.</h2><p>Theo dõi các chương trình và trao quyền lợi đến đúng người, qua từng bước phê duyệt rõ ràng.</p><button class="primary" data-action="nav" data-value="batches">${a.role==='approver'?'Xem hồ sơ chờ duyệt':'Quản lý đợt phát hành'} →</button></div>${cardArt()}</div><div class="stats">${metrics.map(([l,n])=>`<div class="stat"><label>${l}</label><b>${n}</b><small>${a.role==='approver'?'theo đợt được giao':'toàn bộ dữ liệu demo'}</small></div>`).join('')}</div>`+panel('Đợt phát hành gần đây',batchRows(bs.slice(0,5)),`<button class="small" data-action="nav" data-value="batches">Xem tất cả →</button>`)+(program?`<div class="two-col">${panel('Quyền lợi sẻ chia',`<div class="panel-body">${benefitsView(program)}</div>`)}${panel('Một quy trình, đầy đủ căn cứ',`<div class="panel-body"><div class="benefit"><div class="benefit-icon">01</div><div><h3>Chuẩn bị & trình duyệt</h3><p>Chương trình, người thụ hưởng và nội dung được lưu theo phiên bản.</p></div></div><div class="benefit"><div class="benefit-icon">02</div><div><h3>Xác nhận & phát hành</h3><p>Đúng người phê duyệt, đúng nội dung đã trình.</p></div></div><div class="benefit"><div class="benefit-icon">03</div><div><h3>Theo dõi & đối chiếu</h3><p>Kết quả từng thẻ và lịch sử xử lý rõ ràng.</p></div></div></div>`)}</div>`:''),'overview');}
function programsPage(){shell(heading('Chương trình hỗ trợ','Quản lý quyền lợi và các điểm hỗ trợ liên kết.',`<button class="primary" data-action="edit-program">+ Tạo chương trình</button>`)+data.programs.map(p=>panel(esc(p.name),`<div class="panel-body"><dl class="details-grid"><div><dt>Mã chương trình</dt><dd>${esc(p.code)}</dd></div><div><dt>Thời gian</dt><dd>${esc(p.start)} → ${esc(p.end)}</dd></div><div><dt>Địa bàn</dt><dd>${esc(p.area)}</dd></div><div><dt>Mô tả</dt><dd>${esc(p.description)}</dd></div></dl>${benefitsView(p)}<h3>Điểm hỗ trợ</h3>${p.points.map(x=>`<p class="subtle"><strong>${esc(x.name)}</strong> · ${esc(x.type)}<br>${esc(x.address)} <span class="badge">${esc(x.id)}</span></p>`).join('')}</div>`,`<button class="small" data-action="edit-program" data-id="${p.id}">Chỉnh sửa</button>`)).join(''),'programs');}
function peoplePage(){shell(heading('Người thụ hưởng','Hồ sơ hư cấu và căn cứ xét điều kiện giả lập.',`<button class="primary" data-action="edit-person">+ Tạo hồ sơ</button>`)+panel('Danh sách hồ sơ',data.people.length?`<div class="table-wrap"><table><thead><tr><th>Người thụ hưởng</th><th>Chương trình</th><th>Điều kiện giả lập</th><th></th></tr></thead><tbody>${data.people.map(p=>`<tr><td><strong>${esc(p.name)}</strong><small>${esc(p.code)} · ${esc(p.area)}</small></td><td>${esc(data.programs.find(x=>x.id===p.program_id)?.name)}</td><td>${badge(p.eligible?'success':'pending')}<small>${p.eligible?'Đủ điều kiện':'Chưa đủ điều kiện'}</small></td><td><button class="small" data-action="edit-person" data-id="${p.id}">Xem / sửa</button></td></tr>`).join('')}</tbody></table></div>`:'<div class="empty">Chưa có hồ sơ. Hãy tạo chương trình trước.</div>'),'people');}
function batchesPage(){shell(heading(data.account.role==='approver'?'Hồ sơ phê duyệt':'Đợt phát hành','Lập hồ sơ, theo dõi phê duyệt và kết quả phát hành.',data.account.role==='preparer'?`<button class="primary" data-action="edit-batch">+ Lập đợt mới</button>`:'')+panel('Tất cả đợt trong phạm vi',batchRows(data.batches)),'batches');}
function resultView(r){if(!r)return '<div class="empty">Chưa có yêu cầu phát hành. Quyết định phê duyệt và kết quả phát hành được ghi nhận riêng.</div>';return `<div class="panel-body"><div class="notice-box">Đã ghi quyết định phê duyệt · Xác thực mô phỏng · v${r.version}<br>Mã yêu cầu: <strong class="mono">${esc(r.id)}</strong> · ${when(r.created)}<br>${r.state==='processing'?'Đang xử lý; có thể đóng và mở lại để tra cứu.':'Đã hoàn tất lượt xử lý. Hãy đối chiếu từng trạng thái bên dưới; chưa xác định vẫn là chưa xác định.'}</div>${stats(r.counts)}${r.counts.pending?`<p class="subtle">Còn ${r.counts.pending} thẻ chưa xử lý.</p>`:''}</div><div class="table-wrap"><table><thead><tr><th>Người thụ hưởng</th><th>Mã thẻ dự kiến</th><th>Kết quả</th><th></th></tr></thead><tbody>${r.cards.map(c=>{const p=r.snapshot.people.find(p=>p.id===c.person_id);return `<tr><td><strong>${esc(p?.name)}</strong><small>${esc(p?.code)}</small></td><td class="mono">${esc(c.id)}</td><td>${badge(c.status)}${c.reason?`<small>${esc(c.reason)}</small>`:''}</td><td>${cardActions(c)}</td></tr>`;}).join('')}</tbody></table></div>`;}
function cardActions(c){
 if(c.status==='success')return `<button class="small" data-action="open-card" data-value="${esc(c.id)}">Xem thẻ →</button>`;
 if(data?.account.role!=='approver')return '';
 if(c.status==='failed')return `<button class="small" data-action="retry-card" data-value="${esc(c.id)}" data-revision="${c.revision}">Thử lại thẻ lỗi</button>`;
 if(c.status==='unknown')return `<button class="small" data-action="reconcile-card" data-value="${esc(c.id)}" data-revision="${c.revision}">Đối chiếu trước khi xử lý</button>`;
 return '';
}
function newOperationKey(){const bytes=new Uint8Array(16);crypto.getRandomValues(bytes);return Array.from(bytes,x=>x.toString(16).padStart(2,'0')).join('');}
function cardOperationModal(cid,revision,kind){
 const reconcile=kind==='reconcile';
 openModal(reconcile?'Đối chiếu kết quả chưa xác định':'Thử lại phát hành thẻ lỗi',`<form id="card-operation-form" data-card="${esc(cid)}" data-revision="${revision}" data-kind="${kind}" data-key="${newOperationKey()}">
 <div class="notice-box">${reconcile?'ĐỐI CHIẾU MÔ PHỎNG · Không gửi lệnh phát hành mới. Chỉ cho thử lại sau khi xác nhận chưa phát hành.':'THỬ LẠI MÔ PHỎNG · Giữ nguyên mã thẻ, yêu cầu và nội dung đã được duyệt. Không tạo thêm thẻ.'}</div>
 <p>Mã thẻ: <strong class="mono">${esc(cid)}</strong></p>
 <label class="field">${reconcile?'Kết quả đối chiếu giả lập':'Kịch bản cho lần thử lại'}<select name="outcome">
 ${reconcile?'<option value="unknown">Chưa đủ căn cứ — giữ chưa xác định</option><option value="success">Xác nhận đã phát hành</option><option value="failed">Xác nhận chưa phát hành — cho phép thử lại</option>':'<option value="success">Phát hành thành công</option><option value="failed">Vẫn lỗi phát hành</option><option value="unknown">Mất phản hồi — chưa xác định</option>'}</select></label>
 ${reconcile?textfield('Căn cứ / mã đối chiếu giả lập *','evidence','','required maxlength="2000"')+'<label class="checkbox-row"><input type="checkbox" name="confirmed" required>Tôi xác nhận đã kiểm tra căn cứ đối chiếu mô phỏng.</label>':''}
 ${submitButtons(reconcile?'Lưu kết quả đối chiếu':'Ghi yêu cầu thử lại')}</form>`);
}
const snapshotNotice='<div class="notice-box"><strong>Đang xem bản chụp tại thời điểm trình.</strong> Thay đổi chương trình hoặc hồ sơ hiện tại không cập nhật nội dung này. Muốn áp dụng dữ liệu mới: thu hồi về nháp → cập nhật → trình lại. Bản demo xét điều kiện tại thời điểm trình, chưa tái xét điều kiện mới nhất ngay trước phát hành.</div>';
async function batchDetail(id,quiet=false){const b=await api('/batches/'+id);if(quiet&&(modal.open||JSON.stringify(current)===JSON.stringify(b)))return;current=b;const snap=b.snapshot||b.draft;const program=snap.program;let actions='';const role=data.account.role;
if(b.state==='draft'&&role==='preparer')actions=`<button data-action="edit-batch" data-id="${b.id}">Sửa đợt</button><button class="primary" data-action="submit-batch" data-id="${b.id}">Trình phê duyệt →</button>`;
if(b.state==='waiting'&&role==='preparer')actions=`<button data-action="withdraw" data-id="${b.id}">Thu hồi về nháp</button>`;
if(b.state==='waiting'&&role==='approver')actions=`<button class="primary" data-action="begin-approval" data-id="${b.id}">Xem & xác nhận phê duyệt →</button>`;
if(b.snapshot&&['admin','preparer'].includes(role))actions+=`<button data-action="create-projection" data-id="${b.id}">Mở trình chiếu ↗</button>`;
const people=snap.people;const approver=data.accounts.find(a=>a.id===b.approver);
shell(heading(esc(b.name),`${esc(b.code)} · Phiên bản ${b.version}`,`<button class="small" data-action="nav" data-value="batches">← Danh sách</button>`)+`<div class="flow"><span class="${b.state==='draft'?'current':''}">01 Chuẩn bị</span><i></i><span class="${b.state==='waiting'?'current':''}">02 Phê duyệt</span><i></i><span class="${b.state==='processing'?'current':''}">03 Phát hành</span><i></i><span class="${b.state==='completed'?'current':''}">04 Kết quả</span></div>`+panel('Hồ sơ đợt',`<div class="panel-body"><div class="actions">${badge(b.state)}<span class="demo-tag">DỮ LIỆU & XÁC THỰC MÔ PHỎNG</span></div><dl class="details-grid"><div><dt>Chương trình</dt><dd>${esc(program.name)}</dd></div><div><dt>Địa bàn</dt><dd>${esc(program.area)}</dd></div><div><dt>Thời hạn quyền lợi</dt><dd>${esc(program.start)} → ${esc(program.end)}</dd></div><div><dt>Người phê duyệt</dt><dd>${esc(approver?.name||b.approver||'Chưa thiết lập')}</dd></div><div><dt>Số lượng dự kiến</dt><dd>${people.length} thẻ / ${people.length} người</dd></div><div><dt>Nội dung trình</dt><dd>${b.snapshot?'Bản chụp đã khóa · v'+b.version:'Đang soạn thảo'}</dd></div></dl>${b.digest?`<details class="subtle"><summary>Dấu đối chiếu phiên bản</summary><p class="mono">${esc(b.digest)}</p></details>`:''}<div class="actions">${actions}</div></div>`,b.state==='draft'&&role==='admin'?`<button class="small" data-action="configure" data-id="${b.id}">Thiết lập người duyệt</button>`:'')+
(b.snapshot?snapshotNotice:'')+
(b.state==='draft'&&role==='preparer'?'<div class="notice-box">Sau khi lưu đợt, đổi sang vai trò Quản trị demo để thiết lập người phê duyệt. Sau đó quay lại Cán bộ chuẩn bị để trình.</div>':'')+
`<div class="two-col">${panel('Danh sách thẻ dự kiến',`<div class="table-wrap"><table><thead><tr><th>Hồ sơ</th><th>Quyền lợi áp dụng</th></tr></thead><tbody>${people.map(p=>`<tr><td><strong>${esc(p.name)}</strong><small>${esc(p.code)} · ${p.eligible?'Đủ điều kiện giả lập':'Chưa đủ điều kiện'}</small><small>${esc(p.basis)}</small></td><td>${esc(program.benefits.filter(x=>p.benefit_ids.includes(x.id)).map(x=>x.name).join(', '))}</td></tr>`).join('')}</tbody></table></div>`)}${panel('Quyền lợi trong hồ sơ',`<div class="panel-body">${benefitsView(program)}</div>`)}</div>`+
panel('Kết quả phát hành',resultView(b.result),b.result?`<button class="small" data-action="refresh-detail">↻ Cập nhật</button>`:'')+
panel('Lịch sử xử lý',`<div class="panel-body"><div class="timeline">${b.history.map(e=>`<div class="event"><strong>${esc(e.action)}</strong><small>${when(e.created)} · ${esc(e.actor)}</small><details><summary>Xem căn cứ sự kiện</summary><pre>${esc(JSON.stringify(e.details,null,2))}</pre></details></div>`).join('')}</div></div>`),'batches');}
function resultsPage(){shell(heading('Tra cứu kết quả','Tìm theo mã yêu cầu hoặc mở đợt phát hành bên dưới.')+`<form class="search" id="lookup-form"><input name="request_id" aria-label="Mã yêu cầu" placeholder="Nhập mã yêu cầu YC-…" required><button class="primary">Tra cứu</button></form><div id="lookup-result"></div>`+panel('Tra cứu theo đợt',batchRows(data.batches)),'results');}
function programModal(id){const p=data.programs.find(x=>x.id===Number(id))||{benefits:[],points:[]};openModal(id?'Chỉnh sửa chương trình':'Tạo chương trình',`<div class="notice-box">Trường có dấu * là bắt buộc. Thay đổi chương trình không thay đổi bản hồ sơ đã trình hoặc quyền lợi đã phát hành.</div><form id="program-form" data-id="${id||''}"><div class="form-grid">${field('Mã chương trình *','code',p.code,'text','required')}${field('Tên chương trình *','name',p.name,'text','required')}${field('Địa bàn *','area',p.area,'text','required')}${field('Ngày bắt đầu *','start',p.start,'date','required')}${field('Ngày kết thúc *','end',p.end,'date','required')}</div>${textfield('Mô tả','description',p.description)}<h3>Điểm hỗ trợ</h3><div id="point-rows">${p.points.map(pointRow).join('')}</div><button type="button" class="small" data-action="add-point">+ Thêm điểm hỗ trợ</button><h3>Quyền lợi</h3><div id="benefit-rows">${p.benefits.map(b=>benefitRow(b,p.points)).join('')}</div><button type="button" class="small" data-action="add-benefit">+ Thêm quyền lợi</button>${submitButtons('Lưu chương trình')}</form>`);}
function pointRow(p={}){return `<fieldset class="point-row"><legend>Điểm hỗ trợ</legend><div class="form-grid">${field('Mã điểm *','point_id',p.id,'text','required')}${field('Tên điểm *','point_name',p.name,'text','required')}${field('Loại *','point_type',p.type,'text','required')}${field('Địa chỉ minh họa *','point_address',p.address,'text','required')}</div><button class="small danger" type="button" data-action="remove-row">Xóa điểm</button></fieldset>`;}
function benefitRow(b={},points=[]){return `<fieldset class="benefit-row"><legend>Quyền lợi</legend><div class="form-grid">${field('Mã quyền lợi *','benefit_id',b.id,'text','required')}${field('Tên quyền lợi *','benefit_name',b.name,'text','required')}${field('Loại hỗ trợ *','benefit_type',b.type,'text','required')}${field('Hạn mức (để trống nếu không giới hạn)','benefit_limit',b.limit,'number','min="0.01" step="any"')}${field('Đơn vị tính *','benefit_unit',b.unit,'text','required')}${field('Điều kiện *','benefit_condition',b.condition,'text','required')}</div><label class="field">Điểm hỗ trợ liên kết (có thể chọn nhiều)<select name="benefit_points" multiple>${points.map(p=>`<option value="${esc(p.id)}" ${(b.points||[]).includes(p.id)?'selected':''}>${esc(p.name)} (${esc(p.id)})</option>`).join('')}</select></label><button type="button" class="small danger" data-action="remove-row">Xóa quyền lợi</button></fieldset>`;}
function pointsFromForm(){return $$('.point-row').map(row=>({id:row.querySelector('[name=point_id]').value.trim(),name:row.querySelector('[name=point_name]').value.trim(),type:row.querySelector('[name=point_type]').value.trim(),address:row.querySelector('[name=point_address]').value.trim()}));}
function syncPointOptions(){const pts=pointsFromForm();$$('[name=benefit_points]').forEach(select=>{const chosen=[...select.selectedOptions].map(o=>o.value);select.innerHTML=pts.map(p=>`<option value="${esc(p.id)}" ${chosen.includes(p.id)?'selected':''}>${esc(p.name)} (${esc(p.id)})</option>`).join('');});}
function personModal(id){if(!data.programs.length){toast('Hãy tạo chương trình trước.',true);return;}const p=data.people.find(p=>p.id===Number(id))||{program_id:data.programs[0].id,eligible:false,benefit_ids:[]};openModal(id?'Hồ sơ người thụ hưởng':'Tạo hồ sơ mẫu',`<form id="person-form" data-id="${id||''}"><div class="notice-box">Chỉ nhập danh tính hư cấu và căn cứ giả lập.</div><div class="form-grid">${field('Mã hồ sơ *','code',p.code,'text','required')}${field('Họ tên hư cấu *','name',p.name,'text','required')}${field('Địa bàn *','area',p.area,'text','required')}<label class="field">Chương trình *<select name="program_id" id="person-program">${options(data.programs,p.program_id)}</select></label></div><div id="person-benefits">${personBenefits(p.program_id,p.benefit_ids)}</div><label class="checkbox-row"><input type="checkbox" name="eligible" ${p.eligible?'checked':''}> Đủ điều kiện giả lập</label>${textfield('Căn cứ giả lập *','basis',p.basis,'required')}${submitButtons('Lưu hồ sơ')}</form>`);}
function personBenefits(pid,selected=[]){return `<h3>Nhóm quyền lợi *</h3>${(data.programs.find(p=>p.id===Number(pid))?.benefits||[]).map(b=>`<label class="checkbox-row"><input type="checkbox" name="benefit_ids" value="${esc(b.id)}" ${selected.includes(b.id)?'checked':''}>${esc(b.name)}</label>`).join('')}`;}
async function batchModal(id){if(!data.programs.length){toast('Hãy tạo chương trình trước.',true);return;}const b=id?await api('/batches/'+id):{program_id:data.programs[0].id,people:[]};openModal(id?'Chỉnh sửa đợt nháp':'Lập đợt phát hành',`<form id="batch-form" data-id="${id||''}" data-version="${b.version||0}"><div class="form-grid">${field('Mã đợt *','code',b.code,'text','required')}${field('Tên đợt *','name',b.name,'text','required')}</div><label class="field">Chương trình *<select name="program_id" id="batch-program">${options(data.programs,b.program_id)}</select></label><h3>Chọn người thụ hưởng</h3><p class="subtle">Một người một thẻ trong cùng chương trình. Hồ sơ chưa đủ điều kiện không được chọn.</p><div id="batch-people">${batchPeople(b.program_id,b.people)}</div>${submitButtons('Lưu đợt nháp')}</form>`);}
function batchPeople(pid,selected=[]){const people=data.people.filter(p=>p.program_id===Number(pid));return people.length?people.map(p=>`<label class="checkbox-row ${!p.eligible?'disabled':''}"><input type="checkbox" name="people" value="${p.id}" ${selected.includes(p.id)&&p.eligible?'checked':''} ${!p.eligible?'disabled':''}><span>${esc(p.name)}<small>${esc(p.code)} · ${p.eligible?'Đủ điều kiện giả lập':'Chưa đủ điều kiện'}</small></span></label>`).join(''):'<div class="empty">Chưa có hồ sơ trong chương trình.</div>';}
function configModal(){openModal('Thiết lập người phê duyệt',`<form id="config-form"><label class="field">Tài khoản phê duyệt<select name="approver" required><option value="">Chọn tài khoản</option>${options(data.accounts.filter(x=>x.role==='approver'&&x.active),current.approver)}</select></label><label class="field">Phương án xác thực<select name="auth"><option value="simulation">Mô phỏng — không sử dụng ColdKey thật</option></select></label><p class="subtle">Phạm vi: chỉ tài khoản này được phê duyệt đợt ${esc(current.code)} ở phiên bản còn hiệu lực.</p>${submitButtons('Lưu cấu hình')}</form>`);}
async function beginApproval(){const bid=current.id,version=current.version,routeHash=location.hash;const c=await api(`/batches/${bid}/challenge`,{version});if(location.hash!==routeHash||current?.id!==bid){await api(`/batches/${bid}/cancel-auth`,{challenge:c.challenge});return;}activeChallenge={...c,batch_id:bid,routeHash};openModal('Xác nhận quyết định phát hành',`<form id="approval-form"><div class="notice-box">XÁC THỰC MÔ PHỎNG · Không kết nối ColdKey thật.<br>Phiên xác nhận có hiệu lực 5 phút.</div>${snapshotNotice}<h3>${esc(c.snapshot.name)}</h3><p>${esc(c.snapshot.program.name)} · v${c.version}<br><strong>${c.snapshot.people.length} thẻ dự kiến</strong> · ${esc(c.snapshot.program.start)} → ${esc(c.snapshot.program.end)}</p><details><summary>Đối chiếu nội dung được xác nhận</summary><div>${benefitsView(c.snapshot.program)}</div><p class="mono">${esc(c.digest)}</p></details><label class="checkbox-row"><input type="checkbox" name="confirm" required>Tôi đã xem hồ sơ và xác nhận quyết định phát hành.</label><label class="field">Kết quả xác thực mô phỏng<select name="authentication"><option value="success">Xác thực thành công (giả lập)</option><option value="fail">Xác thực thất bại (giả lập)</option></select></label><label class="field">Kịch bản phát hành demo<select name="mode"><option value="success">Tất cả thành công</option><option value="partial">Xen kẽ thành công / lỗi / chưa xác định</option><option value="failure">Tất cả lỗi phát hành</option></select></label><div class="modal-actions"><button type="button" data-action="cancel-approval">Hủy xác thực</button><button type="submit" class="primary">Xác thực & ghi quyết định</button></div></form>`);}
async function showCard(cid){const c=await api('/cards/'+encodeURIComponent(cid));openModal('Thẻ Nhân Ái · Đã phát hành',`${cardArt(c.person.name,c.card.id)}<div class="notice-box">THẺ MÔ PHỎNG · ${esc(c.batch.code)} · Hồ sơ đã phê duyệt v${c.version}. Xem thẻ không trừ quyền lợi.</div><h3>${esc(c.person.name)}</h3><p class="subtle">${esc(c.program.name)}<br>Hiệu lực ${esc(c.program.start)} → ${esc(c.program.end)}</p>${benefitsView({...c.program,benefits:c.benefits,points:c.points})}<h3>Điểm hỗ trợ</h3>${c.points.map(p=>`<p class="subtle"><strong>${esc(p.name)}</strong><br>${esc(p.address)}</p>`).join('')}`);}
async function projectionPage(token){clearInterval(poll);clearInterval(projectionTimer);let inFlight=false;let previous=null;
async function update(){if(inFlight)return;inFlight=true;try{const p=await api('/public/'+encodeURIComponent(token));if(!location.hash.startsWith('#screen/'))return;if(JSON.stringify(previous)===JSON.stringify(p)){const c=$('#connection');if(c){c.className='connection';c.textContent='● Đã đồng bộ · '+new Date().toLocaleTimeString('vi-VN');}}else{previous=p;renderProjection(p);}}catch(e){if(!location.hash.startsWith('#screen/'))return;if(!previous||e.status===404||e.status===409){$('#app').innerHTML=`<div class="projection"><h1>Không thể hiển thị phiên</h1><p>${esc(e.message)}</p><button data-action="nav" data-value="overview">Về ứng dụng</button></div>`;previous=null;}else{const c=$('#connection');if(c){c.className='connection offline';c.textContent='● Mất kết nối · Nội dung cũ, đang thử kết nối lại';}}}finally{inFlight=false;}}
await update();projectionTimer=setInterval(update,2000);}
function renderProjection(p){const c=p.counts;const status=p.authenticating?'Đang xác thực mô phỏng':states[p.state];const headline=p.state==='completed'?(c.unknown||c.failed?'Kết quả cần đối chiếu':'Đã phát hành thành công'):status;$('#app').innerHTML=`<main class="projection"><header><div class="brand"><div class="brand-icon">✳</div><div>Thẻ Nhân Ái<small>CÙNG NHAU SẺ CHIA</small></div></div><span class="demo-tag">PHIÊN TRÌNH CHIẾU · MÔ PHỎNG</span><span id="connection" class="connection">● Đã đồng bộ · ${new Date().toLocaleTimeString('vi-VN')}</span></header><div class="eyebrow">${esc(p.program)}</div><div class="stage"><div><h1>${esc(p.name)}</h1><p class="subtle">${esc(p.area)} · v${p.version}</p><h2>${esc(headline)}</h2><p class="subtle">${p.state==='completed'?'Quyết định đã ghi nhận. Kết quả phát hành hiển thị theo từng nhóm trạng thái.':'Theo dõi cùng một đợt trên điện thoại và màn hình trình chiếu.'}</p>${badge(p.state)}</div>${cardArt('Thẻ đại diện · không chứa danh tính')}</div>${stats(c)}${c.pending?`<p class="subtle">${c.pending} thẻ đang chờ xử lý.</p>`:''}<div class="two-col">${panel('Quyền lợi đồng hành',`<div class="panel-body">${p.benefits.map(b=>`<div class="benefit"><div class="benefit-icon">♡</div><div><h3>${esc(b.name)}</h3><p>${esc(b.limit??'Không giới hạn')} ${esc(b.unit)} · ${esc(b.condition)}</p></div></div>`).join('')}<p class="subtle">Thời hạn: ${esc(p.start)} → ${esc(p.end)}</p></div>`)}${panel('Các điểm hỗ trợ',`<div class="panel-body">${p.points.map(x=>`<div class="benefit"><div class="benefit-icon">⌖</div><div><h3>${esc(x.name)}</h3><p>${esc(x.type)}</p></div></div>`).join('')}</div>`)}</div><footer>Dữ liệu công bố giới hạn · Không hiển thị danh tính người thụ hưởng · Xác thực và phát hành giả lập</footer></main>`;}
async function route(){try{await cancelAuthentication();}catch(e){toast('Chưa hủy được phiên xác thực. Giữ màn hình hiện tại và thử lại khi có kết nối. '+e.message,true);return;}if(modal.open)closeModal();clearInterval(poll);clearInterval(projectionTimer);current=null;const hash=location.hash.slice(1)||'overview';if(hash.startsWith('screen/'))return projectionPage(hash.slice(7));try{data=await api('/bootstrap');const [page,id]=hash.split('/');if(page==='batch'&&/^\d+$/.test(id)){await batchDetail(Number(id));poll=setInterval(async()=>{if(!modal.open&&!busy&&document.visibilityState==='visible'){try{await batchDetail(Number(id),true);}catch(e){clearInterval(poll);toast(e.message,true);}}},2500);return;}
if(data.account.role==='viewer'&&page!=='overview'){location.hash='overview';return;}
if(['programs','people'].includes(page)&&data.account.role!=='preparer'){location.hash='overview';return;}
({overview,programs:programsPage,people:peoplePage,batches:batchesPage,results:resultsPage}[page]||overview)();}catch(e){if(e.status===401)await loginView();else $('#app').innerHTML=`<div class="loading"><p>${esc(e.message)}</p><button data-action="reload">Thử lại</button></div>`;}}
async function mutation(path,body,message){const r=await api(path,body);closeModal();toast(message);await route();return r;}
document.addEventListener('click',async event=>{const b=event.target.closest('[data-action]');if(!b||busy)return;const action=b.dataset.action,id=b.dataset.id,value=b.dataset.value;try{busy=true;b.disabled=true;
switch(action){case 'nav':await cancelAuthentication();closeModal();location.hash=value;break;case 'reload':await route();break;case 'close-modal':if(activeChallenge)await dismissApproval();else closeModal();break;case 'switch-account':await cancelAuthentication();await api('/logout',{});closeModal();location.hash='overview';await loginView();break;case 'open-batch':await cancelAuthentication();closeModal();location.hash='batch/'+id;break;case 'edit-program':programModal(id);break;case 'edit-person':personModal(id);break;case 'edit-batch':await batchModal(id);break;case 'add-point':$('#point-rows').insertAdjacentHTML('beforeend',pointRow());break;case 'add-benefit':$('#benefit-rows').insertAdjacentHTML('beforeend',benefitRow({},pointsFromForm()));break;case 'remove-row':{const row=b.closest('fieldset');row.remove();syncPointOptions();break;}case 'configure':configModal();break;case 'submit-batch':await mutation(`/batches/${id}/submit`,{version:current.version},'Đã trình hồ sơ phê duyệt.');break;case 'withdraw':await mutation(`/batches/${id}/withdraw`,{version:current.version},'Đã thu hồi, tạo phiên bản nháp mới.');break;case 'refresh-detail':await batchDetail(current.id);break;case 'begin-approval':await beginApproval();break;case 'cancel-approval':await dismissApproval();toast('Đã hủy phiên xác thực. Không phát hành thẻ.');break;case 'retry-card':cardOperationModal(value,Number(b.dataset.revision),'retry');break;case 'reconcile-card':cardOperationModal(value,Number(b.dataset.revision),'reconcile');break;case 'open-card':await showCard(value);break;case 'create-projection':{const p=await api(`/batches/${id}/projection`,{});const url=location.origin+location.pathname+'#screen/'+p.token;openModal('Phiên trình chiếu đã sẵn sàng',`<p class="subtle">Liên kết chỉ công bố tên chương trình, quyền lợi, điểm hỗ trợ và số tổng hợp. Mở trên thiết bị cùng truy cập được máy chủ demo.</p><div class="public-invite"><a href="${esc(url)}" target="_blank" rel="noopener">Mở màn hình trình chiếu ↗</a><p>${esc(url)}</p><strong>Mã phiên:</strong> ${esc(p.token)}</div>`);break;}}
}catch(e){toast(e.message,true);}finally{busy=false;if(b.isConnected)b.disabled=false;}});
document.addEventListener('change',event=>{if(event.target.id==='person-program')$('#person-benefits').innerHTML=personBenefits(event.target.value);if(event.target.id==='batch-program')$('#batch-people').innerHTML=batchPeople(event.target.value);if(event.target.closest('.point-row'))syncPointOptions();});
document.addEventListener('submit',async event=>{const form=event.target;if(!form.id)return;event.preventDefault();if(busy)return;busy=true;const buttons=[...form.querySelectorAll('button')];buttons.forEach(b=>b.disabled=true);try{const f=formData(form),id=form.dataset.id;
switch(form.id){case 'login-form':await api('/login',f);location.hash='overview';await route();break;case 'program-form':{const body={...f,points:pointsFromForm(),benefits:$$('.benefit-row').map(row=>{const v=n=>row.querySelector(`[name=benefit_${n}]`).value.trim();return {id:v('id'),name:v('name'),type:v('type'),limit:v('limit')===''?null:Number(v('limit')),unit:v('unit'),condition:v('condition'),points:[...row.querySelector('select').selectedOptions].map(o=>o.value)};})};await mutation('/programs'+(id?'/'+id:''),body,'Đã lưu chương trình.');break;}
case 'person-form':await mutation('/people'+(id?'/'+id:''),{...f,program_id:Number(f.program_id),eligible:form.elements.eligible.checked,benefit_ids:[...new FormData(form).getAll('benefit_ids')]},'Đã lưu hồ sơ mẫu.');break;
case 'batch-form':{const r=await mutation('/batches'+(id?'/'+id:''),{...f,program_id:Number(f.program_id),version:Number(form.dataset.version),people:new FormData(form).getAll('people').map(Number)},'Đã lưu đợt nháp.');location.hash='batch/'+r.id;break;}
case 'config-form':await mutation(`/batches/${current.id}/configure`,{...f,version:current.version},'Đã lưu cấu hình phê duyệt.');break;
case 'approval-form':{const r=await api(`/batches/${activeChallenge.batch_id}/approve`,{challenge:activeChallenge.challenge,authentication:f.authentication,mode:f.mode});closeModal();toast(r.request_id?'Đã ghi quyết định. Mã yêu cầu: '+r.request_id:'Xác thực thất bại; không phát hành thẻ.');await route();break;}
case 'card-operation-form':{const payload={operation_key:form.dataset.key,revision:Number(form.dataset.revision),outcome:f.outcome};if(form.dataset.kind==='reconcile'){payload.evidence=f.evidence;payload.confirmed=form.elements.confirmed.checked;}const r=await api(`/cards/${encodeURIComponent(form.dataset.card)}/${form.dataset.kind}`,payload);closeModal();toast(form.dataset.kind==='reconcile'?'Đã ghi kết quả đối chiếu mô phỏng.':'Đã ghi nhận lần thử lại; không tạo thẻ mới.');if(location.hash==='results'||location.hash==='#results'){const result=await api('/requests/'+encodeURIComponent(r.request_id));$('#lookup-result').innerHTML=panel('Kết quả tra cứu',resultView(result));}else{await route();}break;}
case 'lookup-form':{try{const r=await api('/requests/'+encodeURIComponent(f.request_id.trim()));$('#lookup-result').innerHTML=panel('Kết quả tra cứu',resultView(r));}catch(e){$('#lookup-result').innerHTML=`<p class="error-inline">${esc(e.message)}</p>`;}break;}
case 'projection-form':location.hash='screen/'+encodeURIComponent(f.token.trim());break;}
}catch(e){toast(e.message,true);}finally{busy=false;buttons.forEach(b=>{if(b.isConnected)b.disabled=false;});}});
modal.addEventListener('cancel',event=>{if(activeChallenge){event.preventDefault();dismissApproval().catch(e=>{toast(e.message,true);});}});
window.addEventListener('hashchange',()=>route());
window.addEventListener('pagehide',cancelOnPageHide);
window.addEventListener('pageshow',event=>{if(event.persisted)route();});
document.addEventListener('visibilitychange',async()=>{if(document.visibilityState==='hidden'&&activeChallenge){try{await cancelAuthentication();closeModal();}catch(e){toast('Chưa hủy được xác thực: '+e.message,true);}}});
window.addEventListener('online',()=>{if(!location.hash.startsWith('#screen/'))toast('Đã kết nối lại. Tra cứu trạng thái trước khi thao tác tiếp.');});
window.addEventListener('offline',()=>toast('Mất kết nối. Không gửi lại quyết định; hãy tra cứu sau khi kết nối lại.',true));
route();
"""

# ========== 2. PYTHON: NGHIỆP VỤ VÀ SQLITE ==========
"""Thẻ Nhân Ái 0.1.1 — demo domain; Python standard library only."""
import contextlib
import hashlib
import json
import math
import secrets
import sqlite3
import time
from datetime import datetime, timezone

VERSION = '0.1.1'
ROLES = {'preparer': 'Cán bộ chuẩn bị', 'admin': 'Quản trị demo', 'approver': 'Người phê duyệt', 'viewer': 'Người xem trình chiếu'}

class Problem(Exception):
    def __init__(self, message, status=400):
        self.message, self.status = message, status

def now():
    return datetime.now(timezone.utc).isoformat()

def dump(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True)

def need(condition, message, status=400):
    if not condition:
        raise Problem(message, status)

def required(data, *keys):
    for key in keys:
        need(isinstance(data.get(key), str) and bool(data[key].strip()), f'Thiếu trường bắt buộc: {key}.')
        need(len(data[key]) <= 2000, f'Trường {key} quá dài.')

def positive_id(value):
    need(type(value) is int and value > 0, 'Mã đối tượng không hợp lệ.')
    return value

class Store:
    def __init__(self, path):
        self.path = str(path)
        with self.db() as db:
            db.executescript('''
            CREATE TABLE IF NOT EXISTS accounts(id TEXT PRIMARY KEY, name TEXT NOT NULL, role TEXT NOT NULL, active INTEGER NOT NULL DEFAULT 1);
            CREATE TABLE IF NOT EXISTS sessions(token TEXT PRIMARY KEY, account_id TEXT NOT NULL REFERENCES accounts(id), expires REAL NOT NULL);
            CREATE TABLE IF NOT EXISTS programs(id INTEGER PRIMARY KEY, code TEXT UNIQUE NOT NULL, data TEXT NOT NULL);
            CREATE TABLE IF NOT EXISTS people(id INTEGER PRIMARY KEY, code TEXT UNIQUE NOT NULL, program_id INTEGER NOT NULL REFERENCES programs(id), data TEXT NOT NULL);
            CREATE TABLE IF NOT EXISTS batches(id INTEGER PRIMARY KEY, code TEXT UNIQUE NOT NULL, name TEXT NOT NULL, program_id INTEGER NOT NULL REFERENCES programs(id), people TEXT NOT NULL, approver TEXT REFERENCES accounts(id), auth TEXT NOT NULL DEFAULT 'simulation', state TEXT NOT NULL DEFAULT 'draft', version INTEGER NOT NULL DEFAULT 1, snapshot TEXT, digest TEXT);
            CREATE TABLE IF NOT EXISTS challenges(token TEXT PRIMARY KEY, batch_id INTEGER NOT NULL REFERENCES batches(id), account_id TEXT NOT NULL, version INTEGER NOT NULL, digest TEXT NOT NULL, expires REAL NOT NULL);
            CREATE TABLE IF NOT EXISTS requests(id TEXT PRIMARY KEY, batch_id INTEGER NOT NULL REFERENCES batches(id), version INTEGER NOT NULL, actor TEXT NOT NULL, snapshot TEXT NOT NULL, created TEXT NOT NULL, mode TEXT NOT NULL, state TEXT NOT NULL DEFAULT 'processing', UNIQUE(batch_id,version));
            CREATE TABLE IF NOT EXISTS cards(id TEXT PRIMARY KEY, request_id TEXT NOT NULL REFERENCES requests(id), program_id INTEGER NOT NULL, person_id INTEGER NOT NULL, ordinal INTEGER NOT NULL, status TEXT NOT NULL DEFAULT 'pending', reason TEXT, UNIQUE(program_id,person_id));
            CREATE TABLE IF NOT EXISTS events(id INTEGER PRIMARY KEY, batch_id INTEGER NOT NULL REFERENCES batches(id), actor TEXT NOT NULL, action TEXT NOT NULL, created TEXT NOT NULL, details TEXT NOT NULL);
            CREATE TRIGGER IF NOT EXISTS events_no_update BEFORE UPDATE ON events BEGIN SELECT RAISE(ABORT,'Lịch sử chỉ được bổ sung'); END;
            CREATE TRIGGER IF NOT EXISTS events_no_delete BEFORE DELETE ON events BEGIN SELECT RAISE(ABORT,'Lịch sử chỉ được bổ sung'); END;
            CREATE TABLE IF NOT EXISTS projections(token TEXT PRIMARY KEY, batch_id INTEGER NOT NULL REFERENCES batches(id), created TEXT NOT NULL);
            ''')
            # Additive migrations keep existing 0.1.0/0.1.1 demo databases intact.
            if 'session_token' not in {r['name'] for r in db.execute('PRAGMA table_info(challenges)')}:
                db.execute("ALTER TABLE challenges ADD COLUMN session_token TEXT NOT NULL DEFAULT ''")
                # Old transient challenges cannot be attributed to a login session safely.
                for old in db.execute('SELECT * FROM challenges').fetchall():
                    if self.batch(db,old['batch_id'])['state']=='waiting':
                        self.event(db,old['batch_id'],old['account_id'],'Hết hiệu lực phiên xác thực cũ khi cập nhật',{'version':old['version'],'auth':'simulation'})
                db.execute('DELETE FROM challenges')
            if 'revision' not in {r['name'] for r in db.execute('PRAGMA table_info(cards)')}:
                db.execute('ALTER TABLE cards ADD COLUMN revision INTEGER NOT NULL DEFAULT 0')
            db.execute("""CREATE TABLE IF NOT EXISTS card_operations(
                id TEXT PRIMARY KEY, request_id TEXT NOT NULL REFERENCES requests(id),
                card_id TEXT NOT NULL REFERENCES cards(id), actor TEXT NOT NULL,
                operation_key TEXT NOT NULL, kind TEXT NOT NULL, payload TEXT NOT NULL,
                state TEXT NOT NULL, created TEXT NOT NULL, UNIQUE(actor,operation_key))""")
            if not db.execute('SELECT 1 FROM accounts').fetchone():
                db.executemany('INSERT INTO accounts VALUES (?,?,?,?)', [
                    ('cb01','Mai An · Chuẩn bị','preparer',1), ('qt01','Quản trị demo','admin',1),
                    ('pd01','Minh Tâm · Phê duyệt','approver',1), ('pd02','Hải Bình · Phê duyệt','approver',1),
                    ('xem01','Khách trình chiếu','viewer',1), ('off01','Tài khoản ngừng hoạt động','approver',0)])
                program = {'code':'CT-2026-01','name':'Ấm áp sẻ chia','description':'Chương trình hỗ trợ cộng đồng — toàn bộ dữ liệu là hư cấu.', 'area':'Khu vực Minh Hòa (giả lập)', 'start':'2026-01-01','end':'2027-12-31', 'benefits':[
                    {'id':'LT','name':'Gói lương thực','type':'Hiện vật','condition':'Hộ gia đình đủ điều kiện giả lập','limit':2,'unit':'gói / tháng','points':['HT01']},
                    {'id':'YT','name':'Chăm sóc sức khỏe','type':'Dịch vụ','condition':'Có thẻ còn hiệu lực','limit':1,'unit':'lượt / tháng','points':['HT02']}], 'points':[
                    {'id':'HT01','name':'Điểm sẻ chia Minh Hòa','type':'Cửa hàng cộng đồng','address':'Địa chỉ minh họa A'},
                    {'id':'HT02','name':'Trạm sức khỏe An Vui','type':'Y tế','address':'Địa chỉ minh họa B'}]}
                db.execute('INSERT INTO programs VALUES(1,?,?)',(program['code'],dump(program)))
                for i, name in enumerate(['Nguyễn An Mẫu','Trần Bình Mẫu','Lê Chi Mẫu','Phạm Dũng Mẫu'],1):
                    person={'code':f'HS-{i:03}','name':name,'area':'Minh Hòa (giả lập)','eligible':i != 4,'basis':'Đối chiếu điều kiện bằng dữ liệu giả lập','benefit_ids':['LT','YT']}
                    db.execute('INSERT INTO people VALUES(?,?,1,?)',(i,person['code'],dump(person)))
                db.execute("INSERT INTO batches(id,code,name,program_id,people,approver) VALUES(1,'DOT-001','Đợt sẻ chia đầu tiên',1,'[1,2,3]','pd01')")
                self.event(db,1,'cb01','Tạo đợt nháp',{'version':1,'demo':True})

    @contextlib.contextmanager
    def db(self, write=False):
        db = sqlite3.connect(self.path, timeout=15)
        db.row_factory = sqlite3.Row
        db.execute('PRAGMA foreign_keys=ON')
        db.execute('PRAGMA journal_mode=WAL')
        if write:
            db.execute('BEGIN IMMEDIATE')
        try:
            yield db
            db.commit()
        except sqlite3.IntegrityError as e:
            db.rollback()
            raise Problem('Dữ liệu trùng mã hoặc đã được sử dụng trong đợt phát hành.',409) from e
        except Exception:
            db.rollback()
            raise
        finally:
            db.close()

    def event(self, db, bid, actor, action, details):
        db.execute('INSERT INTO events(batch_id,actor,action,created,details) VALUES(?,?,?,?,?)',(bid,actor,action,now(),dump(details)))

    def account(self, db, token):
        row=db.execute('SELECT a.* FROM accounts a JOIN sessions s ON s.account_id=a.id WHERE s.token=? AND s.expires>? AND a.active=1',(token,time.time())).fetchone()
        need(row is not None,'Vui lòng chọn tài khoản demo.',401)
        return dict(row)

    def role(self, account, *roles):
        need(account['role'] in roles,'Tài khoản không có quyền thực hiện thao tác này.',403)

    def batch(self, db, bid):
        row=db.execute('SELECT * FROM batches WHERE id=?',(bid,)).fetchone()
        need(row is not None,'Không tìm thấy đợt.',404)
        return dict(row)

    def visible(self, account, batch):
        need(account['role'] in ('admin','preparer') or (account['role']=='approver' and batch['approver']==account['id']),'Đợt nằm ngoài phạm vi tài khoản.',403)

    def program(self, db, pid):
        row=db.execute('SELECT * FROM programs WHERE id=?',(pid,)).fetchone()
        need(row is not None,'Không tìm thấy chương trình.',404)
        return {'id':row['id'],**json.loads(row['data'])}

    def person(self, db, pid):
        row=db.execute('SELECT * FROM people WHERE id=?',(pid,)).fetchone()
        need(row is not None,'Không tìm thấy hồ sơ.',404)
        return {'id':row['id'],'program_id':row['program_id'],**json.loads(row['data'])}

    def login(self, aid):
        need(isinstance(aid,str) and bool(aid),'Mã tài khoản không hợp lệ.')
        with self.db(True) as db:
            row=db.execute('SELECT * FROM accounts WHERE id=? AND active=1',(aid,)).fetchone()
            need(row is not None,'Tài khoản không tồn tại hoặc đã ngừng hoạt động.',403)
            token=secrets.token_urlsafe(32)
            db.execute('DELETE FROM sessions WHERE expires<?',(time.time(),))
            db.execute('INSERT INTO sessions VALUES(?,?,?)',(token,aid,time.time()+8*3600))
            return token,dict(row)

    def logout(self, token):
        with self.db(True) as db:
            rows=db.execute('SELECT * FROM challenges WHERE session_token=?',(token,)).fetchall()
            for c in rows:
                if c['expires']>time.time() and self.batch(db,c['batch_id'])['state']=='waiting':
                    self.event(db,c['batch_id'],c['account_id'],'Hủy xác thực khi đăng xuất',{'version':c['version'],'auth':'simulation'})
            db.execute('DELETE FROM challenges WHERE session_token=?',(token,))
            db.execute('DELETE FROM sessions WHERE token=?',(token,))
        return {'ok':True}

    def cancel_challenge(self, token, bid, data):
        need(isinstance(data.get('challenge'),str),'Phiên xác thực không hợp lệ.')
        with self.db(True) as db:
            # Cancellation only removes the caller's own session; never creates a decision.
            session=db.execute('SELECT account_id FROM sessions WHERE token=?',(token,)).fetchone()
            need(session is not None,'Phiên đăng nhập không còn tồn tại.',401)
            a={'id':session['account_id']}
            c=db.execute('SELECT * FROM challenges WHERE token=?',(data['challenge'],)).fetchone()
            if not c:
                return {'cancelled':False}
            need(c['batch_id']==bid and c['account_id']==a['id'] and c['session_token']==token,'Không có quyền hủy phiên xác thực này.',403)
            db.execute('DELETE FROM challenges WHERE token=?',(c['token'],))
            if self.batch(db,bid)['state']=='waiting':
                self.event(db,bid,a['id'],'Hủy xác thực khi rời màn hình',{'version':c['version'],'auth':'simulation'})
            return {'cancelled':True}

    def boot(self, token):
        with self.db() as db:
            a=self.account(db,token)
            batches=[dict(r) for r in db.execute('SELECT * FROM batches ORDER BY id DESC') if a['role'] in ('admin','preparer') or (a['role']=='approver' and r['approver']==a['id'])]
            for b in batches:
                b['people']=json.loads(b['people'])
                b.pop('snapshot'); b.pop('digest')
            full=a['role'] in ('admin','preparer')
            stats={'program_count':len({b['program_id'] for b in batches}),
                   'beneficiary_count':len({pid for b in batches for pid in b['people']}),
                   'batch_count':len(batches),'waiting_count':sum(b['state']=='waiting' for b in batches),
                   'scope':'assigned_batches' if a['role']=='approver' else 'all_demo'}
            if full:
                stats['program_count']=db.execute('SELECT COUNT(*) FROM programs').fetchone()[0]
                stats['beneficiary_count']=db.execute('SELECT COUNT(*) FROM people').fetchone()[0]
            return {'version':VERSION,'stats':stats,'account':a,'accounts':[dict(r) for r in db.execute('SELECT id,name,role,active FROM accounts') if full or r['id']==a['id']],
                'programs':[self.program(db,r[0]) for r in db.execute('SELECT id FROM programs')] if full else [],
                'people':[self.person(db,r[0]) for r in db.execute('SELECT id FROM people')] if full else [],'batches':batches}

    def save_program(self, token, data, pid=None):
        required(data,'code','name','area','start','end')
        try:
            start=datetime.strptime(data['start'],'%Y-%m-%d'); end=datetime.strptime(data['end'],'%Y-%m-%d')
        except ValueError:
            raise Problem('Ngày bắt đầu/kết thúc phải có định dạng YYYY-MM-DD.')
        need(end>=start,'Ngày kết thúc không được trước ngày bắt đầu.')
        benefits=data.get('benefits'); points=data.get('points')
        need(isinstance(benefits,list) and benefits,'Cần ít nhất một quyền lợi.')
        need(isinstance(points,list),'Danh sách điểm hỗ trợ không hợp lệ.')
        for items in [benefits,points]:
            ids=[]
            for x in items:
                need(isinstance(x,dict),'Dữ liệu quyền lợi/điểm hỗ trợ không hợp lệ.')
                required(x,'id','name','type'); ids.append(x['id'])
            need(len(ids)==len(set(ids)),'Trùng mã quyền lợi hoặc điểm hỗ trợ.')
        point_ids={p['id'] for p in points}
        for p in points: required(p,'address')
        for b in benefits:
            required(b,'condition','unit')
            need(b.get('limit') is None or (type(b.get('limit')) in (int,float) and math.isfinite(b['limit']) and b['limit']>0),'Hạn mức phải là số dương hoặc null.')
            need(isinstance(b.get('points'),list) and all(isinstance(x,str) and x in point_ids for x in b['points']),'Quyền lợi tham chiếu điểm hỗ trợ không tồn tại.')
        data={k:data[k] for k in ('code','name','area','start','end','benefits','points')} | {'description':str(data.get('description',''))[:2000]}
        with self.db(True) as db:
            a=self.account(db,token); self.role(a,'preparer')
            if pid:
                self.program(db,pid)
                # Do not invalidate the benefit links of existing beneficiary records.
                allowed={b['id'] for b in benefits}
                for row in db.execute('SELECT data FROM people WHERE program_id=?',(pid,)):
                    need(set(json.loads(row[0])['benefit_ids'])<=allowed,'Quyền lợi đang được dùng trong hồ sơ, không thể xóa mã này.',409)
                db.execute('UPDATE programs SET code=?,data=? WHERE id=?',(data['code'],dump(data),pid))
            else:
                pid=db.execute('INSERT INTO programs(code,data) VALUES(?,?)',(data['code'],dump(data))).lastrowid
            return {'id':pid}

    def save_person(self, token, data, pid=None):
        required(data,'code','name','area','basis')
        program_id=positive_id(data.get('program_id'))
        need(type(data.get('eligible')) is bool,'Cần xác định điều kiện giả lập.')
        ids=data.get('benefit_ids')
        need(isinstance(ids,list) and ids and all(isinstance(x,str) for x in ids) and len(ids)==len(set(ids)),'Cần chọn nhóm quyền lợi hợp lệ, không trùng.')
        clean={k:data[k] for k in ('code','name','area','basis','eligible','benefit_ids')}
        with self.db(True) as db:
            a=self.account(db,token); self.role(a,'preparer')
            program=self.program(db,program_id)
            need(set(ids)<={b['id'] for b in program['benefits']},'Quyền lợi không thuộc chương trình.')
            if pid:
                self.person(db,pid)
                db.execute('UPDATE people SET code=?,program_id=?,data=? WHERE id=?',(clean['code'],program_id,dump(clean),pid))
            else:
                pid=db.execute('INSERT INTO people(code,program_id,data) VALUES(?,?,?)',(clean['code'],program_id,dump(clean))).lastrowid
            return {'id':pid}

    def save_batch(self, token, data, bid=None):
        required(data,'code','name'); program_id=positive_id(data.get('program_id'))
        ids=data.get('people',[])
        need(isinstance(ids,list) and all(type(x) is int and x>0 for x in ids),'Danh sách hồ sơ không hợp lệ.')
        need(len(ids)==len(set(ids)),'Trùng hồ sơ trong cùng đợt.')
        with self.db(True) as db:
            a=self.account(db,token); self.role(a,'preparer'); self.program(db,program_id)
            for pid in ids:
                p=self.person(db,pid)
                need(p['program_id']==program_id and p['eligible'],'Hồ sơ chưa đủ điều kiện hoặc sai chương trình.')
            if bid:
                b=self.batch(db,bid)
                need(b['state']=='draft','Chỉ sửa được đợt nháp; hãy thu hồi về nháp trước.',409)
                need(data.get('version')==b['version'],'Nội dung đã thay đổi. Tải lại đợt.',409)
                db.execute('UPDATE batches SET code=?,name=?,program_id=?,people=?,version=version+1 WHERE id=?',(data['code'],data['name'],program_id,dump(ids),bid))
            else:
                bid=db.execute('INSERT INTO batches(code,name,program_id,people) VALUES(?,?,?,?)',(data['code'],data['name'],program_id,dump(ids))).lastrowid
            self.event(db,bid,a['id'],'Lưu đợt nháp',{'people':len(ids)})
            return {'id':bid}

    def configure(self, token, bid, data):
        with self.db(True) as db:
            a=self.account(db,token); self.role(a,'admin'); b=self.batch(db,bid)
            need(b['state']=='draft','Chỉ cấu hình người duyệt khi đợt ở trạng thái nháp.',409)
            need(data.get('version')==b['version'],'Phiên bản đã thay đổi.',409)
            need(isinstance(data.get('approver'),str),'Tài khoản phê duyệt không hợp lệ.')
            approver=db.execute("SELECT * FROM accounts WHERE id=? AND active=1 AND role='approver'",(data.get('approver'),)).fetchone()
            need(approver is not None,'Tài khoản phê duyệt không tồn tại hoặc không hoạt động.')
            need(data.get('auth')=='simulation','ColdKey thật chưa tích hợp; chỉ hỗ trợ xác thực mô phỏng.')
            db.execute('UPDATE batches SET approver=?,auth=?,version=version+1 WHERE id=?',(approver['id'],'simulation',bid))
            self.event(db,bid,a['id'],'Cấu hình người phê duyệt',{'approver':approver['id'],'auth':'simulation'})
            return {'ok':True}

    def submit(self, token, bid, version):
        with self.db(True) as db:
            a=self.account(db,token); self.role(a,'preparer'); b=self.batch(db,bid)
            need(b['state']=='draft' and version==b['version'],'Trạng thái hoặc phiên bản không còn hợp lệ.',409)
            need(db.execute("SELECT 1 FROM accounts WHERE id=? AND active=1 AND role='approver'",(b['approver'],)).fetchone(),'Chưa có người phê duyệt hợp lệ.')
            ids=json.loads(b['people']); need(ids,'Không thể trình đợt rỗng.')
            people=[self.person(db,pid) for pid in ids]; program=self.program(db,b['program_id'])
            for p in people:
                need(p['eligible'] and p['program_id']==b['program_id'],'Hồ sơ chưa đủ điều kiện hoặc sai chương trình.')
                need(set(p['benefit_ids'])<={x['id'] for x in program['benefits']},'Nhóm quyền lợi không còn hợp lệ.')
                need(not db.execute('SELECT 1 FROM cards WHERE program_id=? AND person_id=?',(b['program_id'],p['id'])).fetchone(),'Hồ sơ đã có thẻ hoặc đã được ghi nhận trong yêu cầu khác.',409)
            snapshot={'batch_id':bid,'code':b['code'],'name':b['name'],'version':b['version'],'program':program,'people':people,'approver':b['approver'],'auth':'simulation'}
            body=dump(snapshot); digest=hashlib.sha256(body.encode()).hexdigest()
            db.execute("UPDATE batches SET state='waiting',snapshot=?,digest=? WHERE id=?",(body,digest,bid))
            self.event(db,bid,a['id'],'Trình phê duyệt',{'version':b['version'],'digest':digest})
            return {'ok':True}

    def withdraw(self, token, bid, version):
        with self.db(True) as db:
            a=self.account(db,token); self.role(a,'preparer'); b=self.batch(db,bid)
            need(b['state']=='waiting' and version==b['version'],'Chỉ thu hồi hồ sơ đang chờ duyệt đúng phiên bản.',409)
            db.execute("UPDATE batches SET state='draft',version=version+1,snapshot=NULL,digest=NULL WHERE id=?",(bid,))
            self.event(db,bid,a['id'],'Thu hồi về nháp',{'old_version':b['version'],'new_version':b['version']+1})
            return {'ok':True}

    def challenge(self, token, bid, version):
        with self.db(True) as db:
            a=self.account(db,token); self.role(a,'approver'); b=self.batch(db,bid); self.visible(a,b)
            need(b['state']=='waiting' and version==b['version'],'Hồ sơ đã thay đổi hoặc đã được xử lý.',409)
            challenge=secrets.token_urlsafe(32)
            db.execute('DELETE FROM challenges WHERE batch_id=? AND session_token=?',(bid,token))
            db.execute('INSERT INTO challenges(token,batch_id,account_id,version,digest,expires,session_token) VALUES(?,?,?,?,?,?,?)',(challenge,bid,a['id'],b['version'],b['digest'],time.time()+300,token))
            self.event(db,bid,a['id'],'Bắt đầu xác thực mô phỏng',{'version':version,'auth':'simulation'})
            return {'challenge':challenge,'version':version,'digest':b['digest'],'expires_in':300,'snapshot':json.loads(b['snapshot'])}

    def approve(self, token, bid, data):
        with self.db(True) as db:
            a=self.account(db,token); self.role(a,'approver'); b=self.batch(db,bid); self.visible(a,b)
            need(isinstance(data.get('challenge'),str),'Phiên xác nhận không hợp lệ.',403)
            c=db.execute('SELECT * FROM challenges WHERE token=? AND account_id=? AND batch_id=?',(data.get('challenge'),a['id'],bid)).fetchone()
            need(c is not None,'Phiên xác nhận không hợp lệ.',403)
            need(c['session_token']==token,'Phiên xác nhận thuộc phiên đăng nhập khác.',403)
            need(c['version']==b['version'] and c['digest']==b['digest'],'Nội dung đã thay đổi. Phải xác nhận lại hồ sơ.',409)
            existing=db.execute('SELECT id FROM requests WHERE batch_id=? AND version=?',(bid,c['version'])).fetchone()
            if existing:
                return {'request_id':existing['id'],'replayed':True}
            need(c['expires']>time.time(),'Phiên xác nhận đã hết hạn. Mở lại bước phê duyệt.',409)
            need(b['state']=='waiting','Hồ sơ không còn chờ phê duyệt.',409)
            need(b['auth']=='simulation','Phương án xác thực không được hỗ trợ.')
            outcome=data.get('authentication')
            if outcome in ('cancel','fail'):
                db.execute('DELETE FROM challenges WHERE token=?',(c['token'],))
                self.event(db,bid,a['id'],'Hủy xác thực mô phỏng' if outcome=='cancel' else 'Xác thực mô phỏng thất bại',{'auth':'simulation','version':b['version']})
                return {'approved':False,'message':'Không phát sinh yêu cầu phát hành.'}
            need(outcome=='success','Cần kết quả xác thực mô phỏng rõ ràng.')
            mode=data.get('mode','success'); need(mode in ('success','partial','failure'),'Kịch bản phát hành không hợp lệ.')
            snap=json.loads(b['snapshot'])
            for p in snap['people']:
                need(not db.execute('SELECT 1 FROM cards WHERE program_id=? AND person_id=?',(b['program_id'],p['id'])).fetchone(),'Hồ sơ đã được phát hành hoặc giữ chỗ trong đợt khác.',409)
            rid='YC-'+secrets.token_hex(6).upper()
            db.execute('INSERT INTO requests(id,batch_id,version,actor,snapshot,created,mode) VALUES(?,?,?,?,?,?,?)',(rid,bid,b['version'],a['id'],b['snapshot'],now(),mode))
            for i,p in enumerate(snap['people']):
                db.execute('INSERT INTO cards(id,request_id,program_id,person_id,ordinal) VALUES(?,?,?,?,?)',('NA-'+secrets.token_hex(5).upper(),rid,b['program_id'],p['id'],i))
            db.execute("UPDATE batches SET state='processing' WHERE id=?",(bid,))
            self.event(db,bid,a['id'],'Ghi quyết định phê duyệt',{'request_id':rid,'version':b['version'],'digest':b['digest'],'auth':'simulation','mode':mode})
            return {'request_id':rid,'replayed':False}

    def tick(self):
        """Durable, restart-safe demo worker. Unknown outcomes never get retried automatically."""
        with self.db(True) as db:
            for r in db.execute("SELECT * FROM requests WHERE state='processing'").fetchall():
                cards=db.execute("SELECT * FROM cards WHERE request_id=? AND status='pending' ORDER BY ordinal",(r['id'],)).fetchall()
                for c in cards:
                    operation=db.execute("SELECT * FROM card_operations WHERE card_id=? AND kind='retry' AND state='pending'",(c['id'],)).fetchone()
                    status=json.loads(operation['payload'])['outcome'] if operation else ('success' if r['mode']=='success' else 'failed' if r['mode']=='failure' else ['success','failed','unknown'][c['ordinal']%3])
                    reason={'success':None,'failed':'Lỗi phát hành giả lập; người duyệt có thể thử lại trên chính thẻ này.','unknown':'Mô phỏng mất phản hồi; chưa xác định kết quả, không tự thử lại.'}[status]
                    db.execute('UPDATE cards SET status=?,reason=?,revision=revision+1 WHERE id=?',(status,reason,c['id']))
                    if operation:
                        db.execute("UPDATE card_operations SET state='done' WHERE id=?",(operation['id'],))
                    self.event(db,r['batch_id'],'worker-demo','Kết quả phát hành từng thẻ',{'request_id':r['id'],'card_id':c['id'],'status':status,'operation_id':operation['id'] if operation else None,'simulation':True})
                db.execute("UPDATE requests SET state='completed' WHERE id=?",(r['id'],))
                db.execute("UPDATE batches SET state='completed' WHERE id=?",(r['batch_id'],))
                self.event(db,r['batch_id'],'worker-demo','Hoàn tất lượt xử lý phát hành',{'request_id':r['id'],'simulation':True})

    def process_card(self, token, cid, kind, data):
        """Retry/reconcile the same reserved card; never inserts another card or request."""
        need(kind in ('retry','reconcile'),'Thao tác không hợp lệ.')
        required(data,'operation_key','outcome')
        need(len(data['operation_key'])<=128,'Mã thao tác quá dài.')
        need(type(data.get('revision')) is int and data['revision']>=0,'Cần phiên bản kết quả thẻ hợp lệ.')
        need(data['outcome'] in ('success','failed','unknown'),'Kết quả mô phỏng không hợp lệ.')
        if kind=='reconcile':
            required(data,'evidence')
            need(data.get('confirmed') is True,'Phải xác nhận đã đối chiếu kết quả mô phỏng.')
        payload={'kind':kind,'card_id':cid,'revision':data['revision'],'outcome':data['outcome']}
        if kind=='reconcile':payload.update(evidence=data['evidence'].strip(),confirmed=True)
        body=dump(payload)
        with self.db(True) as db:
            a=self.account(db,token);self.role(a,'approver')
            card=db.execute('SELECT * FROM cards WHERE id=?',(cid,)).fetchone()
            need(card is not None,'Không tìm thấy thẻ.',404)
            request=db.execute('SELECT * FROM requests WHERE id=?',(card['request_id'],)).fetchone()
            batch=self.batch(db,request['batch_id']);self.visible(a,batch)
            existing=db.execute('SELECT * FROM card_operations WHERE actor=? AND operation_key=?',(a['id'],data['operation_key'])).fetchone()
            if existing:
                need(existing['payload']==body,'Mã thao tác đã được sử dụng cho nội dung khác.',409)
                return {'operation_id':existing['id'],'request_id':request['id'],'card_id':cid,'replayed':True,'state':existing['state']}
            need(card['revision']==data['revision'],'Kết quả thẻ đã thay đổi. Tải lại trước khi xử lý.',409)
            expected='failed' if kind=='retry' else 'unknown'
            need(card['status']==expected,
                 'Chỉ thử lại thẻ lỗi đã xác định; thẻ chưa xác định phải đối chiếu trước.' if kind=='retry' else 'Chỉ đối chiếu thẻ có kết quả chưa xác định.',409)
            opid='TT-'+secrets.token_hex(8).upper()
            state='pending' if kind=='retry' else 'done'
            db.execute('INSERT INTO card_operations VALUES(?,?,?,?,?,?,?,?,?)',(opid,request['id'],cid,a['id'],data['operation_key'],kind,body,state,now()))
            if kind=='retry':
                db.execute("UPDATE cards SET status='pending',reason='Đang thử lại phát hành mô phỏng',revision=revision+1 WHERE id=?",(cid,))
                db.execute("UPDATE requests SET state='processing' WHERE id=?",(request['id'],))
                db.execute("UPDATE batches SET state='processing' WHERE id=?",(batch['id'],))
                action='Yêu cầu thử lại thẻ lỗi'
            else:
                reason={'success':None,'failed':'Đối chiếu mô phỏng xác nhận chưa phát hành; có thể thử lại.',
                        'unknown':'Đối chiếu mô phỏng chưa đủ căn cứ; tiếp tục giữ chưa xác định, không thử lại.'}[data['outcome']]
                db.execute('UPDATE cards SET status=?,reason=?,revision=revision+1 WHERE id=?',(data['outcome'],reason,cid))
                action='Đối chiếu kết quả chưa xác định'
            self.event(db,batch['id'],a['id'],action,{'operation_id':opid,'request_id':request['id'],
                'card_id':cid,'version':request['version'],'result_revision':data['revision'],
                'outcome':data['outcome'],'evidence':payload.get('evidence'),'simulation':True})
            return {'operation_id':opid,'request_id':request['id'],'card_id':cid,'replayed':False,'state':state}

    def result(self, db, rid):
        row=db.execute('SELECT * FROM requests WHERE id=?',(rid,)).fetchone()
        need(row is not None,'Không tìm thấy mã yêu cầu.',404)
        r=dict(row); r['snapshot']=json.loads(r['snapshot'])
        r['cards']=[dict(c) for c in db.execute('SELECT * FROM cards WHERE request_id=? ORDER BY ordinal',(rid,))]
        r['counts']={s:sum(c['status']==s for c in r['cards']) for s in ('success','failed','unknown','pending')}
        r['counts']['total']=len(r['cards'])
        return r

    def detail(self, token, bid):
        with self.db() as db:
            a=self.account(db,token); b=self.batch(db,bid); self.visible(a,b)
            b['people']=json.loads(b['people']); b['snapshot']=json.loads(b['snapshot']) if b['snapshot'] else None
            if not b['snapshot']:
                b['draft']={'program':self.program(db,b['program_id']),'people':[self.person(db,i) for i in b['people']]}
            b['history']=[{**dict(r),'details':json.loads(r['details'])} for r in db.execute('SELECT * FROM events WHERE batch_id=? ORDER BY id',(bid,))]
            r=db.execute('SELECT id FROM requests WHERE batch_id=? ORDER BY created DESC LIMIT 1',(bid,)).fetchone()
            b['result']=self.result(db,r[0]) if r else None
            b['projections']=[r[0] for r in db.execute('SELECT token FROM projections WHERE batch_id=?',(bid,))] if a['role'] in ('preparer','admin') else []
            return b

    def lookup(self, token, rid):
        with self.db() as db:
            a=self.account(db,token); r=self.result(db,rid); self.visible(a,self.batch(db,r['batch_id']))
            return r

    def card(self, token, cid):
        with self.db() as db:
            a=self.account(db,token)
            row=db.execute('SELECT * FROM cards WHERE id=?',(cid,)).fetchone(); need(row is not None,'Không tìm thấy thẻ.',404)
            r=self.result(db,row['request_id']); b=self.batch(db,r['batch_id']); self.visible(a,b)
            need(row['status']=='success','Chỉ mở được thẻ phát hành thành công.',409)
            snap=r['snapshot']; person=next(p for p in snap['people'] if p['id']==row['person_id'])
            benefits=[x for x in snap['program']['benefits'] if x['id'] in person['benefit_ids']]
            point_ids={p for x in benefits for p in x['points']}
            return {'card':dict(row),'person':person,'batch':{'code':snap['code'],'name':snap['name']},'program':snap['program'],'benefits':benefits,'points':[p for p in snap['program']['points'] if p['id'] in point_ids],'version':r['version']}

    def create_projection(self, token, bid):
        with self.db(True) as db:
            a=self.account(db,token); self.role(a,'preparer','admin'); b=self.batch(db,bid)
            need(b['snapshot'] is not None,'Cần trình duyệt đợt trước khi mở trình chiếu.',409)
            old=db.execute('SELECT token FROM projections WHERE batch_id=?',(bid,)).fetchone()
            if old: return {'token':old[0]}
            value=secrets.token_urlsafe(24)
            db.execute('INSERT INTO projections VALUES(?,?,?)',(value,bid,now()))
            self.event(db,bid,a['id'],'Mở phiên trình chiếu',{'public_fields':'Tên chương trình/đợt, quyền lợi, tên điểm, số tổng hợp; không công bố người thụ hưởng'})
            return {'token':value}

    def projection(self, token):
        with self.db() as db:
            row=db.execute('SELECT batch_id FROM projections WHERE token=?',(token,)).fetchone()
            need(row is not None,'Phiên trình chiếu không tồn tại.',404)
            b=self.batch(db,row[0]); need(b['snapshot'] is not None,'Đợt đang được sửa; tạm ẩn nội dung trình chiếu.',409)
            snap=json.loads(b['snapshot']); p=snap['program']
            r=db.execute('SELECT id FROM requests WHERE batch_id=? ORDER BY created DESC LIMIT 1',(b['id'],)).fetchone()
            counts=self.result(db,r[0])['counts'] if r else {'total':len(snap['people']),'success':0,'failed':0,'unknown':0,'pending':len(snap['people'])}
            # Strict allowlist. No beneficiary names, card IDs, addresses, request IDs or history.
            return {'name':snap['name'],'program':p['name'],'area':p['area'],'start':p['start'],'end':p['end'],'state':b['state'],'version':snap['version'],'counts':counts,'simulation':True,
                'benefits':[{k:x[k] for k in ('name','type','condition','limit','unit')} for x in p['benefits']],
                'points':[{'name':x['name'],'type':x['type']} for x in p['points'] if x['id'] in {i for ben in p['benefits'] for i in ben['points']}],
                'authenticating':bool(b['state']=='waiting' and db.execute("SELECT 1 FROM challenges c JOIN sessions s ON s.token=c.session_token JOIN accounts a ON a.id=c.account_id WHERE c.batch_id=? AND c.version=? AND c.expires>? AND s.expires>? AND s.account_id=c.account_id AND a.active=1 AND a.role='approver' AND a.id=?",(b['id'],b['version'],time.time(),time.time(),b['approver'])).fetchone())}

# ========== 3. HTTP API ==========
#!/usr/bin/env python3
"""Run: python server.py --port 8000. No third-party packages."""
import argparse
import json
import logging
import os
import re
import threading
from http import HTTPStatus
from http.cookies import SimpleCookie
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse



def make_handler(store):
    class Handler(BaseHTTPRequestHandler):
        server_version='NhanAi/'+VERSION
        def log_message(self, fmt, *args):
            # URL can contain a projection capability. Never log URLs or cookies.
            logging.info('%s %s', self.command, getattr(self,'response_code',''))

        def reply(self, data, status=200, cookie=None):
            body=json.dumps(data,ensure_ascii=False).encode()
            self.send_response(status); self.response_code=status
            self.send_header('Content-Type','application/json; charset=utf-8')
            self.send_header('Content-Length',str(len(body))); self.security_headers()
            if cookie: self.send_header('Set-Cookie',cookie)
            self.end_headers(); self.wfile.write(body)

        def security_headers(self):
            self.send_header('Cache-Control','no-store')
            self.send_header('X-Content-Type-Options','nosniff')
            self.send_header('Referrer-Policy','no-referrer')
            self.send_header('Content-Security-Policy',"default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self' data:; connect-src 'self'; frame-ancestors 'none'; base-uri 'none'; form-action 'self'")

        def token(self):
            try:
                c=SimpleCookie(self.headers.get('Cookie','')); return c['session'].value if 'session' in c else ''
            except Exception: return ''

        def run(self, post=False):
            try:
                path=urlparse(self.path).path
                data={}
                if post:
                    # JSON-only requests and same-origin checks prevent drive-by form/CSRF mutations.
                    host=self.headers.get('Host','')
                    origin=self.headers.get('Origin')
                    if origin:
                        parsed=urlparse(origin)
                        if parsed.netloc!=host or parsed.scheme not in ('http','https'): raise Problem('Nguồn yêu cầu không hợp lệ.',403)
                    if self.headers.get('Sec-Fetch-Site')=='cross-site': raise Problem('Yêu cầu khác nguồn bị chặn.',403)
                    if self.headers.get_content_type()!='application/json': raise Problem('Yêu cầu phải là JSON.',415)
                    try: size=int(self.headers.get('Content-Length','0'))
                    except ValueError: raise Problem('Độ dài yêu cầu không hợp lệ.')
                    if not 0<size<=1024*1024: raise Problem('Yêu cầu rỗng hoặc quá lớn.',413)
                    try: data=json.loads(self.rfile.read(size))
                    except (ValueError,UnicodeError): raise Problem('JSON không hợp lệ.')
                    if not isinstance(data,dict): raise Problem('Nội dung phải là đối tượng JSON.')
                token=self.token()
                if path=='/api/meta' and not post: return self.reply({'version':VERSION})
                if path=='/api/accounts' and not post:
                    with store.db() as db: rows=[dict(r) for r in db.execute('SELECT id,name,role,active FROM accounts')]
                    return self.reply(rows)
                if path=='/api/login' and post:
                    tok,a=store.login(data.get('account_id'))
                    if token: store.logout(token)
                    return self.reply(a,cookie=f'session={tok}; HttpOnly; SameSite=Strict; Path=/; Max-Age=28800')
                if path=='/api/logout' and post:
                    store.logout(token)
                    return self.reply({'ok':True},cookie='session=; HttpOnly; SameSite=Strict; Path=/; Max-Age=0')
                if path=='/api/bootstrap' and not post: return self.reply(store.boot(token))
                m=re.fullmatch(r'/api/public/([A-Za-z0-9_-]+)',path)
                if m and not post: return self.reply(store.projection(m[1]))
                m=re.fullmatch(r'/api/(programs|people|batches)(?:/(\d+))?',path)
                if m:
                    kind=m[1]; objid=int(m[2]) if m[2] else None
                    if post:
                        return self.reply({'programs':store.save_program,'people':store.save_person,'batches':store.save_batch}[kind](token,data,objid))
                    if kind=='batches' and objid: return self.reply(store.detail(token,objid))
                m=re.fullmatch(r'/api/batches/(\d+)/(configure|submit|withdraw|challenge|approve|projection|cancel-auth)',path)
                if m and post:
                    bid=int(m[1]); action=m[2]
                    if action in ('submit','withdraw','challenge'): result=getattr(store,action)(token,bid,data.get('version'))
                    elif action=='cancel-auth': result=store.cancel_challenge(token,bid,data)
                    elif action=='projection': result=store.create_projection(token,bid)
                    else: result=getattr(store,action)(token,bid,data)
                    return self.reply(result)
                m=re.fullmatch(r'/api/cards/([A-Za-z0-9_-]+)/(retry|reconcile)',path)
                if m and post: return self.reply(store.process_card(token,m[1],m[2],data))
                m=re.fullmatch(r'/api/(requests|cards)/([A-Za-z0-9_-]+)',path)
                if m and not post: return self.reply((store.lookup if m[1]=='requests' else store.card)(token,m[2]))
                if path.startswith('/api/'): raise Problem('Không tìm thấy API.',404)
                if post: raise Problem('Không tìm thấy.',404)
                files={'/':'index.html','/index.html':'index.html','/app.js':'app.js','/style.css':'style.css'}
                if path not in files: raise Problem('Không tìm thấy trang.',404)
                file=Path(files[path]); body=STATIC_FILES[files[path]].encode('utf-8')
                types={'.html':'text/html','.js':'text/javascript','.css':'text/css'}
                self.send_response(200); self.response_code=200
                self.send_header('Content-Type',types[file.suffix]+'; charset=utf-8')
                self.send_header('Content-Length',str(len(body))); self.security_headers(); self.end_headers(); self.wfile.write(body)
            except Problem as e: self.reply({'error':e.message},e.status)
            except (BrokenPipeError,ConnectionResetError): pass
            except Exception:
                logging.exception('Unhandled server error')
                self.reply({'error':'Lỗi máy chủ. Vui lòng tải lại và tra cứu yêu cầu trước khi thao tác tiếp.'},500)
        def do_GET(self): self.run()
        def do_POST(self): self.run(True)
    return Handler



# ========== 4. KHỞI ĐỘNG ỨNG DỤNG ==========
def main():
    import errno
    import webbrowser

    parser = argparse.ArgumentParser(description="Thẻ Nhân Ái — chạy trực tiếp trên Python và VS Code")
    parser.add_argument("--port", type=int, default=8000, help="Cổng web, mặc định 8000")
    parser.add_argument("--host", default="127.0.0.1", help="Địa chỉ lắng nghe, mặc định chỉ máy này")
    parser.add_argument("--db", default=str(Path(__file__).resolve().parent / "nhan_ai_data" / "demo.sqlite3"))
    parser.add_argument("--no-browser", action="store_true", help="Không tự mở trình duyệt")
    args = parser.parse_args()
    if not 0 <= args.port <= 65535:
        parser.error("Cổng phải nằm trong khoảng 0 đến 65535.")

    Path(args.db).parent.mkdir(parents=True, exist_ok=True)
    store = Store(args.db)
    handler = make_handler(store)
    try:
        httpd = ThreadingHTTPServer((args.host, args.port), handler)
    except OSError as exc:
        if exc.errno not in (errno.EADDRINUSE, 10048):
            raise
        # Cổng đã được ứng dụng khác sử dụng: chọn cổng trống và in đúng URL.
        print(f"Cổng {args.port} đang được sử dụng. Đang chọn cổng trống...", flush=True)
        httpd = ThreadingHTTPServer((args.host, 0), handler)

    stop = threading.Event()
    def worker():
        while not stop.wait(1.5):
            try:
                store.tick()
            except Exception:
                logging.exception("Worker demo bị lỗi; yêu cầu vẫn được giữ trong cơ sở dữ liệu")

    thread = threading.Thread(target=worker, daemon=True)
    thread.start()
    browser_host = "127.0.0.1" if args.host == "0.0.0.0" else args.host
    url = f"http://{browser_host}:{httpd.server_port}"
    print(f"\nTHẺ NHÂN ÁI — {VERSION} — XÁC THỰC VÀ PHÁT HÀNH MÔ PHỎNG", flush=True)
    print("Mở ứng dụng tại: " + url, flush=True)
    print("Dữ liệu: " + str(Path(args.db).resolve()), flush=True)
    print("Giữ cửa sổ Terminal này mở. Nhấn Ctrl+C để dừng.\n", flush=True)

    if not args.no_browser:
        def launch_browser():
            try:
                webbrowser.open(url)
            except Exception:
                print("Không tự mở được trình duyệt. Bạn hãy mở địa chỉ: " + url, flush=True)
        opener = threading.Timer(0.5, launch_browser)
        opener.daemon = True
        opener.start()

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nĐã dừng ứng dụng; dữ liệu đã lưu vẫn được giữ lại.", flush=True)
    finally:
        stop.set()
        httpd.server_close()
        thread.join(3)


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        import traceback
        traceback.print_exc()
        if os.name == "nt":
            input("Không khởi động được. Sao chép lỗi phía trên để được hỗ trợ. Nhấn Enter để đóng...")
        raise SystemExit(1)
