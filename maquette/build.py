"""Assemble a standalone UI; keep all private inputs and outputs outside Git."""
import argparse
import base64
import json
import hashlib
from io import BytesIO
from pathlib import Path
from zipfile import ZipFile
from xml.etree import ElementTree as E

NS={'s':'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}

def workbook(blob, include_reference=False):
    with ZipFile(BytesIO(blob)) as z:
        strings=[''.join(t.text or '' for t in si.iterfind('.//s:t',NS)) for si in E.fromstring(z.read('xl/sharedStrings.xml')).findall('s:si',NS)] if 'xl/sharedStrings.xml' in z.namelist() else []
        rels={r.get('Id'):r.get('Target') for r in E.fromstring(z.read('xl/_rels/workbook.xml.rels'))}
        sheets={}
        for sh in E.fromstring(z.read('xl/workbook.xml')).find('s:sheets',NS):
            target=rels[sh.get('{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id')]
            target=target.lstrip('/') if target.startswith('/') else 'xl/'+target
            if sh.get('name')=='ReferenceData' and not include_reference:
                continue
            rows=[]
            for row in E.fromstring(z.read(target)).findall('s:sheetData/s:row',NS):
                cells={}
                for c in row.findall('s:c',NS):
                    index=0
                    for char in ''.join(ch for ch in c.get('r','') if ch.isalpha()):index=index*26+ord(char)-64
                    v=c.find('s:v',NS)
                    value=v.text if v is not None else ''.join(t.text or '' for t in c.iterfind('.//s:t',NS))
                    if c.get('t')=='s' and value:value=strings[int(value)]
                    cells[index-1]=value or ''
                if any(v.strip() for v in cells.values()):rows.append([cells.get(i,'') for i in range(max(cells)+1)])
            sheets[sh.get('name')]=rows
        return sheets

def seed(catalogue,matrices):
    raw=workbook(Path(catalogue).read_bytes())
    sheet,rows=next(iter(raw.items()))
    headers=rows[0]
    products=[dict(zip(headers,row+['']*(len(headers)-len(row)))) for row in rows[1:]]
    result={'filename':Path(catalogue).name,'sheet':sheet,'headers':headers,'products':products,'matrices':[],'optionSets':{}}
    for platform,filename in matrices:
        with ZipFile(filename) as archive:
            for name in archive.namelist():
                if not name.lower().endswith('.xlsx'):continue
                blob=archive.read(name)
                sheets=workbook(blob, include_reference=True);columns=sheets['Columns'];categories=[]
                # Orange sometimes inserts a variant-axis column before the category columns.
                for i,category in enumerate(columns[0][4:],4):
                    if not category or category.strip().casefold() in ('axe de variant','variant axis'):continue
                    attrs=[]
                    for row in columns[1:]:
                        padded=row+['']*max(0,i+1-len(row))
                        attrs.append({'code':padded[0],'label':padded[1],'description':padded[2], 'example':padded[3],'status':padded[i]})
                    if any(a['status'] in ('REQUIRED','OPTIONAL','RECOMMENDED') for a in attrs):categories.append({'name':category,'attributes':attrs})
                options={}
                reference=sheets.get('ReferenceData',[])
                if reference:
                    for col,code in enumerate(reference[0]):
                        if not code:continue
                        values=list(dict.fromkeys(r[col] for r in reference[1:] if len(r)>col and r[col]))
                        if not values:continue
                        key=hashlib.sha256(json.dumps(values,ensure_ascii=False).encode()).hexdigest()[:24]
                        result['optionSets'][key]=values
                        options[code]=key
                data=sheets['Data']
                with ZipFile(BytesIO(blob)) as template:
                    rels={r.get('Id'):r.get('Target') for r in E.fromstring(template.read('xl/_rels/workbook.xml.rels'))}
                    sh=next(x for x in E.fromstring(template.read('xl/workbook.xml')).find('s:sheets',NS) if x.get('name')=='Data')
                    target=rels[sh.get('{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id')]
                    sheet_path=target.lstrip('/') if target.startswith('/') else 'xl/'+target
                result['matrices'].append({'platform':platform,'file':Path(name).name,'categories':categories,'codes':data[1], 'labels':data[0], 'options':options,'sheetPath':sheet_path,'revision':hashlib.sha256(blob).hexdigest(),'template':base64.b64encode(blob).decode('ascii')})
    return result

def build(args):
    root=Path(__file__).parent
    html=(root/'index.html').read_text()
    html=html.replace('/* APP_STYLES */',(root/'style.css').read_text())
    html=html.replace('LOGO_DATA','data:image/png;base64,'+base64.b64encode((root.parent/'design/lick/logo.png').read_bytes()).decode())
    for src in ['reader.js','xlsx-export.js','app.js','hub.js']:
        html=html.replace(f'<script src="{src}"></script>','<script>\n'+(root/src).read_text().replace('</script','<\\/script')+'\n</script>')
    data=seed(args.catalogue,[(p,Path(f)) for p,f in [('Boulanger',args.boulanger),('Decathlon',args.decathlon),('Orange',args.orange)] if f]) if args.catalogue else {'filename':'','headers':[],'products':[],'matrices':[]}
    encoded=json.dumps(data,ensure_ascii=False).replace('<','\\u003c').replace('>','\\u003e').replace('&','\\u0026')
    html=html.replace('INITIAL_DATA',encoded)
    Path(args.output).parent.mkdir(parents=True,exist_ok=True)
    Path(args.output).write_text(html)
    print(json.dumps({'articles':len(data['products']),'matrices':len(data['matrices']),'categories':{p:len({c['name'] for m in data['matrices'] if m['platform']==p for c in m['categories']}) for p in ['Boulanger','Decathlon','Orange']}},ensure_ascii=False))

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--orange');p.add_argument('--catalogue');p.add_argument('--boulanger');p.add_argument('--decathlon');p.add_argument('--output',required=True)
    build(p.parse_args())
