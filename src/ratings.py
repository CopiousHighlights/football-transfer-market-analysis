"""Export editable workbook ratings without changing transfer facts."""
import csv,json,sqlite3
from datetime import date,datetime
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def export_ratings(wb):
    metadata=json.loads((ROOT/'data/ratings/scouting_ratings.json').read_text(encoding='utf-8'))
    existing={r['rating_id']:r for r in metadata['rows']}
    sheet=wb['Transfer_Ratings'];headers=[c.value for c in sheet[5]]
    rows=[]
    for values in sheet.iter_rows(min_row=6,values_only=True):
        if not values[0]:continue
        record={k:v.isoformat()[:10] if isinstance(v,(date,datetime)) else v for k,v in zip(headers,values)}
        if record['rating_id'] not in existing:raise ValueError('Register new transfer identity before exporting ratings')
        rating=record['rating']
        if rating is not None and (not isinstance(rating,(int,float)) or not .1<=rating<=10 or abs(rating*10-round(rating*10))>1e-8):raise ValueError('Ratings must be numeric, 0.1–10.0, one decimal')
        if record['rating_status']=='Fee needed' and rating is not None:raise ValueError('Missing fee cannot receive a calculated fee-value rating')
        rows.append({**existing[record['rating_id']],**record})
    if len(rows)!=len({r['rating_id'] for r in rows}):raise ValueError('Duplicate rating transfer IDs')
    metadata['rows']=rows
    output=ROOT/'data/processed/transfer_ratings.csv'
    with output.open('w',newline='',encoding='utf-8') as f:
        writer=csv.DictWriter(f,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
    (ROOT/'data/processed/ratings.json').write_text(json.dumps(metadata,ensure_ascii=False,indent=2),encoding='utf-8')
    with sqlite3.connect(ROOT/'data/transfer_market.sqlite') as con:
        con.execute('DROP TABLE IF EXISTS transfer_ratings')
        fields=list(rows[0]);numeric={'source_index','fee_amount','age_at_transfer','rating'}
        con.execute('CREATE TABLE transfer_ratings ('+', '.join('"'+k+'" '+('REAL' if k in numeric else 'TEXT') for k in fields)+')')
        con.executemany('INSERT INTO transfer_ratings VALUES ('+','.join('?' for k in fields)+')',[[r[k] for k in fields] for r in rows])
    # Position weights and production criteria remain inspectable CSV inputs.
    rub=wb['Position_Rubric'];weights=[]
    for row in rub.iter_rows(min_row=6,max_row=14,values_only=True):
        weights.append(dict(zip(['position','rule_status','production','fee_vs_worth','potential','age','competition'],row[:7])))
    with (ROOT/'data/processed/position_rating_weights.csv').open('w',newline='',encoding='utf-8') as f:
        writer=csv.DictWriter(f,fieldnames=list(weights[0]));writer.writeheader();writer.writerows(weights)
    with (ROOT/'data/processed/position_production_criteria.csv').open('w',newline='',encoding='utf-8') as f:
        writer=csv.writer(f);writer.writerow(['position','criterion','weight','evidence_needed','normalization','rule_status'])
        writer.writerows([list(row[:6]) for row in rub.iter_rows(min_row=18,max_row=53,values_only=True)])
    return {'rating_records':len(rows),'scored':sum(r['rating'] is not None for r in rows),'fee_needed':sum(r['rating_status']=='Fee needed' for r in rows)}
