"""将证据声明转成可用于方案的现行资格。"""
from datetime import date
from .context import eligible

def same_period(start,end,target):
    day=date.fromisoformat(target)
    return date.fromisoformat(start)<=day<=date.fromisoformat(end)

def allowed(supply,demand,certificates,period,state):
    s=supply['payload'];d=demand['payload']
    good,why=eligible(s,d,state,period)
    if not good:return False,why,None
    if s['product']!=d['product'] or s['market']!=d['market']:
        return False,'产品或市场不匹配',None
    if not same_period(s['start'],s['end'],period):
        return False,'供应不在期间',None
    if d.get('required_certificate'):
        for certificate in certificates:
            c=certificate['payload']
            if c['batch']==s['batch'] and c['standard']==d['required_certificate'] and c['state']=='active' and same_period(c['start'],c['end'],period):
                return True,'可用',certificate
        return False,'没有适用的有效证书',None
    return True,'可用',None

def classify_inputs(supplies,demands,certificates):
    batch_ids={item['payload']['batch'] for item in supplies}
    problems=[]
    for item in certificates:
        if item['payload']['batch'] not in batch_ids:
            problems.append({'record':item['id'],'reason':'证书所指批次尚未取得'})
    for item in demands:
        if item['payload']['quantity']<=0:problems.append({'record':item['id'],'reason':'需求量必须为正'})
    return problems
