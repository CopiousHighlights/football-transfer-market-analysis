import base64,csv,json,re,unittest,zlib
from pathlib import Path
R=Path(__file__).resolve().parents[1]
P=R/'power-bi'
class PowerBIProjectTests(unittest.TestCase):
    def test_visual_fields_exist_in_model(self):
        model=json.loads((P/'TransferMarket.SemanticModel/model.bim').read_text(encoding='utf8'))['model']
        tables={t['name']:t for t in model['tables']}
        for path in P.rglob('visual.json'):
            visual=json.loads(path.read_text(encoding='utf8'))
            for role in visual['visual']['query']['queryState'].values():
                for projection in role['projections']:
                    kind,field=next(iter(projection['field'].items()))
                    table=tables[field['Expression']['SourceRef']['Entity']]
                    self.assertIn(field['Property'],[f['name'] for f in table['measures' if kind=='Measure' else 'columns']])
    def test_embedded_snapshots_match_csvs(self):
        names={'Transfers':'summer_transfers','HistoricalSample':'paid_sample','ValuationSample':'valuation_sample'}
        for table,csv_name in names.items():
            query=(P/'queries'/f'{table}.pq').read_text(encoding='utf8')
            payload=re.search(r'Binary.FromText\("([^\"]+)"',query).group(1)
            records=json.loads(zlib.decompress(base64.b64decode(payload),-15))
            with (R/'data/processed'/f'{csv_name}.csv').open(encoding='utf8',newline='') as f:source=list(csv.DictReader(f))
            self.assertEqual(len(records),len(source))
            for row,expected in zip(records,source):
                self.assertEqual(row,{k:(v or None) for k,v in expected.items() if k in row})
    def test_relationship_keys_are_unique(self):
        with (R/'data/processed/summer_transfers.csv').open(encoding='utf8',newline='') as f:rows=list(csv.DictReader(f))
        self.assertEqual(len(rows),len(set(r['record_id'] for r in rows)))
        model=json.loads((P/'TransferMarket.SemanticModel/model.bim').read_text(encoding='utf8'))['model']
        self.assertEqual(len(model['relationships']),2)
if __name__=='__main__':unittest.main()
