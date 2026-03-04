from pathlib import Path
ROOT=Path('.')
DAG_HINT='- For non-trivial tasks, instantiate the `Template DAG 100% compliance` from `orchestrate-multi-agents`; owners/tasks may be reduced only when not applicable, but mandatory gates cannot be removed.'
for p in ROOT.rglob('*.md'):
    s=p.as_posix().lower()
    if '/.history/' in s or '/bin/' in s:
        continue
    try:
        t=p.read_text(encoding='utf-8')
    except Exception:
        continue
    h='## Mandatory multi-agent orchestration skill'
    if h not in t or DAG_HINT in t:
        continue
    i=t.find(h)
    j=t.find('\n## ', i+1)
    if j==-1:
        block=t[i:].rstrip()+'\n'+DAG_HINT+'\n'
        n=t[:i]+block
    else:
        block=t[i:j].rstrip()+'\n'+DAG_HINT+'\n'
        n=t[:i]+block+t[j:]
    p.write_text(n,encoding='utf-8')
print('ok')
