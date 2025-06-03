from flask import Flask, render_template, request, jsonify
import requests
from bs4 import BeautifulSoup
import json
import os
from datetime import datetime
import hashlib

app = Flask(__name__)

# File to store comments data
DATA_FILE = 'comments_data.json'

def load_data():
    """Load existing comments data from file"""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_data(data):
    """Save comments data to file"""
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def scrap_comments(url):
    """Enhanced scraper function with better comment extraction"""
    response = requests.get(url)
    response.raise_for_status()
    
    soup = BeautifulSoup(response.text, 'html.parser')
    comments = soup.find_all('tr', class_='athing comtr')
    
    comments_list = []
    for comment in comments:
        indent = comment.find('td', class_='ind')
        if indent and indent.get('indent') == '0':
            comment_div = comment.find('div', class_='commtext')
            if comment_div:
                comment_text = '\n\n'.join(str(element) for element in comment_div.stripped_strings)
                if comment_text:
                    print("comment_text", comment_text)
                    # Get comment ID for uniqueness
                    comment_id = comment.get('id', '')
                    # Get author if available
                    author_elem = comment.find('a', class_='hnuser')
                    author = author_elem.get_text() if author_elem else 'Unknown'
                    
                    comments_list.append({
                        'id': comment_id,
                        'text': comment_text,
                        'author': author,
                        'read': False,
                        'timestamp': datetime.now().isoformat()
                    })
    
    return comments_list

@app.route('/')
def index():
    """Serve the main page with existing threads"""
    all_data = load_data()
    threads = []
    for url_hash, data in all_data.items():
        thread_data = {
            'url': data['url'],
            'first_scraped': data['first_scraped'],
            'last_scraped': data['last_scraped'],
            'total_comments': len([c for c in data['comments'] if not c.get('is_divider', False)]),
            'unread_comments': len([c for c in data['comments'] if not c.get('is_divider', False) and not c.get('read', False)])
        }
        threads.append(thread_data)
    
    # Return JSON if requested
    if request.headers.get('Accept') == 'application/json':
        return jsonify({'threads': threads})
    
    return render_template('index.html', threads=threads)

@app.route('/scrape', methods=['POST'])
def scrape_comments():
    """Scrape comments from HN thread URL"""
    try:
        data = request.get_json()
        url = data.get('url', '').strip()
        
        if not url:
            return jsonify({'error': 'URL is required'}), 400
        
        # Generate a hash for the URL to use as key
        url_hash = hashlib.md5(url.encode()).hexdigest()
        
        # Load existing data
        all_data = load_data()
        
        # Scrape new comments
        new_comments = scrap_comments(url)
        
        if url_hash in all_data:
            # URL already exists, add divider and new comments
            existing_comments = all_data[url_hash]['comments']
            
            # Add divider
            divider = {
                'id': f'divider_{datetime.now().timestamp()}',
                'text': f'--- New comments scraped at {datetime.now().strftime("%Y-%m-%d %H:%M:%S")} ---',
                'author': 'System',
                'read': True,
                'timestamp': datetime.now().isoformat(),
                'is_divider': True
            }
            
            # Filter out comments that already exist (by ID)
            existing_ids = {comment['id'] for comment in existing_comments if not comment.get('is_divider')}
            truly_new_comments = [comment for comment in new_comments if comment['id'] not in existing_ids]
            
            if truly_new_comments:
                # Add new comments at the beginning, followed by the divider
                all_data[url_hash]['comments'] = truly_new_comments + [divider] + all_data[url_hash]['comments']
                all_data[url_hash]['last_scraped'] = datetime.now().isoformat()
            else:
                return jsonify({
                    'message': 'No new comments found',
                    'comments': all_data[url_hash]['comments']
                })
        else:
            # New URL
            all_data[url_hash] = {
                'url': url,
                'comments': new_comments,
                'first_scraped': datetime.now().isoformat(),
                'last_scraped': datetime.now().isoformat()
            }
        
        # Save data
        save_data(all_data)
        
        return jsonify({
            'message': f'Successfully scraped {len([c for c in new_comments if not c.get("is_divider")])} comments',
            'comments': all_data[url_hash]['comments']
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/mark_read', methods=['POST'])
def mark_read():
    """Mark a comment as read/unread"""
    try:
        data = request.get_json()
        url = data.get('url', '').strip()
        comment_id = data.get('comment_id', '')
        read_status = data.get('read', True)
        
        if not url or not comment_id:
            return jsonify({'error': 'URL and comment_id are required'}), 400
        
        url_hash = hashlib.md5(url.encode()).hexdigest()
        all_data = load_data()
        
        if url_hash not in all_data:
            return jsonify({'error': 'URL not found'}), 404
        
        # Find and update the comment
        for comment in all_data[url_hash]['comments']:
            if comment['id'] == comment_id:
                comment['read'] = read_status
                break
        
        save_data(all_data)
        return jsonify({'message': 'Comment status updated'})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/get_comments', methods=['POST'])
def get_comments():
    """Get existing comments for a URL"""
    try:
        data = request.get_json()
        url = data.get('url', '').strip()
        
        if not url:
            return jsonify({'error': 'URL is required'}), 400
        
        url_hash = hashlib.md5(url.encode()).hexdigest()
        all_data = load_data()
        
        if url_hash in all_data:
            return jsonify({
                'comments': all_data[url_hash]['comments'],
                'first_scraped': all_data[url_hash].get('first_scraped'),
                'last_scraped': all_data[url_hash].get('last_scraped')
            })
        else:
            return jsonify({'comments': []})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) 