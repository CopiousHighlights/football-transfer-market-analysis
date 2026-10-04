import json,csv,zlib,base64,shutil
from pathlib import Path
R=Path(__file__).resolve().parents[1];P=R/'power-bi';P.mkdir(exist_ok=True)
def put(path,data):
 p=P/path;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(data,ensure_ascii=False,indent=2) if isinstance(data,(dict,list)) else data,encoding='utf8')
def schema(kind,version):return f'https://developer.microsoft.com/json-schemas/fabric/item/report/definition/{kind}/{version}/schema.json'
put('TransferMarket.pbip',{'version':'1.0','artifacts':[{'report':{'path':'TransferMarket.Report'}}],'settings':{'enableAutoRecovery':True}})
put('TransferMarket.Report/definition.pbir',{'$schema':'https://developer.microsoft.com/json-schemas/fabric/item/report/definitionProperties/2.0.0/schema.json','version':'4.0','datasetReference':{'byPath':{'path':'../TransferMarket.SemanticModel'}}})
put('TransferMarket.SemanticModel/definition.pbism',{'version':'1.0','settings':{}})
theme=json.loads((P/'theme.json').read_text(encoding='utf8'))
put('theme.json',theme);put('TransferMarket.Report/StaticResources/RegisteredResources/FootballTheme.json',theme)
put('TransferMarket.Report/definition/version.json',{'$schema':schema('versionMetadata','1.0.0'),'version':'2.0.0'})
put('TransferMarket.Report/definition/report.json',{'$schema':schema('report','3.3.0'),'themeCollection':{'customTheme':{'name':'FootballTheme','reportVersionAtImport':{'visual':'2.12.0','page':'2.1.0','report':'3.3.0'},'type':'RegisteredResources'}},'resourcePackages':[{'name':'RegisteredResources','type':'RegisteredResources','items':[{'name':'FootballTheme','path':'FootballTheme.json','type':'CustomTheme'}]}]})
model={'name':'TransferMarket','compatibilityLevel':1567,'model':{'culture':'en-GB','defaultPowerBIDataSourceVersion':'powerBI_V3','tables':[],'relationships':[],'expressions':[{'name':'ProjectRoot','kind':'m','expression':'"" meta [IsParameterQuery=true, Type="Text", IsParameterQueryRequired=false]','description':'Optional repository root, e.g. C:/Projects/football-transfer-market-analysis. Blank uses bundled snapshot.'}]}}
types={'text':('string','type text'),'int':('int64','Int64.Type'),'number':('double','type number'),'date':('dateTime','type date')}
specs={
 'Transfers':('summer_transfers',{'record_id':'text','player_name':'text','from_club':'text','to_club':'text','announcement_date':'date','transfer_type':'text','fee_status':'text','quoted_fee_gbp':'number','quote_basis':'text','from_league':'text','to_league':'text','position':'text','source_url':'text','has_reported_fee':'int','is_permanent_fee':'int','announcement_month':'text'}),
 'HistoricalSample':('paid_sample',{'player_name':'text','from_club_name':'text','to_club_name':'text','transfer_date':'date','transfer_fee':'number','mv_at_transfer':'number','fee_to_mv':'number','position':'text','age_at_transfer':'int'}),
 'ValuationSample':('valuation_sample',{'player_name':'text','position':'text','sub_position':'text','age':'int','current_club_name':'text','league':'text','tm_value':'number','fair_value':'number','tm_to_fair':'number','minutes':'int','goals':'int','assists':'int'})}
csvrows={}
for name,(file,cols) in specs.items():
 with (R/'data/processed'/f'{file}.csv').open(encoding='utf8',newline='') as f:rows=list(csv.DictReader(f))
 rows=[{k:(None if v=='' else v) for k,v in row.items() if k in cols} for row in rows];csvrows[name]=rows
 payload=base64.b64encode(zlib.compress(json.dumps(rows,ensure_ascii=False).encode())[2:-4]).decode()
 transforms=', '.join('{"'+k+'", '+types[v][1]+'}' for k,v in cols.items())
 expr=f'''let
    Snapshot = Table.FromRecords(Json.Document(Binary.Decompress(Binary.FromText("{payload}", BinaryEncoding.Base64), Compression.Deflate))),
    Source = if ProjectRoot = "" then Snapshot else Table.SelectColumns(Table.PromoteHeaders(Csv.Document(File.Contents(ProjectRoot & "/data/processed/{file}.csv"), [Delimiter=",", Encoding=65001, QuoteStyle=QuoteStyle.Csv]), [PromoteAllScalars=true]), {{{', '.join('"'+k+'"' for k in cols)}}}),
    BlanksToNull = Table.ReplaceValue(Source, "", null, Replacer.ReplaceValue, Table.ColumnNames(Source)),
    Typed = Table.TransformColumnTypes(BlanksToNull, {{{transforms}}}, "en-GB")
in
    Typed'''
 table={'name':name,'columns':[{'name':k,'dataType':types[v][0],'sourceColumn':k,'summarizeBy':'none',**({'formatString':'dd MMM yyyy'} if v=='date' else {})} for k,v in cols.items()], 'partitions':[{'name':name,'mode':'import','source':{'type':'m','expression':expr}}]}
 model['model']['tables'].append(table)
 (P/'queries').mkdir(exist_ok=True);(P/'queries'/f'{name}.pq').write_text(expr,encoding='utf8')
