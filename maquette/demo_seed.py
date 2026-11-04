"""Fictional data only: never use marketplace imports generated from this demo."""
import base64
import hashlib
from io import BytesIO
from zipfile import ZipFile, ZipInfo, ZIP_DEFLATED
from xml.sax.saxutils import escape


def example_template(codes, labels):
    ns = 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'
    def col(index):
        result = ''
        while index:
            index, remainder = divmod(index - 1, 26)
            result = chr(65 + remainder) + result
        return result
    def sheet(rows):
        cells = []
        for index, row in enumerate(rows, 1):
            values = ''.join(f'<c r="{col(i)}{index}" t="inlineStr"><is><t>{escape(value)}</t></is></c>' for i, value in enumerate(row, 1))
            cells.append(f'<row r="{index}">{values}</row>')
        return f'<worksheet xmlns="{ns}"><sheetData>{"".join(cells)}</sheetData></worksheet>'
    files = {
        '[Content_Types].xml': '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/><Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/><Override PartName="/xl/worksheets/sheet1.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/></Types>',
        '_rels/.rels': '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/></Relationships>',
        'xl/workbook.xml': f'<workbook xmlns="{ns}" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"><sheets><sheet name="Data" sheetId="1" r:id="rId1"/></sheets></workbook>',
        'xl/_rels/workbook.xml.rels': '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet1.xml"/></Relationships>',
        'xl/worksheets/sheet1.xml': sheet([labels, codes]),
    }
    stream = BytesIO()
    with ZipFile(stream, 'w') as archive:
        for name, content in files.items():
            info = ZipInfo(name, (1980, 1, 1, 0, 0, 0))
            info.compress_type = ZIP_DEFLATED
            archive.writestr(info, content.encode('utf-8'))
    return stream.getvalue()


def demonstration():
    samples = [
        ('DEMO-A001', 'Casque audio · Modèle A', 'Audio', 'A', ''),
        ('DEMO-B002', 'Bouilloire · Modèle B', 'Petit électroménager', 'B', 'Bouilloire fictive pour découvrir l’éditeur de contenu.'),
        ('DEMO-C003', 'Station d’énergie · Modèle C', 'Énergie', 'C', ''),
        ('DEMO-D004', 'Montre de sport · Modèle D', 'Objets connectés', 'D', 'Montre fictive utilisée uniquement pour illustrer la navigation.'),
        ('DEMO-E005', 'Aspirateur robot · Modèle E', 'Entretien', 'E', ''),
        ('DEMO-F006', 'Sac de voyage · Modèle F', 'Bagagerie', 'F', 'Sac fictif : caractéristiques techniques à compléter.'),
    ]
    products = []
    for sku, name, family, model, description in samples:
        products.append(dict(reference=sku, ean='', name=name, brand='Marque démo', model=model,
                             product_type=family, description_html=description,
                             short_description_original='Article fictif de démonstration.',
                             image_1='', weight='', attr_hauteur='', attr_largeur=''))
    codes = ['category', 'product_id', 'product_title', 'description', 'brand', 'ean', 'color']
    labels = ['Catégorie', 'Référence interne', 'Titre', 'Description', 'Marque', 'EAN', 'Couleur']
    template = example_template(codes, labels)
    matrices = []
    for platform in ['Boulanger', 'Decathlon', 'Orange']:
        attrs = [dict(code=code, label=label,
                      description='Exemple fictif pour découvrir les correspondances. Importer la vraie matrice avant toute préparation produit.',
                      example='', status='REQUIRED' if index < 5 else 'OPTIONAL')
                 for index, (code, label) in enumerate(zip(codes, labels))]
        matrices.append(dict(platform=platform, file=f'DEMONSTRATION_{platform}.xlsx', demo=True,
                             categories=[dict(name='DÉMONSTRATION / Exemple de catégorie', attributes=attrs)],
                             codes=codes, labels=labels, options={}, sheetPath='xl/worksheets/sheet1.xml',
                             revision=hashlib.sha256(template).hexdigest(),
                             template=base64.b64encode(template).decode('ascii')))
    return dict(demo=True, filename='CATALOGUE_DEMONSTRATION — données fictives', sheet='Démonstration',
                headers=list(products[0]), products=products, matrices=matrices, optionSets={})
