"""在单期已确认供应约束内形成可解释的分配。"""
from .policy import allowed,classify_inputs

def plan(supplies,demands,certificates,period,state):
    problems=classify_inputs(supplies,demands,certificates)
    if problems:return {'allocations':[],'unmet':[],'reasons':problems}
    inventory={s['id']:s['payload']['quantity'] for s in supplies}
    allocations=[];unmet=[];reasons=[]
    for demand in sorted(demands,key=lambda x:(x['payload']['priority'],x['id'])):
        remaining=demand['payload']['quantity']
        options=[]
        for supply in supplies:
            ok,reason,certificate=allowed(supply,demand,certificates,period,state)
            if ok:options.append((supply['payload']['unit_cost'],supply['id'],supply,certificate))
            else:reasons.append({'demand':demand['id'],'supply':supply['id'],'reason':reason})
        for _,_,supply,certificate in sorted(options):
            take=min(remaining,inventory[supply['id']])
            if take<=0:continue
            inventory[supply['id']]-=take;remaining-=take
            allocations.append({'demand':demand['id'],'supply':supply['id'],'quantity':take,
              'unit_cost':supply['payload']['unit_cost'],
              'intensity':supply['payload']['intensity'],
              'certificate':certificate['id'] if certificate else None,
              'evidence':[demand['source']['sha256'],supply['source']['sha256']]})
            if remaining<=0:break
        if remaining>0:unmet.append({'demand':demand['id'],'quantity':remaining})
    return {'allocations':allocations,'unmet':unmet,'reasons':reasons}
