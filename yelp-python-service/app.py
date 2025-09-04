# Simplified Python Yelp Scraping Service for Railway Deployment
from flask import Flask, request, jsonify
import requests
import json
import time
import random
import os
from urllib.parse import urlencode
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

def get_fresh_cookies():
    """Get fresh cookies - update these periodically"""
    return {
        'hl': 'en_US',
        'wdi': '2|953FC3FFAE03AAD2|0x1.a1fd9481c7f6bp+30|80787e7f360789eb',
        'bse': 'fef6d6fe2fe44fa69be5d9dcd396b4ae',
        '_gcl_au': '1.1.1850127271.1753179426',
        'spses.5f33': '*',
        '_ga': 'GA1.2.953FC3FFAE03AAD2',
        'g_state': '{"i_t":1753269042609,"i_l":0}',
        '_uetsid': '061e3c0066e511f0b3c00fe8774a2211',
        '_uetvid': '061e738066e511f08f70277d66ffec55',
        '__adroll_fpc': '11fa207052bcddcc2bdbf69c3cfed1b7-1753182708151',
        '_fbp': 'fb.1.1753182710726.431624590298200515',
        'adc': 'Uwixn8SsCURqEoKy56frqg%3A1h8zUV304HzSdycKLmBKrQ%3A1753183925',
        'xcj': '1|WrZNxMklu_OOOhL3eSNQp2eQxQRl55RncFghEANGxvE',
        'recentlocations': 'San+Francisco%2C+CA%3B%3BSan+Francisco%2C+CA%2C+United+States%3B%3BChicago%2C+IL%2C+United+States%3B%3B',
        'location': '%7B%22accuracy%22%3A+4%2C+%22county%22%3A+%22San+Francisco+County%22%2C+%22min_longitude%22%3A+-122.51781463623047%2C+%22address1%22%3A+%22%22%2C+%22min_latitude%22%3A+37.706368356809776%2C+%22city%22%3A+%22San+Francisco%22%2C+%22latitude%22%3A+37.775123%2C+%22location_type%22%3A+%22locality%22%2C+%22state%22%3A+%22CA%22%2C+%22country%22%3A+%22US%22%2C+%22place_id%22%3A+%221237%22%2C+%22parent_id%22%3A+371%2C+%22address2%22%3A+%22%22%2C+%22max_longitude%22%3A+-122.3550796508789%2C+%22zip%22%3A+%22%22%2C+%22display%22%3A+%22San+Francisco%2C+CA%22%2C+%22unformatted%22%3A+%22San+Francisco%2C+CA%22%2C+%22longitude%22%3A+-122.41932%2C+%22max_latitude%22%3A+37.81602226140252%2C+%22provenance%22%3A+%22YELP_GEOCODING_ENGINE%22%2C+%22address3%22%3A+%22%22%2C+%22borough%22%3A+%22%22%2C+%22confident%22%3A+null%2C+%22isGoogleHood%22%3A+false%2C+%22language%22%3A+null%2C+%22neighborhood%22%3A+%22%22%2C+%22polygons%22%3A+null%2C+%22usingDefaultZip%22%3A+false%7D',
        'datadome': 'XNgC1V8IobrQ9G6SWpSLNnomdMDyNxwrWePEst5gAYe_qIeS5qC67OC2ZbI_AoHAOQrY~So6~ht7fJVPQWC~qiieSh~Fi1pqtvFRq8cMlvSS6lhYrbhUgn5qd1av3lnQ',
        '_ga_K9Z2ZEVC8C': 'GS2.2.s1753179427$o1$g1$t1753184021$j19$l0$h0',
        '__ar_v4': 'BHPKS4B4ONEJJMGH4QCJZR%3A20250721%3A15%7CQB5JPFIKRZDSBOZSULG4YB%3A20250721%3A15%7C7YX6SJQ4RZAMPB6LZ7CHFF%3A20250721%3A15',
        'bsi': '1%7Cc5aa68da-09e8-518d-a042-5bbb6d93b452%7C1753184026263%7C1753179424447%7C1%7C6ec15984561dd62a',
        'spid.5f33': '8c702fc5-8413-4601-ac23-9efde710301e.1753179428.1.1753184045..5086d705-a47c-4b17-a6e8-0d8fc67cd588..6197e310-00e7-4224-9b96-55ea586e096c.1753179427884.137',
        'OptanonConsent': 'isGpcEnabled=0&datestamp=Tue+Jul+22+2025+17%3A04%3A15+GMT%2B0530+(India+Standard+Time)&version=202403.1.0&browserGpcFlag=0&isIABGlobal=false&identifierType=Cookie+Unique+Id&hosts=&consentId=8a9cdd03-c8ed-4882-81ac-48a968877799&interactionCount=1&isAnonUser=1&landingPath=https%3A%2F%2Fwww.yelp.com%2Fsearch%3Ffind_desc%3Dsoftware+company%26find_loc%3DChicago%252C+IL%252C+United+States&groups=BG122%3A1%2CC0003%3A1%2CC0002%3A1%2CC0001%3A1%2CC0004%3A1',
    }

