import json
from datetime import datetime

# Read current HTML
with open('global-emerging-markets-dashboard.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Extract current DATA array
import re
data_match = re.search(r'const DATA = \[([\s\S]*?)\];', content)
if data_match:
    current_data = data_match.group(1).strip()
else:
    print("ERROR: DATA not found")
    exit(1)

# Create archive entry for today (2026-08-18 was the last update)
# We'll store archives as a JS object
archive_entry = f'''
 {{
   date: "2026-08-18",
   title: "每日更新：新增16条政策条目",
   meta: "影响：条目总数从44条增至60条；新增百慕大为离岸金融中心覆盖国家",
   data: [{current_data}]
 }}'''

# Find where to insert ARCHIVES (after HISTORY definition)
history_end = content.find('];', content.find('const HISTORY = [')) + 2

# Insert ARCHIVES definition
archives_def = f'''
const ARCHIVES = [{archive_entry}
];'''

content = content[:history_end] + '\n' + archives_def + content[history_end:]

# Modify renderHistory to create links instead of expandable items
old_render = '''function renderHistory(){ const box=document.getElementById("historyList"); box.innerHTML = HISTORY.map(h=>`<div class="history-item" onclick="this.classList.toggle('open')"><div class="hd"><div class="date">${{h.date}} · ${{h.title}}</div><div class="meta2">${{h.meta}}</div><span class="arrow">▼</span></div><div class="body"><div class="sum">${{h.summary}}</div></div></div>`).join(""); }'''

new_render = '''function renderHistory(){ const box=document.getElementById("historyList"); box.innerHTML = HISTORY.map(h=>{
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

content = content.replace(old_render, new_render)

# Add CSS for clickable history and back button
old_css = '.history-item .meta2{margin-top:8px;color:var(--ink-soft);font-size:12px}'
new_css = '''.history-item .meta2{margin-top:8px;color:var(--ink-soft);font-size:12px}
.history-item.clickable{cursor:pointer;transition:all .15s;}
.history-item.clickable:hover{background:var(--blue-soft);border-color:var(--blue);}
.history-item .badge{background:var(--blue);color:#fff;padding:3px 10px;border-radius:12px;font-size:11px;font-weight:600;}
.back-btn{margin-bottom:12px;}
.back-btn button{background:var(--blue);color:#fff;border:none;padding:8px 16px;border-radius:8px;cursor:pointer;font-size:13px;}
.back-btn button:hover{background:#003a94;}'''
content = content.replace(old_css, new_css)

with open('global-emerging-markets-dashboard.html', 'w', encoding='utf-8') as f:
    f.write(content)

print('Done: added archive viewing feature')
