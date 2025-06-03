# Hacker News Comment Scraper

A simple web application to scrape and manage comments from Hacker News threads. Features include marking comments as read/unread and tracking new comments with dividers when re-scraping the same URL.

## Features

- 🔍 **Scrape Comments**: Extract top-level comments from any Hacker News thread
- ✅ **Mark as Read**: Keep track of which comments you've read
- 🔄 **Re-scraping**: Add new comments with dividers when scraping the same URL again
- 💾 **Persistent Storage**: Comments are saved locally in JSON format
- 📱 **Responsive Design**: Works on desktop and mobile devices
- 🎨 **Modern UI**: Clean, intuitive interface with smooth interactions

## Installation

1. **Clone or navigate to the project directory**:
   ```bash
   cd /path/to/HN-Scrapper
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   python app.py
   ```

4. **Open your browser** and go to:
   ```
   http://localhost:5000
   ```

## Usage

### Scraping Comments

1. **Enter a Hacker News URL** in the input field (e.g., `https://news.ycombinator.com/item?id=123456`)
2. **Click "Scrape Comments"** to fetch all top-level comments
3. **View the results** in the comments section below

### Managing Comments

- **Mark as Read**: Click the "Mark Read" button on any comment
- **Mark as Unread**: Click "Mark Unread" to revert the status
- **View Stats**: See total, read, and unread comment counts in the header

### Re-scraping

When you enter the same URL again:
- New comments will be added below a divider showing the timestamp
- Existing comments remain with their read/unread status
- Only truly new comments are added (duplicates are filtered out)

## File Structure

```
HN-Scrapper/
├── app.py              # Flask backend application
├── scrapper.py         # Original scraper (legacy)
├── requirements.txt    # Python dependencies
├── README.md          # This file
├── templates/
│   └── index.html     # Frontend HTML template
└── comments_data.json # Auto-generated data storage (created on first use)
```

## API Endpoints

The backend provides several REST API endpoints:

- `GET /` - Serve the main HTML page
- `POST /scrape` - Scrape comments from a URL
- `POST /mark_read` - Mark a comment as read/unread
- `POST /get_comments` - Retrieve existing comments for a URL

## Data Storage

Comments are stored in `comments_data.json` with the following structure:

```json
{
  "url_hash": {
    "url": "original_url",
    "comments": [
      {
        "id": "comment_id",
        "text": "comment_text",
        "author": "username",
        "read": false,
        "timestamp": "2024-01-01T12:00:00",
        "is_divider": false
      }
    ],
    "first_scraped": "2024-01-01T12:00:00",
    "last_scraped": "2024-01-01T12:00:00"
  }
}
```

## Technical Details

- **Backend**: Flask (Python)
- **Frontend**: Vanilla HTML/CSS/JavaScript
- **Scraping**: BeautifulSoup4 with requests
- **Storage**: JSON file-based persistence
- **Styling**: Modern CSS with gradients and responsive design

## Troubleshooting

### Common Issues

1. **"No comments found"**:
   - Verify the URL is a valid Hacker News thread
   - Check if the thread has any top-level comments
   - Ensure you have internet connectivity

2. **"Network error"**:
   - Check if the Flask server is running
   - Verify the server is accessible at `localhost:5000`
   - Check for firewall or proxy issues

3. **Comments not persisting**:
   - Ensure the application has write permissions in the directory
   - Check if `comments_data.json` is being created

### Development

To run in development mode with debug enabled:

```bash
export FLASK_ENV=development
python app.py
```

## Contributing

Feel free to submit issues, feature requests, or pull requests to improve the application.

## License

This project is open source and available under the MIT License. 