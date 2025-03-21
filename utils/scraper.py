import logging
import random
import re
import requests
from bs4 import BeautifulSoup
import trafilatura
from urllib.parse import quote_plus

def scrape_product_data(device_type, brand, model):
    """
    Scrape product data from multiple sources to gather pricing information.
    
    Args:
        device_type (str): Type of device (phone, laptop, etc.)
        brand (str): Brand name
        model (str): Model name
        
    Returns:
        dict: Dictionary containing scraped pricing data
    """
    logging.info(f"Scraping data for {brand} {model}")
    
    try:
        # Combine sources for better price estimation
        ebay_data = scrape_ebay(device_type, brand, model)
        amazon_data = scrape_amazon(device_type, brand, model)
        
        # Combine the data
        combined_data = {
            "ebay": ebay_data,
            "amazon": amazon_data,
            "average_price": calculate_average_price(ebay_data, amazon_data)
        }
        
        return combined_data
    
    except Exception as e:
        logging.error(f"Error in scraping: {str(e)}")
        # Return fallback data if scraping fails
        return {
            "ebay": {"min_price": 0, "max_price": 0, "avg_price": 0, "listings": 0},
            "amazon": {"min_price": 0, "max_price": 0, "avg_price": 0, "listings": 0},
            "average_price": 0
        }

def scrape_ebay(device_type, brand, model):
    """
    Scrape eBay for pricing data. In a production environment, 
    this would use the eBay API or perform actual web scraping.
    
    For this demo, we'll simulate the scraping process.
    """
    logging.info(f"Scraping eBay for {brand} {model}")
    
    try:
        # In a real implementation, we'd use the eBay API or scrape the website
        # For demo purposes, use a simulated approach with random variation
        query = f"{brand} {model} {device_type}"
        url = f"https://www.ebay.com/sch/i.html?_nkw={quote_plus(query)}"
        
        # Let's use Trafilatura to get some text content for logging purposes
        logging.debug(f"Would scrape URL: {url}")
        
        # Simulate scraping results (in real app, we'd extract this from the page)
        # Base prices adjusted by device type and brand recognition
        base_price = get_base_price(device_type, brand)
        
        # Add some randomness to simulate market variation
        price_variation = base_price * 0.2  # 20% variation
        listings = random.randint(5, 50)
        
        # Generate simulated price data
        min_price = max(10, base_price - price_variation)
        max_price = base_price + price_variation
        avg_price = (min_price + max_price) / 2
        
        return {
            "min_price": round(min_price, 2),
            "max_price": round(max_price, 2),
            "avg_price": round(avg_price, 2),
            "listings": listings
        }
        
    except Exception as e:
        logging.error(f"Error scraping eBay: {str(e)}")
        return {"min_price": 0, "max_price": 0, "avg_price": 0, "listings": 0}

def scrape_amazon(device_type, brand, model):
    """
    Scrape Amazon for pricing data. In a production environment,
    this would use the Amazon API or perform actual web scraping.
    
    For this demo, we'll simulate the scraping process with slightly
    different price points than eBay.
    """
    logging.info(f"Scraping Amazon for {brand} {model}")
    
    try:
        # In a real implementation, we'd use the Amazon API or scrape the website
        query = f"{brand} {model} {device_type}"
        url = f"https://www.amazon.com/s?k={quote_plus(query)}"
        
        logging.debug(f"Would scrape URL: {url}")
        
        # Simulate scraping results (in real app, we'd extract this from the page)
        # Amazon prices tend to be a bit higher than eBay
        base_price = get_base_price(device_type, brand) * 1.1  # 10% higher than eBay
        
        # Add some randomness
        price_variation = base_price * 0.15  # 15% variation
        listings = random.randint(3, 30)
        
        # Generate simulated price data
        min_price = max(15, base_price - price_variation)
        max_price = base_price + price_variation
        avg_price = (min_price + max_price) / 2
        
        return {
            "min_price": round(min_price, 2),
            "max_price": round(max_price, 2),
            "avg_price": round(avg_price, 2),
            "listings": listings
        }
        
    except Exception as e:
        logging.error(f"Error scraping Amazon: {str(e)}")
        return {"min_price": 0, "max_price": 0, "avg_price": 0, "listings": 0}

def get_base_price(device_type, brand):
    """
    Get a base price for a device type and brand.
    This is a simplified approach - in reality, you'd use historical data.
    """
    # Base prices by device type
    device_prices = {
        "smartphone": 300,
        "laptop": 800,
        "tablet": 250,
        "desktop": 700,
        "monitor": 200,
        "tv": 500,
        "camera": 400,
        "headphones": 100,
        "smartwatch": 150,
        "speaker": 120,
    }
    
    # Brand multipliers (premium brands cost more)
    brand_multipliers = {
        "apple": 1.8,
        "samsung": 1.5,
        "google": 1.6,
        "sony": 1.4,
        "microsoft": 1.5,
        "dell": 1.2,
        "hp": 1.1,
        "lenovo": 1.1,
        "asus": 1.1,
        "acer": 0.9,
        "lg": 1.2,
        "bose": 1.6,
        "canon": 1.3,
        "nikon": 1.3
    }
    
    # Get base price for device type (default to 200 if not found)
    base = device_prices.get(device_type.lower(), 200)
    
    # Apply brand multiplier if available
    multiplier = brand_multipliers.get(brand.lower(), 1.0)
    
    return base * multiplier

def calculate_average_price(ebay_data, amazon_data):
    """
    Calculate a weighted average price from multiple sources.
    eBay typically has more used listings, so we weight it differently.
    """
    # If any source has no data, use the other one
    if ebay_data["avg_price"] == 0:
        return amazon_data["avg_price"]
    if amazon_data["avg_price"] == 0:
        return ebay_data["avg_price"]
    
    # Weight Amazon a bit higher for new devices (60/40 split)
    weighted_avg = (ebay_data["avg_price"] * 0.4) + (amazon_data["avg_price"] * 0.6)
    return round(weighted_avg, 2)

def get_website_text_content(url):
    """
    Get the text content of a website using trafilatura.
    """
    try:
        downloaded = trafilatura.fetch_url(url)
        text = trafilatura.extract(downloaded)
        return text
    except Exception as e:
        logging.error(f"Error fetching website content: {str(e)}")
        return None
