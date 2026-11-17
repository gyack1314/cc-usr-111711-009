"""按已知时间冻结报告及输入证据。"""
import hashlib
import json
from .evidence import records
from .planner import plan
from .context import snapshot,metrics
from .economics import summarize

def generate(db,period,known_at):
    supplies=records(db,'supply',known_at)
    demands=records(db,'demand',known_at)
    certificates=records(db,'certificate',known_at)
    state=snapshot(db,known_at)
    result=plan(supplies,demands,certificates,period,state)
    sources=sorted({r['source']['sha256'] for group in (supplies,demands,certificates) for r in group})
    report={'period':period,'known_at':known_at,'summary':summarize(result),
            'allocations':result['allocations'],'unmet':result['unmet'],
            'reasons':result['reasons'],'input_sha256':sources,
            'business_context':state,'context_metrics':metrics(result['allocations'],state,period)}
    report['fingerprint']=hashlib.sha256(json.dumps(report,ensure_ascii=False,sort_keys=True).encode()).hexdigest()
    return report

def compare(left,right):
    fields=('delivered','cost','emissions','unmet')
    return {'left':left['fingerprint'],'right':right['fingerprint'],
            'changes':{field:right['summary'][field]-left['summary'][field] for field in fields},
            'evidence_changed':left['input_sha256']!=right['input_sha256']}
