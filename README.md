
# URL Crawler and Checker

Welcome to the URL Crawler and Checker project! This Flask-based web application, styled with Bulma, provides  tools to analyze and manage URLs on any website.

## Features

### 1. URL Site Crawler

The URL Site Crawler tool allows you to:
- **Crawl any website** and retrieve all URLs/links.
- **Categorize** the links into internal, external, and broken links.
- **Download results** as an Excel file.
- **Generate sitemap.xml** from internal links.

You can access this feature via the web interface at the root path `/` or through the command line.

**Command-line Usage:**
```bash
python csitche.py scrape -u <web-URL> -o <json-file-path-output>
```

### 2. URL Checker

The URL Checker tool lets you:
- **Verify** if a URL is active, redirected, or returns an error.
- Input URLs manually and receive instant feedback on their status.

## Installation

To get started with this project, follow the steps below:

1. **Clone the repository:**
   ```bash
   git clone https://github.com/aodihis/url-crawler-checker.git
   cd url-crawler-checker
   ```

2. **Create a virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install the required packages:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Flask application:**
   ```bash
   python app.py
   ```

## Usage

Once the application is running, you can access the URL Site Crawler via `http:\\localhost:5000` Use the web interface to input your desired website URL and explore the crawled links.

For command-line usage, use the following command to save the crawled URLs as a JSON file:

```bash
python csitche.py scrape -u <web-URL> -o <json-file-path-output>
```

## Technologies Used

- **Flask**: A lightweight WSGI web application framework in Python.
- **Bulma**: A modern CSS framework based on Flexbox.