def get_headers():
    """Get request headers"""
    return {
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'no-cache',
        'pragma': 'no-cache',
        'priority': 'u=1, i',
        'referer': 'https://www.yelp.com/',
        'sec-ch-device-memory': '8',
        'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
        'sec-ch-ua-arch': '"x86"',
        'sec-ch-ua-full-version-list': '"Not)A;Brand";v="8.0.0.0", "Chromium";v="138.0.7204.158", "Google Chrome";v="138.0.7204.158"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-model': '""',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
    }

def scrape_yelp_page(query, location, start=0):
    """Scrape a single Yelp page"""
    try:
        params = {
            'find_desc': query,
            'find_loc': location,
            'start': str(start),
            'parent_request_id': f'{random.randint(100000, 999999)}',
            'request_origin': 'user',
        }
        
        url = 'https://www.yelp.com/search/snippet'
        
        # Create session for better cookie handling
        session = requests.Session()
        session.cookies.update(get_fresh_cookies())
        
        logger.info(f"🔍 Scraping Yelp page {start} for '{query}' in '{location}'")
        
        response = session.get(
            url,
            params=params,
            headers=get_headers(),
            timeout=30
        )
        
        logger.info(f"📊 Response status: {response.status_code}")
        
        if response.status_code == 403:
            logger.warning("⚠️ Got 403 - cookies may be expired or blocked")
            return []
        
        if response.status_code != 200:
            logger.warning(f"⚠️ Unexpected status code: {response.status_code}")
            return []
        
        # Try to parse JSON response
        try:
            data = response.json()
            logger.info("✅ Successfully parsed JSON response")
        except json.JSONDecodeError:
            logger.warning("⚠️ Response is not valid JSON - may be blocked")
            return []
        
        # Extract business data
        leads = []
        
        # Navigate to business data
        main_content = data.get('searchPageProps', {}).get('mainContentComponentsListProps', [])
        
        if not main_content:
            logger.warning("⚠️ No mainContentComponentsListProps found")
            return []
        
        for item in main_content:
            if 'searchResultBusiness' in item:
                business = item['searchResultBusiness']
                
                try:
                    alias = business.get('alias', '')
                    name = business.get('name', 'Unknown Business')
                    phone = business.get('phone', '')
                    rating = business.get('rating', 0)
                    review_count = business.get('reviewCount', 0)
                    product_url = f'https://www.yelp.com/biz/{alias}' if alias else ''
                    
                    # Extract location info
                    location_info = business.get('location', {})
                    address = location_info.get('address1', '')
                    city = location_info.get('city', '')
                    state = location_info.get('state', '')
                    
                    # Extract categories
                    categories = business.get('categories', [])
                    category_names = [cat.get('title', '') for cat in categories]
                    
                    lead_data = {
                        'name': name,
                        'phone': phone,
                        'company': name,
                        'source': 'Yelp',
                        'email': None,
                        'notes': f'Rating: {rating}/5.0 ({review_count} reviews), Categories: {", ".join(category_names)}, Address: {address}, {city}, {state}, Profile URL: {product_url}',
                        'status': 'new',
                        'rating': rating,
                        'review_count': review_count,
                        'categories': category_names,
                        'address': f'{address}, {city}, {state}',
                        'profile_url': product_url
                    }
                    
                    leads.append(lead_data)
                    logger.info(f"✅ Extracted: {name} - {phone}")
                    
                except Exception as e:
                    logger.error(f"❌ Error processing business: {e}")
        
        logger.info(f"✅ Extracted {len(leads)} leads from page {start}")
        return leads
        
    except Exception as e:
        logger.error(f"❌ Error scraping page {start}: {e}")
        return []

