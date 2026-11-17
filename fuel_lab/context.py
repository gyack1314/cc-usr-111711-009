"""解释已取得原文中的备用库存与检修业务上下文。"""
from .evidence import records

def snapshot(db,known_at):
    rows=records(db,'context',known_at)
    if not rows:return None
    p=rows[-1]['payload']
    return {'reserve_pool':p['reserve_pool'],'reserve_units':p['reserve_units'],'outage_from':p['outage_from'],'expected_recovery':p['expected_recovery']}

def eligible(s,d,state,period):
    if state is None:return False,'缺少业务上下文'
    return (s.get('reserve_pool',state['reserve_pool'])==state['reserve_pool'],'备用供应不属于当前库存池')

def metrics(allocations,state,period):
    if state is None:return {'context_gap':'缺少业务上下文'}
    return {'reserve_left':state['reserve_units']-sum(x['quantity'] for x in allocations),'expected_recovery':state['expected_recovery']}