def add_dimension(name,col,values,typ='text'):
 expr='let Source = #table(type table ['+col+' = '+types[typ][1]+'], {'+', '.join('{'+('"'+v.replace('"','""')+'"' if typ=='text' else '#date('+v.replace('-',',')+')')+'}' for v in values)+'}) in Source'
 model['model']['tables'].append({'name':name,'columns':[{'name':col,'dataType':types[typ][0],'sourceColumn':col,'summarizeBy':'none'}],'partitions':[{'name':name,'mode':'import','source':{'type':'m','expression':expr}}]})
add_dimension('DestinationLeague','League',sorted(set(r['to_league'] or 'Unknown' for r in csvrows['Transfers'])))
add_dimension('AnnouncementDate','Date',sorted(set(r['announcement_date'] for r in csvrows['Transfers'] if r['announcement_date'])),'date')
for name,col,dim,dcol in [('destination_league','to_league','DestinationLeague','League'),('announcement_date','announcement_date','AnnouncementDate','Date')]:
 model['model']['relationships'].append({'name':name,'fromTable':'Transfers','fromColumn':col,'toTable':dim,'toColumn':dcol,'crossFilteringBehavior':'oneDirection'})
measures={
 'Transfers':[
 ('Transfer records','COUNTROWS(Transfers)','#,0'),
 ('Reported permanent fees GBP','CALCULATE(SUM(Transfers[quoted_fee_gbp]), Transfers[is_permanent_fee] = 1)','£#,0'),
 ('Reported fee coverage','DIVIDE(SUM(Transfers[has_reported_fee]), [Transfer records])','0.0%'),
 ('Unknown fee records','CALCULATE(COUNTROWS(Transfers), ISBLANK(Transfers[quoted_fee_gbp]))','#,0'),
 ('Permanent fee deals','SUM(Transfers[is_permanent_fee])','#,0')],
 'HistoricalSample':[
 ('Sample fees EUR','SUM(HistoricalSample[transfer_fee])','€#,0'),
 ('Sample median fee EUR','MEDIAN(HistoricalSample[transfer_fee])','€#,0'),
 ('Sample records','COUNTROWS(HistoricalSample)','#,0')],
 'ValuationSample':[
 ('Valuation records','COUNTROWS(ValuationSample)','#,0'),
 ('Listed value EUR','SUM(ValuationSample[tm_value])','€#,0'),
 ('Model estimate EUR','SUM(ValuationSample[fair_value])','€#,0'),
 ('Model gap EUR','[Model estimate EUR] - [Listed value EUR]','€#,0')]
}
for table in model['model']['tables']:
 if table['name'] in measures:table['measures']=[{'name':n,'expression':e,'formatString':fmt} for n,e,fmt in measures[table['name']]]
put('TransferMarket.SemanticModel/model.bim',model)
put('measures.dax','\n\n'.join(f'{table}[{n}] = {e}' for table,ms in measures.items() for n,e,fmt in ms))
pages=[]
def literal(value):return {'expr':{'Literal':{'Value':"'"+value.replace("'","''")+"'"}}}
def projection(table,col,measure=False):return {'field':{('Measure' if measure else 'Column'):{'Expression':{'SourceRef':{'Entity':table}},'Property':col}},'queryRef':f'{table}.{col}','nativeQueryRef':col}
def page(name,title):
 pages.append(name);put(f'TransferMarket.Report/definition/pages/{name}/page.json',{'$schema':schema('page','2.1.0'),'name':name,'displayName':title,'displayOption':'FitToPage','width':1280,'height':860})
 return name
def visual(page,name,title,kind,x,y,w,h,roles):
 v={'$schema':schema('visualContainer','2.12.0'),'name':name,'position':{'x':x,'y':y,'z':len(list((P/f'TransferMarket.Report/definition/pages/{page}').glob('visuals/*'))),'width':w,'height':h,'tabOrder':0},'visual':{'visualType':kind,'query':{'queryState':{role:{'projections':[projection(*p) for p in fields]} for role,fields in roles.items()}},'visualContainerObjects':{'title':[{'properties':{'show':{'expr':{'Literal':{'Value':'true'}}},'text':literal(title)}}]}}}
 put(f'TransferMarket.Report/definition/pages/{page}/visuals/{name}/visual.json',v)
