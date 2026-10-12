import json, urllib.request, urllib.parse
API='https://api.modrinth.com/v2'
UA={'User-Agent':'Trino11/TMods-bundles check'}
def get(url):
    try:
        with urllib.request.urlopen(urllib.request.Request(url,headers=UA),timeout=30) as r: return json.load(r)
    except Exception as e: return {'error':str(e)}
GV='26.3'
out={}
tags=get(API+'/tag/game_version')
out['game_versions_recent']=[t['version'] for t in tags[:25]] if isinstance(tags,list) else tags
out['fabric_loader']=[(l['loader']['version'],l['loader']['stable']) for l in get('https://meta.fabricmc.net/v2/versions/loader/'+GV)[:5]] if True else None
ids=json.load(open('.github/check/ids.json'))
projects=get(API+'/projects?ids='+urllib.parse.quote(json.dumps(ids)))
res=[]
deps=set()
for p in projects:
    q='?loaders='+urllib.parse.quote('["fabric"]')+'&game_versions='+urllib.parse.quote(json.dumps([GV]))
    vs=get(API+'/project/'+p['id']+'/version'+q)
    allv=get(API+'/project/'+p['id']+'/version?loaders='+urllib.parse.quote('["fabric"]'))
    newest=allv[0]['game_versions'][-3:] if isinstance(allv,list) and allv else None
    pick=None
    if isinstance(vs,list) and vs:
        rel=[v for v in vs if v['version_type']=='release']
        pick=(rel or vs)[0]
        nums=[v['version_number'] for v in allv] if isinstance(allv,list) else []
        req=[x['project_id'] for x in pick['dependencies'] if x['dependency_type']=='required' and x.get('project_id')]
        deps.update(req)
        pick={'id':pick['id'],'number':pick['version_number'],'type':pick['version_type'],'unique':nums.count(pick['version_number'])==1,'required':req,'file':(next((f for f in pick['files'] if f['primary']),pick['files'][0]))['filename']}
    res.append({'id':p['id'],'slug':p['slug'],'title':p['title'],'pick':pick,'newest_fabric_game_versions':newest,'status':p.get('status')})
missing=[d for d in deps if d not in ids]
out['projects']=res
out['missing_required']=get(API+'/projects?ids='+urllib.parse.quote(json.dumps(missing))) if missing else []
out['missing_required']=[{'id':x['id'],'slug':x['slug'],'title':x['title']} for x in out['missing_required']] if isinstance(out['missing_required'],list) else out['missing_required']
print('RESULT_JSON '+json.dumps(out))
