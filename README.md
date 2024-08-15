# Vimeo Link Scraper Application

This project is a Flask application that scrapes embedded Vimeo videos from a web page, lists them, and provides an option to download these links as a CSV file. The application is deployed on Google Cloud Platform (GCP) and integrated into a WordPress site using the Divi theme.

## Project Overview

The steps outlined below will guide you through creating a Flask application, deploying it on GCP, and embedding it in a WordPress site with Divi.

### Step 1: Setting Up the Flask Application

1. **Create Project Directory**:
   ```bash
   mkdir flask_vimeo_scraper
   cd flask_vimeo_scraper
   ```

2. **Create and Activate Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # For Windows: venv\Scripts\activate
   ```

3. **Install Required Packages**:
   ```bash
   pip install Flask requests beautifulsoup4 gunicorn
   ```

4. **Create `app.py`**:
   ```python
   import os
   from flask import Flask, request, render_template, send_file
   import requests
   from bs4 import BeautifulSoup
   import csv
   import re
   import io

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

   if __name__ == '__main__':
       app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
   ```

5. **Create `requirements.txt`**:
   ```bash
   pip freeze > requirements.txt
   ```

6. **Create `app.yaml`**:
   Create an `app.yaml` file in the project directory with the following content:
   ```yaml
   runtime: python310  # Using Python 3.10

   entrypoint: gunicorn -b :$PORT app:app

   handlers:
   - url: /.*
     script: auto
   ```

7. **Create `templates/index.html`**:
   Create a folder named `templates` and inside it, create a file named `index.html` with the following content:
   ```html
   <!doctype html>
   <html lang="en">
     <head>
       <meta charset="utf-8">
       <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
       <title>Vimeo Link Scraper</title>
       <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
     </head>
     <body>
       <div class="container">
         <h1 class="mt-5">Vimeo Link Scraper</h1>
         <form method="post" class="mt-3">
           <div class="form-group">
             <label for="url">Enter the URL:</label>
             <input type="url" class="form-control" id="url" name="url" required>
           </div>
           <button type="submit" class="btn btn-primary">Get Vimeo Links</button>
         </form>

         {% if vimeo_links %}
           <h2 class="mt-5">Found Vimeo Links:</h2>
           <ul class="list-group mt-3">
             {% for link in vimeo_links %}
               <li class="list-group-item">
                 <a href="{{ link }}" target="_blank">{{ link }}</a>
               </li>
             {% endfor %}
           </ul>
           <form method="post" class="mt-3">
             <input type="hidden" name="url" value="{{ request.form['url'] }}">
             <button type="submit" name="download" class="btn btn-success">Download CSV</button>
           </form>
         {% endif %}
       </div>
     </body>
   </html>
   ```

### Step 2: Deploying the Application on Google Cloud Platform

1. **Install Google Cloud SDK**:
   - Download and install the SDK from [Google Cloud SDK](https://cloud.google.com/sdk/docs/install).

2. **Configure Google Cloud SDK**:
   ```bash
   gcloud init
   ```

3. **Create a New Project**:
   - Go to the Google Cloud Console and create a new project. Note down the Project ID.

4. **Set Project ID**:
   ```bash
   gcloud config set project YOUR_PROJECT_ID
   ```

5. **Deploy the Application**:
   ```bash
   gcloud app deploy
   ```

6. **Launch and Test the Application**:
   ```bash
   gcloud app browse
   ```

### Step 3: Embedding the Application in a WordPress Site

1. **Log in to WordPress Admin Panel**:
   - Log in to your WordPress admin panel (`https://hasanbeker.com/wp-admin`).

2. **Create a New Page or Post**:
   - Navigate to "Pages" or "Posts" in the left menu and click "Add New".

3. **Use Divi Builder to Edit the Page**:
   - Click on "Use The Divi Builder".
   - Choose "Start Building".

4. **Add IFrame Code Using Divi Builder**:
   - Add a new row.
   - Add a Text Module to the row.
   - In the Text Module settings, switch to the "Text" tab and insert the following iframe code:

   ```html
   <iframe src="https://your-project-id.ue.r.appspot.com" width="100%" height="800"></iframe>
   ```
   - Replace `your-project-id.ue.r.appspot.com` with your actual application URL.

5. **Publish the Page**:
   - Save and publish the page.

6. **Check the Published Page**:
   - Visit the published page to ensure the Flask application is embedded correctly in an iframe.

## Summary

By following these steps, you can successfully create a Flask application, deploy it on Google Cloud Platform, and integrate it into your WordPress site using the Divi theme. This setup allows users to search for Vimeo videos and download the links in a CSV format directly from your WordPress site. If you encounter any issues or need further assistance, feel free to reach out. Good luck!

