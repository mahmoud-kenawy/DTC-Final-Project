import xml.etree.ElementTree as ET
import urllib.parse
import urllib.request
import base64

def get_base64_img(url):
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            data = response.read()
            b64 = base64.b64encode(data).decode('utf-8')
            if url.endswith('.svg'):
                return f'data:image/svg+xml;base64,{b64}'
            else:
                return f'data:image/png;base64,{b64}'
    except Exception as e:
        print(f'Error downloading {url}: {e}')
        return ''

print('Downloading icons...')
python_img = get_base64_img('https://upload.wikimedia.org/wikipedia/commons/c/c3/Python-logo-notext.svg')
spark_img = get_base64_img('https://upload.wikimedia.org/wikipedia/commons/f/f3/Apache_Spark_logo.svg')

print('Parsing original SVG...')
svg_path = 'docs/DTCFinal.drawio .svg'
tree = ET.parse(svg_path)
svg_root = tree.getroot()

content_str = urllib.parse.unquote(svg_root.attrib['content'])
mxfile = ET.fromstring(content_str)
root = mxfile.find('.//root')

python_id = 'stream_python'
ET.SubElement(root, 'mxCell', {'id': python_id, 'value': '', 'style': f'shape=image;verticalLabelPosition=bottom;labelBackgroundColor=default;verticalAlign=top;aspect=fixed;imageAspect=0;image={python_img};', 'vertex': '1', 'parent': '1'}).append(ET.Element('mxGeometry', {'x': '460', 'y': '380', 'width': '80', 'height': '80', 'as': 'geometry'}))
ET.SubElement(root, 'mxCell', {'id': f'{python_id}_label', 'value': '&lt;b&gt;Python Producer&lt;/b&gt;', 'style': 'text;html=1;align=center;verticalAlign=middle;resizable=0;points=[];', 'vertex': '1', 'parent': '1'}).append(ET.Element('mxGeometry', {'x': '450', 'y': '470', 'width': '100', 'height': '30', 'as': 'geometry'}))

kafka_id = 'stream_kafka'
ET.SubElement(root, 'mxCell', {'id': kafka_id, 'value': '&lt;b&gt;&lt;font style=\"font-size: 15px;\"&gt;Kafka Broker&lt;/font&gt;&lt;/b&gt;', 'style': 'rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;shadow=0;glass=0;', 'vertex': '1', 'parent': '1'}).append(ET.Element('mxGeometry', {'x': '700', 'y': '380', 'width': '100', 'height': '80', 'as': 'geometry'}))

spark_id = 'stream_spark'
ET.SubElement(root, 'mxCell', {'id': spark_id, 'value': '', 'style': f'shape=image;verticalLabelPosition=bottom;labelBackgroundColor=default;verticalAlign=top;aspect=fixed;imageAspect=0;image={spark_img};', 'vertex': '1', 'parent': '1'}).append(ET.Element('mxGeometry', {'x': '900', 'y': '380', 'width': '120', 'height': '60', 'as': 'geometry'}))
ET.SubElement(root, 'mxCell', {'id': f'{spark_id}_label', 'value': '&lt;b&gt;PySpark Consumer&lt;/b&gt;', 'style': 'text;html=1;align=center;verticalAlign=middle;resizable=0;points=[];', 'vertex': '1', 'parent': '1'}).append(ET.Element('mxGeometry', {'x': '910', 'y': '450', 'width': '100', 'height': '30', 'as': 'geometry'}))

ET.SubElement(root, 'mxCell', {'id': 'edge_usgs_python', 'style': 'edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;', 'edge': '1', 'parent': '1', 'source': 'xG334gaVbaBVJ1zQHwoB-15', 'target': python_id}).append(ET.Element('mxGeometry', {'relative': '1', 'as': 'geometry'}))
ET.SubElement(root, 'mxCell', {'id': 'edge_python_kafka', 'style': 'edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;', 'edge': '1', 'parent': '1', 'source': python_id, 'target': kafka_id}).append(ET.Element('mxGeometry', {'relative': '1', 'as': 'geometry'}))
ET.SubElement(root, 'mxCell', {'id': 'edge_kafka_spark', 'style': 'edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;', 'edge': '1', 'parent': '1', 'source': kafka_id, 'target': spark_id}).append(ET.Element('mxGeometry', {'relative': '1', 'as': 'geometry'}))
ET.SubElement(root, 'mxCell', {'id': 'edge_spark_bq', 'style': 'edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;', 'edge': '1', 'parent': '1', 'source': spark_id, 'target': 'xG334gaVbaBVJ1zQHwoB-17'}).append(ET.Element('mxGeometry', {'relative': '1', 'as': 'geometry'}))

bg_box = root.find('.//mxCell[@id=\"xG334gaVbaBVJ1zQHwoB-16\"]')
if bg_box is not None:
    geom = bg_box.find('mxGeometry')
    geom.set('height', '450')

new_content = ET.tostring(mxfile, encoding='unicode')
svg_root.attrib['content'] = urllib.parse.quote(new_content)

viewBox = svg_root.attrib.get('viewBox', '0 0 1129 341').split(' ')
if len(viewBox) == 4:
    viewBox[3] = '600'
    svg_root.attrib['viewBox'] = ' '.join(viewBox)
    svg_root.attrib['height'] = '600px'

tree.write('docs/DTCFinal_Stream.drawio.svg', encoding='UTF-8', xml_declaration=True)
print('Successfully created docs/DTCFinal_Stream.drawio.svg')
