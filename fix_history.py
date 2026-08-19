import re

with open('global-emerging-markets-dashboard.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update HISTORY to include archive links
old_history = '''const HISTORY = [
 {date:"2026-08-18", title:"每日更新：新增16条政策条目", summary:"本次更新覆盖全部7个地区。新增条目包括：尼日利亚SEC ESG/多样性要求、肯尼亚Finance Act 2026及大规模注销执法、埃塞俄比亚投资激励改革条例586/2026、新加坡董事违规处罚升级、印尼企业刑事责任扩大、马来西亚MCCG 2026修订、巴西受益所有权门槛下调、墨西哥ESG强制披露、哥伦比亚统一合规体系、沙特CMA公司法实施条例修订、阿联酋气候法强制披露、中港SFC-CSRC深化合作、开曼公司法修订、百慕大全球最低税、俄罗斯数字资产监管框架。", meta:"影响：条目总数从44条增至60条；新增百慕大为离岸金融中心覆盖国家"},
 {date:"2026-08-18", title:"看板重构与历史档案启用", summary:"看板统一为新兴地区公司治理法规政策看板，并新增历史档案（记录）入口；后续更新摘要会持续沉淀到历史档案中，便于随时查看。", meta:"影响：导航结构更新、历史归档功能上线"},
 {date:"2026-08-17", title:"示例历史记录", summary:"历史档案展示区已启用，后续每日更新的旧版本摘要将自动归档。", meta:"影响：支持回看旧更新记录"}
];'''

new_history = '''const HISTORY = [
 {date:"2026-08-18", title:"每日更新：新增16条政策条目", summary:"本次更新覆盖全部7个地区。新增条目包括：尼日利亚SEC ESG/多样性要求、肯尼亚Finance Act 2026及大规模注销执法、埃塞俄比亚投资激励改革条例586/2026、新加坡董事违规处罚升级、印尼企业刑事责任扩大、马来西亚MCCG 2026修订、巴西受益所有权门槛下调、墨西哥ESG强制披露、哥伦比亚统一合规体系、沙特CMA公司法实施条例修订、阿联酋气候法强制披露、中港SFC-CSRC深化合作、开曼公司法修订、百慕大全球最低税、俄罗斯数字资产监管框架。", meta:"影响：条目总数从44条增至60条；新增百慕大为离岸金融中心覆盖国家", archive:"archive-2026-08-18.html"},
 {date:"2026-08-18", title:"看板重构与历史档案启用", summary:"看板统一为新兴地区公司治理法规政策看板，并新增历史档案（记录）入口；后续更新摘要会持续沉淀到历史档案中，便于随时查看。", meta:"影响：导航结构更新、历史归档功能上线", archive:null},
 {date:"2026-08-17", title:"示例历史记录", summary:"历史档案展示区已启用，后续每日更新的旧版本摘要将自动归档。", meta:"影响：支持回看旧更新记录", archive:null}
];'''

content = content.replace(old_history, new_history)

# 2. Remove the broken ARCHIVES block
archives_block = re.search(r'\nconst ARCHIVES = \[[\s\S]*?\n\];\n', content)
if archives_block:
    content = content.replace(archives_block.group(0), '\n')

# 3. Update renderHistory to create clickable links
old_render = '''function renderHistory(){ const box=document.getElementById("historyList"); box.innerHTML = HISTORY.map(h=>{
  const archive = ARCHIVES.find(a=>a.date===h.date);
  const hasArchive = archive ? true : false;
  return `<div class="history-item ${{hasArchive?'clickable':''}}" ${{hasArchive?`onclick="loadArchive('${{h.date}}')`:''}}>
    <div class="hd">
      <div class="date">${{h.date}} · ${{h.title}}</div>
      <div class="meta2">${{h.meta}}</div>
      ${{hasArchive?'<span class="badge">查看存档</span>':''}}
    </div>
  </div>`;
}).join(""); }

function loadArchive(date){
  const archive = ARCHIVES.find(a=>a.date===date);
  if(!archive) return;
  // Switch to archive view
  document.getElementById("dashboardPanel").style.display = "block";
  document.getElementById("historyPanel").classList.remove("active");
  document.querySelectorAll("[data-tab]").forEach(x=>x.classList.remove("active"));
  document.querySelector('[data-tab="dashboard"]').classList.add("active");
  // Replace DATA with archive data
  const originalData = DATA;
  DATA = archive.data;
  renderStats();
  render();
  // Add back button
  const stats = document.getElementById("stats");
  const backBtn = document.createElement("div");
  backBtn.className = "back-btn";
  backBtn.innerHTML = '<button onclick="location.reload()">← 返回当前看板</button>';
  stats.insertBefore(backBtn, stats.firstChild);
}'''

new_render = '''function renderHistory(){ const box=document.getElementById("historyList"); box.innerHTML = HISTORY.map(h=>{
  const hasArchive = h.archive ? true : false;
  const link = hasArchive ? `<a href="${h.archive}" target="_blank" class="archive-link">查看当天看板快照 →</a>` : '';
  return `<div class="history-item ${hasArchive?'has-archive':''}">
    <div class="hd">
      <div class="date">${h.date} · ${h.title}</div>
      <div class="meta2">${h.meta}</div>
      ${link}
    </div>
    <div class="sum">${h.summary}</div>
  </div>`;
}).join(""); }'''

content = content.replace(old_render, new_render)

# 4. Update CSS for clickable archive links
old_css = '''.history-item .meta2{margin-top:8px;color:var(--ink-soft);font-size:12px}
.history-item{cursor:pointer;transition:box-shadow .15s;}
.history-item:hover{box-shadow:0 2px 8px rgba(0,0,0,.08);}
.history-item .hd{cursor:pointer;}
.history-item .arrow{font-size:12px;color:var(--ink-soft);transition:transform .2s;flex-shrink:0;margin-left:8px;}
.history-item.open .arrow{transform:rotate(180deg);}
.history-item .body{max-height:0 !important;overflow:hidden !important;transition:max-height .3s ease,padding .3s ease;}
.history-item.open .body{max-height:500px;padding-top:8px;}
.history-item .sum{margin-top:6px;color:var(--ink);font-size:13px;line-height:1.65}'''

new_css = '''.history-item .meta2{margin-top:8px;color:var(--ink-soft);font-size:12px}
.history-item{border:1px solid var(--line);border-radius:16px;padding:14px 16px;background:linear-gradient(180deg,#fff,#f9fbff);transition:box-shadow .15s;}
.history-item:hover{box-shadow:0 2px 8px rgba(0,0,0,.08);}
.history-item.has-archive{border-left:3px solid var(--blue);cursor:pointer;}
.history-item.has-archive:hover{background:var(--blue-soft);}
.history-item .hd{display:flex;justify-content:space-between;gap:12px;flex-wrap:wrap;align-items:center;}
.history-item .sum{margin-top:6px;color:var(--ink);font-size:13px;line-height:1.65;}
.archive-link{display:inline-block;margin-top:8px;color:var(--blue);font-size:13px;font-weight:600;text-decoration:none;transition:color .15s;}
.archive-link:hover{color:#003a94;text-decoration:underline;}'''

content = content.replace(old_css, new_css)

with open('global-emerging-markets-dashboard.html', 'w', encoding='utf-8') as f:
    f.write(content)

print('Done: history items now link to archive snapshots')
