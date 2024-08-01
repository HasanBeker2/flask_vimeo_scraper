from flask import Flask, request, render_template, send_file  # Import send_file
import requests
from bs4 import BeautifulSoup
import csv
import re
import io
import os

app = Flask(__name__)

def find_vimeo_links(url):
    try:
        response = requests.get(url)
        if response.status_code != 200:
            return []

        soup = BeautifulSoup(response.content, 'html.parser')
        vimeo_links = []

        for iframe in soup.find_all('iframe'):
            src = iframe.get('src')
            if src and 'vimeo.com' in src:
                vimeo_links.append(src)

        vimeo_direct_links = re.findall(r'https://vimeo.com/\d+', response.text)
        vimeo_links.extend(vimeo_direct_links)

        return vimeo_links
    except Exception as e:
        return []

@app.route('/', methods=['GET', 'POST'])
def index():
    vimeo_links = []
    if request.method == 'POST':
        url = request.form['url']
        vimeo_links = find_vimeo_links(url)
        if 'download' in request.form:
            output = io.StringIO()
            writer = csv.writer(output)
            writer.writerow(['page_url', 'vimeo_link'])
            for link in vimeo_links:
                writer.writerow([url, link])
            output.seek(0)
            return send_file(io.BytesIO(output.getvalue().encode()), 
                             mimetype='text/csv', 
                             as_attachment=True, 
                             download_name='vimeo_links.csv')
    return render_template('index.html', vimeo_links=vimeo_links)

# if __name__ == '__main__':
#     app.run(debug=True)
    
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

