"""读取项目数据并形成两个证据时点的分析报告。"""
import argparse
import json
from pathlib import Path
from .evidence import connect,receive
from .reports import generate,compare

def main():
    p=argparse.ArgumentParser()
    p.add_argument('command',choices=['inspect'])
    p.add_argument('input')
    args=p.parse_args()
    doc=json.loads(Path(args.input).read_text(encoding='utf-8'))
    db=connect(':memory:')
    for item in doc['documents']:receive(db,item)
    left=generate(db,doc['period'],doc['known_at'][0])
    right=generate(db,doc['period'],doc['known_at'][1])
    print(json.dumps({'initial':left,'current':right,'comparison':compare(left,right)},ensure_ascii=False,indent=2))
    db.close()
if __name__=='__main__':main()
