import json, datetime
d=json.load(open('scenarios_out.json',encoding='utf-8'))
def dt(ms): return datetime.datetime.utcfromtimestamp(ms/1000+7*3600).strftime('%d/%m/%Y %H:%M')
for k,v in d.items():
    o=v.get('overview')
    print('=====',k,v.get('inputs'),'toast',v.get('toast'))
    if not o: print('  (no overview)'); continue
    print('  filters',o.get('filters'),'metrics',o.get('metrics'),'brand_metrics',o.get('brand_metrics'),'brand_scope',o.get('brand_scope'))
    top=(v.get('top') or {}).get('data',[])
    print('  top n=',len(top), {x:(v['top'].get(x)) for x in v['top'] if x!='data'} if v.get('top') else None)
    for t in top:
        print('   ',t['rank'],t['name'],'tier',t['member_tier_name'],'rec',t['recency'],'n',t['transaction_count'],'first',dt(t['first_transaction_date']),'last',dt(t['last_transaction_date']),'sales',t['sales_value'],'pics',[((p['store_name'] or '-')[:6],p['pic_name'],p['pic_type']) for p in t['pics']])
    pt=(v.get('periodTbl') or {}).get('data',[])
    print('  periodTbl rows',len(pt),'sum total',sum(r['total_customers'] for r in pt),'AS+AA ok',all(r['advisor_selected']+r['auto_assigned']==r['total_customers'] for r in pt))
    for r in pt: print('    ',r)
    print('  engagement',(v.get('engagement') or {}).get('data'))
    print('  composition',(v.get('composition') or {}).get('data'))
    tt=(v.get('totalTbl') or {}).get('data',[])
    st=(v.get('statuses') or {}).get('data',[])
    print('  totalTbl rows',len(tt),'AS+AA==Total all?',all(r['advisor_selected']+r['auto_assigned']==r['total_customers'] for r in tt), 'statuses rows',len(st))
    if k=='A_default':
        print('  mismatch rows (AS+AA!=Total):',[ (r['pic_name'],r['total_customers'],r['advisor_selected'],r['auto_assigned']) for r in tt if r['advisor_selected']+r['auto_assigned']!=r['total_customers']])
        for r in st: print('   status',r)
        print('  tt order',[ (r['pic_name'],r['pic_id'],r['total_customers']) for r in tt])
