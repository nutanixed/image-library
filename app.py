from flask import Flask, render_template, request, redirect, url_for
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
STORAGE_PATH = '/data'
DOWNLOAD_URL = os.environ.get('DOWNLOAD_URL', '').rstrip('/')
LOGOUT_REDIRECT_URL = os.environ.get('LOGOUT_REDIRECT_URL', '/')

@app.route('/')
def index():
    search_query = request.args.get('search', '').lower()
    show_all = request.args.get('show_all', 'false') == 'true'
    
    # Copied links should target the dedicated high-throughput download server.
    download_base_url = DOWNLOAD_URL if DOWNLOAD_URL else request.host_url.rstrip('/')
    
    files = []
    try:
        for root, dirs, filenames in os.walk(STORAGE_PATH):
            # Exclude logs directory from traversal
            if 'logs' in dirs:
                dirs.remove('logs')
                
            for filename in filenames:
                # Get relative path from STORAGE_PATH
                rel_path = os.path.relpath(os.path.join(root, filename), STORAGE_PATH)
                
                # Skip hidden files unless show_all is set
                if any(part.startswith('.') for part in rel_path.split(os.sep)) and not show_all:
                    continue
                    
                if search_query in rel_path.lower():
                    ext = os.path.splitext(filename)[1][1:].upper() or 'FILE'
                    files.append({
                        'name': rel_path,
                        'ext': ext
                    })
    except Exception as e:
        print(f"Error reading directory: {e}")

    files.sort(key=lambda x: x['name'])
    
    # Categorize by extension for the "grouped" look
    grouped_links = {}
    for f in files:
        cat = f['ext']
        if cat not in grouped_links:
            grouped_links[cat] = []
        grouped_links[cat].append(f)
    
    display_categories = sorted(grouped_links.keys())
    
    return render_template('index.html', 
                           grouped_links=grouped_links, 
                           display_categories=display_categories,
                           total_count=len(files),
                           show_all=show_all,
                           download_base_url=download_base_url)

@app.route('/logout')
def logout():
    return redirect(LOGOUT_REDIRECT_URL)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
