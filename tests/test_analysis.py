"""演练来源、资格、分配、经济口径及历史报告的真实调用链。"""
import json
import unittest
from pathlib import Path
from fuel_lab.evidence import connect,receive
from fuel_lab.reports import generate,compare
from fuel_lab.context import snapshot,eligible,metrics
ROOT=Path(__file__).resolve().parents[1]
class AnalysisChain(unittest.TestCase):
    def setUp(self):
        self.doc=json.loads((ROOT/'data/example.json').read_text(encoding='utf-8'))
        self.db=connect(':memory:')
    def tearDown(self):self.db.close()
    def test_source_to_report(self):
        for item in self.doc['documents']:receive(self.db,item)
        older=generate(self.db,self.doc['period'],self.doc['known_at'][0])
        newer=generate(self.db,self.doc['period'],self.doc['known_at'][1])
        self.assertEqual(older['summary']['delivered'],60)
        self.assertEqual(newer['summary']['delivered'],0)
        self.assertTrue(compare(older,newer)['evidence_changed'])
        self.assertNotEqual(older['fingerprint'],newer['fingerprint'])
        self.assertTrue(all(row['evidence'] for row in older['allocations']))
        self.assertEqual(older['business_context'],newer['business_context'])
        self.assertTrue(older['context_metrics'])
    def test_same_source_revision_conflict(self):
        first=self.doc['documents'][0]
        receive(self.db,first)
        changed=json.loads(json.dumps(first))
        changed['records'][0]['payload']['review_marker']='revised'
        with self.assertRaises(ValueError):receive(self.db,changed)
        self.assertEqual(self.db.execute('SELECT COUNT(*) FROM documents').fetchone()[0],1)
    def test_repeat_is_idempotent(self):
        first=self.doc['documents'][0]
        self.assertEqual(receive(self.db,first),receive(self.db,first))
        self.assertEqual(self.db.execute('SELECT COUNT(*) FROM documents').fetchone()[0],1)

    def test_business_context_contract(self):
        for item in self.doc['documents']:receive(self.db,item)
        state=snapshot(self.db,self.doc['known_at'][0])
        self.assertIsNotNone(state)
        supply=self.doc['documents'][1]['records'][0]['payload']
        demand=self.doc['documents'][2]['records'][0]['payload']
        ok,reason=eligible(supply,demand,state,self.doc['period'])
        self.assertTrue(ok,reason)
        self.assertTrue(metrics([],state,self.doc['period']))
