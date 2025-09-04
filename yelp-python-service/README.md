# 🍽️ Yelp Python Scraping Service

Real-time Yelp business data scraping service for Smart Lead Search integration.

## 🚀 **Features**

- ✅ Real-time Yelp business data extraction
- ✅ Flask web service with REST API
- ✅ Multiple page scraping support
- ✅ Structured JSON response format
- ✅ Health monitoring endpoints
- ✅ Production-ready with Gunicorn

## 📡 **API Endpoints**

### `GET /health`
Health check endpoint
```json
{
  "service": "yelp-python-scraper",
  "status": "healthy",
  "timestamp": 1753189407.6213195
}
```

### `POST /scrape`
Main scraping endpoint
```json
{
  "query": "Restaurants",
  "location": "San Francisco, CA"
}
```

**Response:**
```json
{
  "success": true,
  "count": 15,
  "leads": [...],
  "query": "Restaurants",
  "location": "San Francisco, CA",
  "source": "Real-time Yelp via Python Service"
}
```

### `GET /test`
Test endpoint for service verification

## 🛠️ **Local Development**

```bash
# Install dependencies
pip install -r requirements.txt

# Run service
python app.py

# Test endpoints
curl http://localhost:5000/health
curl -X POST http://localhost:5000/scrape \
  -H "Content-Type: application/json" \
  -d '{"query": "Restaurants", "location": "San Francisco, CA"}'
```

## 🚀 **Deployment**

This service is designed for Railway deployment:

1. Connect this repository to Railway
2. Railway auto-detects Python and deploys
3. Service runs on `https://your-app.railway.app`

## 🔧 **Configuration**

Update cookies in `get_fresh_cookies()` function when they expire.

## 📊 **Integration**

This service integrates with Supabase Edge Functions for the Smart Lead Search feature.

## 🎯 **Purpose**

Provides real-time Yelp business data using Python's superior web scraping capabilities while maintaining TypeScript architecture for the main application.
