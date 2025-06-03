import requests
from bs4 import BeautifulSoup

# Hacker news thread URL
def scrap_comments(url):
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
                    return
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
                    })
    
    return comments_list


scrap_comments('https://news.ycombinator.com/item?id=44159528')