def scrape_yelp_multiple_pages(query, location, max_pages=3):
    """Scrape multiple Yelp pages"""
    all_leads = []
    
    for page in range(max_pages):
        start = page * 10
        
        try:
            page_leads = scrape_yelp_page(query, location, start)
            all_leads.extend(page_leads)
            
            if not page_leads:
                logger.info(f"🛑 No results on page {page}, stopping")
                break
            
            # Add delay between pages
            if page < max_pages - 1:
                time.sleep(2)
                
        except Exception as e:
            logger.error(f"❌ Error on page {page}: {e}")
            break
    
    return all_leads

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy", 
        "service": "yelp-python-scraper",
        "timestamp": time.time()
    })

@app.route('/scrape', methods=['POST'])
def scrape_yelp():
    """Main scraping endpoint"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
        
        query = data.get('query', 'Restaurants')
        location = data.get('location', 'San Francisco, CA')
        
        logger.info(f"🍽️ Starting Yelp scrape for: {query} in {location}")
        
        # Scrape multiple pages
        results = scrape_yelp_multiple_pages(query, location, max_pages=3)
        
        logger.info(f"✅ Scraping completed: {len(results)} leads found")
        
        return jsonify({
            "success": True,
            "count": len(results),
            "leads": results,
            "query": query,
            "location": location,
            "source": "Real-time Yelp via Python Service",
            "timestamp": time.time()
        })
        
    except Exception as e:
        logger.error(f"❌ Scraping error: {str(e)}")
        return jsonify({
            "success": False,
            "error": str(e),
            "count": 0,
            "leads": [],
            "timestamp": time.time()
        }), 500

@app.route('/scrape_yelp', methods=['GET'])
def scrape_yelp_get():
    """GET endpoint for easy testing"""
    try:
        query = request.args.get('category', 'Restaurants')
        location = request.args.get('location', 'San Francisco, CA')

        logger.info(f"🍽️ Starting Yelp scrape via GET for: {query} in {location}")

        # Scrape multiple pages
        results = scrape_yelp_multiple_pages(query, location, max_pages=3)

        logger.info(f"✅ Scraping completed: {len(results)} leads found")

        return jsonify({
            "success": True,
            "count": len(results),
            "leads": results,
            "query": query,
            "location": location,
            "source": "Real-time Yelp via Python Service (GET)",
            "timestamp": time.time()
        })

    except Exception as e:
        logger.error(f"❌ GET scraping error: {e}")
        return jsonify({
            "success": False,
            "error": str(e),
            "count": 0,
            "leads": [],
            "timestamp": time.time()
        }), 500

@app.route('/test', methods=['GET'])
def test_endpoint():
    """Test endpoint"""
    return jsonify({
        "message": "🍽️ Yelp Python service is running!",
        "endpoints": {
            "health": "GET /health",
            "scrape": "POST /scrape",
            "scrape_yelp": "GET /scrape_yelp?category=restaurants&location=New York",
            "test": "GET /test"
        },
        "timestamp": time.time()
    })

@app.route('/', methods=['GET'])
def root():
    """Root endpoint"""
    return jsonify({
        "service": "Yelp Python Scraper",
        "status": "running",
        "endpoints": ["/health", "/scrape", "/test"]
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
