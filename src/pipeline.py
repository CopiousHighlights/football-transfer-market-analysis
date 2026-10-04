"""Rebuild documented CSVs, SQLite database, SQL results and quality checks."""
import argparse,csv,hashlib,json,sqlite3
from pathlib import Path
from datetime import date,datetime
import openpyxl
ROOT=Path(__file__).resolve().parents[1]
SOURCES={'summer_new':'Summer26_New','summer_matches':'Summer26_Matches',
         'summer_review':'Summer26_Review','fee_components':'Fee_Components',
         'source_checks':'Source_Checks','paid_sample':'Paid_Sample','valuation_sample':'FTV_Worth'}
def read_sheet(wb,name):
    rows=list(wb[name].values);heads=list(rows[0])
    return [dict(zip(heads,[v.isoformat()[:10] if isinstance(v,(datetime,date)) else v for v in row]))
            for row in rows[1:] if any(v is not None for v in row)]
def write_csv(path,records,fields=None):
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open('w',newline='',encoding='utf-8') as f:
        writer=csv.DictWriter(f,fieldnames=fields or list(records[0]))
        writer.writeheader();writer.writerows(records)
def main(workbook):
    wb=openpyxl.load_workbook(workbook,data_only=True)
    data={key:read_sheet(wb,sheet) for key,sheet in SOURCES.items()}
    # Source-status partition is preserved; matches are included once in the summer view.
    data['summer_transfers']=data['summer_new']+data['summer_matches']
    for row in data['summer_transfers']:
        fee=row['quoted_fee_gbp']
        row['has_reported_fee']=int(isinstance(fee,(int,float)) and fee>0)
        row['is_permanent_fee']=int(row['transfer_type']=='Fee' and row['has_reported_fee']==1)
        row['announcement_month']=(row['announcement_date'] or '')[:7]
    path=ROOT/'data/transfer_market.sqlite';path.parent.mkdir(exist_ok=True)
    with sqlite3.connect(path) as con:
        for name,records in data.items():
            if not records:raise ValueError(f'Empty required sheet: {name}')
            columns=list(records[0]);types=[]
            for c in columns:
                values=[r[c] for r in records if r[c] is not None]
                typ='INTEGER' if values and all(isinstance(v,int) for v in values) else 'REAL' if values and all(isinstance(v,(int,float)) for v in values) else 'TEXT'
                types.append(f'"{c}" {typ}')
            con.execute(f'DROP TABLE IF EXISTS "{name}"')
            con.execute(f'CREATE TABLE "{name}" ({", ".join(types)})')
            con.executemany(f'INSERT INTO "{name}" VALUES ({",".join("?" for _ in columns)})',[[r[c] for c in columns] for r in records])
            write_csv(ROOT/'data/processed'/f'{name}.csv',records)
        con.executescript((ROOT/'sql/views.sql').read_text())
        for query in sorted((ROOT/'sql/analysis').glob('*.sql')):
            cur=con.execute(query.read_text());fields=[x[0] for x in cur.description]
            result=[dict(zip(fields,row)) for row in cur]
            write_csv(ROOT/'analysis'/f'{query.stem}.csv',result,fields)
        ids=[r['record_id'] for r in data['summer_transfers']]
        checks={'unique_summer_ids':len(ids)==len(set(ids)),
                'status_partition':len(data['summer_new'])+len(data['summer_matches'])+len(data['summer_review'])==1521,
                'no_negative_reported_fees':all(r['quoted_fee_gbp'] is None or r['quoted_fee_gbp']>=0 for r in data['summer_transfers']),
                'fee_components_reference_known_ids':set(r['record_id'] for r in data['fee_components']).issubset(set(ids)),
                'coverage_total':con.execute('SELECT SUM(transfers) FROM v_league_arrivals').fetchone()[0]==sum(r['to_league'] in TOP5 for r in data['summer_transfers']),
                'summer_fee_sql_python_reconciliation':abs(con.execute('SELECT SUM(quoted_fee_gbp) FROM summer_transfers WHERE is_permanent_fee=1').fetchone()[0]-sum(r['quoted_fee_gbp'] for r in data['summer_transfers'] if r['is_permanent_fee']))<0.01}
        report={'workbook_sha256':hashlib.sha256(workbook.read_bytes()).hexdigest(),
                'source_rows':{k:len(v) for k,v in data.items()},'checks':checks,
                'historical_sample_zero_or_missing_fees':sum(not r['transfer_fee'] for r in data['paid_sample']),
                'summer_unknown_fee_count':sum(r['quoted_fee_gbp'] is None for r in data['summer_transfers']),
                'limitation':'Workbook summaries referencing 175,182 rows cannot be rebuilt without the external full dataset.'}
        (ROOT/'analysis/quality_report.json').write_text(json.dumps(report,indent=2),encoding='utf8')
        if not all(checks.values()):raise ValueError('Data quality checks failed; inspect analysis/quality_report.json')
        print(json.dumps(report,indent=2))
TOP5={'Premier League','La Liga','Serie A','Bundesliga','Ligue 1'}
if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--workbook',type=Path,default=ROOT/'excel/Football_Transfer_Worth_Final.xlsx')
    main(parser.parse_args().workbook)