pg=page('summer','Summer 2026 | source snapshot · GBP')
for i,(m,t) in enumerate([('Transfer records','Transfer records'),('Reported permanent fees GBP','Reported permanent fees · GBP'),('Reported fee coverage','Positive reported fee coverage')]):visual(pg,'kpi'+str(i),t,'card',24+i*310,20,294,110,{'Values':[('Transfers',m,True)]})
visual(pg,'leaguefilter','Destination league','slicer',970,20,286,110,{'Values':[('DestinationLeague','League')]})
visual(pg,'leaguefees','Reported permanent fees by destination league · GBP','clusteredBarChart',24,150,602,280,{'Category':[('DestinationLeague','League')],'Y':[('Transfers','Reported permanent fees GBP',True)]})
visual(pg,'position','Transfer records by position','clusteredBarChart',646,150,610,280,{'Category':[('Transfers','position')],'Y':[('Transfers','Transfer records',True)]})
visual(pg,'timeline','Announcement timing · source coverage','lineChart',24,450,602,230,{'Category':[('Transfers','announcement_month')],'Y':[('Transfers','Transfer records',True)]})
visual(pg,'status','Fee disclosure status','clusteredBarChart',646,450,610,230,{'Category':[('Transfers','fee_status')],'Y':[('Transfers','Transfer records',True)]})
visual(pg,'detail','Transfer detail · quoted fees may include add-ons','tableEx',24,700,1232,140,{'Values':[('Transfers',k) for k in ['player_name','from_club','to_club','transfer_type','quoted_fee_gbp','quote_basis']]})
pg=page('historical','Historical | selected 200 high-fee records · EUR')
for i,m in enumerate(['Sample records','Sample fees EUR','Sample median fee EUR']):visual(pg,'kpi'+str(i),m,'card',24+i*410,20,390,110,{'Values':[('HistoricalSample',m,True)]})
visual(pg,'positions','Sample fees by position · EUR','clusteredBarChart',24,150,602,310,{'Category':[('HistoricalSample','position')],'Y':[('HistoricalSample','Sample fees EUR',True)]})
visual(pg,'clubfilter','Destination club','slicer',646,150,610,130,{'Values':[('HistoricalSample','to_club_name')]})
visual(pg,'details','Selected sample · not the full historical market','tableEx',24,490,1232,340,{'Values':[('HistoricalSample',k) for k in ['player_name','from_club_name','to_club_name','transfer_date','transfer_fee','mv_at_transfer','fee_to_mv']]})
pg=page('valuation','Valuation | 150-row model sample · exploratory')
for i,m in enumerate(['Valuation records','Listed value EUR','Model estimate EUR']):visual(pg,'kpi'+str(i),m,'card',24+i*410,20,390,110,{'Values':[('ValuationSample',m,True)]})
visual(pg,'gap','Model gap by position · EUR · unvalidated model','clusteredBarChart',24,150,602,290,{'Category':[('ValuationSample','position')],'Y':[('ValuationSample','Model gap EUR',True)]})
visual(pg,'filter','Position','slicer',646,150,610,130,{'Values':[('ValuationSample','position')]})
visual(pg,'details','Listed values and existing model estimates · not sale prices','tableEx',24,470,1232,360,{'Values':[('ValuationSample',k) for k in ['player_name','current_club_name','position','tm_value','fair_value','tm_to_fair','minutes']]})
put('TransferMarket.Report/definition/pages/pages.json',{'$schema':schema('pagesMetadata','1.1.0'),'pageOrder':pages,'activePageName':'summer'})
put('README.md','''# Power BI report

Open `TransferMarket.pbip` with Power BI Desktop, then choose Refresh. The native report has three pages,
12 DAX measures, typed Power Query imports, and two dimension-to-fact relationships.
Blank ProjectRoot uses an embedded copy of the processed CSV snapshot so the project is portable.
To refresh from your files, run the Python pipeline, set the ProjectRoot parameter to your repository folder
(use forward slashes), and refresh Power BI. Embedded snapshots remain unchanged until regenerated.

The report is authored as PBIP/PBIR and TMSL model files, not a PBIX binary.
Definition files are checked against Microsoft schemas; native Desktop visual rendering and DAX execution
must be verified before describing the dashboard as fully tested. No screenshot here is claimed to be a Desktop capture.

Summer fee metrics exclude loans and never mix GBP with EUR. Destination-league filters apply to the
summer page. Historical and valuation pages use independent selected samples.
See `../docs/METHODOLOGY.md` for missing sources and interpretation limits.

Format reference: https://learn.microsoft.com/en-us/power-bi/developer/projects/projects-report
Model reference: https://learn.microsoft.com/en-us/power-bi/developer/projects/projects-dataset
''')
print('Native PBIP report built: 3 pages;',sum(1 for _ in P.rglob('visual.json')),'visuals.')
