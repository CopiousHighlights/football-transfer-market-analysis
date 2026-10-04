import json,sqlite3,unittest
from pathlib import Path
R=Path(__file__).resolve().parents[1]
class PipelineTests(unittest.TestCase):
    def test_quality_checks_pass(self):
        report=json.loads((R/'analysis/quality_report.json').read_text())
        self.assertTrue(all(report['checks'].values()))
    def test_unknown_is_not_zero(self):
        with sqlite3.connect(R/'data/transfer_market.sqlite') as c:
            self.assertGreater(c.execute("SELECT COUNT(*) FROM summer_transfers WHERE fee_status='Undisclosed' AND quoted_fee_gbp IS NULL").fetchone()[0],0)
    def test_component_join_does_not_duplicate_transfers(self):
        with sqlite3.connect(R/'data/transfer_market.sqlite') as c:
            rows=c.execute((R/'sql/analysis/06_fee_component_join.sql').read_text()).fetchall()
            self.assertEqual(len(rows),len(set(r[0] for r in rows)))
if __name__=='__main__':unittest.main()
