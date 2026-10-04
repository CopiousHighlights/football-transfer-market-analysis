import json,re,unittest
from pathlib import Path
from zipfile import ZipFile
import openpyxl
R=Path(__file__).resolve().parents[1]
class RatingTests(unittest.TestCase):
    def test_transfer_identity_and_missing_fees(self):
        rows=json.loads((R/'data/processed/ratings.json').read_text(encoding='utf-8'))['rows']
        self.assertEqual(len(rows),len({r['rating_id'] for r in rows}))
        self.assertEqual(len(rows),112)
        for row in rows:
            if row['rating'] is not None:self.assertTrue(.1<=row['rating']<=10)
            if row['rating_status']=='Fee needed':self.assertIsNone(row['rating'])
        rodri=[r for r in rows if r['dataset']=='historical' and r['player_name']=='Rodri']
        self.assertEqual({r['rating'] for r in rodri},{8.8,9.8})
    def test_original_worksheets_and_native_parts_preserved(self):
        changed={'xl/styles.xml','xl/workbook.xml','xl/_rels/workbook.xml.rels','[Content_Types].xml','docProps/app.xml'}
        with ZipFile(R/'excel/original/Football_Transfer_Worth_Final_Original.xlsx') as old,ZipFile(R/'excel/Football_Transfer_Worth_Final.xlsx') as current:
            for name in old.namelist():
                if name not in changed:self.assertEqual(old.read(name),current.read(name),name)
    def test_position_weights_and_formula_caches(self):
        w=openpyxl.load_workbook(R/'excel/Football_Transfer_Worth_Final.xlsx',data_only=True)
        for values in w['Position_Rubric'].iter_rows(min_row=6,max_row=14,values_only=True):self.assertAlmostEqual(sum(values[2:7]),1)
        self.assertIsNone(w['Rating_Calculator']['J6'].value)
        self.assertEqual(w['Rating_Calculator']['L6'].value,'Needs component scores')
        self.assertEqual(w['Transfer_Ratings']['K9'].value,9.7)
    def test_excel_compatibility_namespace_declarations(self):
        with ZipFile(R/'excel/Football_Transfer_Worth_Final.xlsx') as z:
            for part in ['xl/workbook.xml','xl/styles.xml']:
                text=z.read(part).decode('utf-8')
                prefixes=set(re.findall(r'xmlns:([\w]+)=',text))
                for tokens in re.findall(r'(?:Ignorable|Requires)="([^"]+)"',text):
                    self.assertTrue(set(tokens.split()).issubset(prefixes),part)
if __name__=='__main__':unittest.main()
