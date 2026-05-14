# URL Shortener API (FastAPI + SQLite)

This is a simple URL shortener API built with FastAPI and SQLite.

It allows you to:
- Create short URLs
- Retrieve original URLs
- Track access statistics
- Update or delete URLs

## Features

- Shorten long URLs into a 6-character code
- Redirect to original URL
- Track number of accesses
- Update existing URLs
- Delete URLs
- Lightweight SQLite database (no ORM)

## Tech Stack

- Python
- FastAPI
- SQLite

## API Endpoints

POST /shorten
→ Create a short URL

GET /shorten/{code}
→ Get original URL

GET /shorten/{code}/stats
→ Get access count

PUT /shorten/modify/{code}
→ Update URL

DELETE /shorten/delete/{code}
→ Delete URL

## Example request
POST /shorten

Body:
{
  "url": "https://google.com"
}
