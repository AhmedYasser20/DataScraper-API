# DataScraper API

## Overview
DataScraper API is a lightweight web service that scrapes location-based data from online maps. The backend performs the scraping process and provides an API to fetch the data in CSV format.

## Features
- Scrapes location-based data such as name, address, phone, website, reviews, and rating.
- API endpoint to trigger the scraping process dynamically.
- Returns data in CSV format for easy use.

## Installation
1. Clone the repository:
   ```sh
   git clone https://github.com/yourusername/datascraper-api.git
   cd datascraper-api
   ```
2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
3. Run the Flask server:
   ```sh
   python app.py
   ```

## API Usage
### Download CSV
**Endpoint:**
```
GET /download_csv
```
**Query Parameters:**
- `search_keyword` (string, default: "Marketing Agencies in Dubai")
- `max_businesses` (integer, default: 20)

**Example Request:**
```
GET http://localhost:5000/download_csv?search_keyword=Restaurants+in+Cairo&max_businesses=50
```

**Response:**
A CSV file containing the scraped data.

## Dependencies
- Flask
- Selenium
- Pandas

