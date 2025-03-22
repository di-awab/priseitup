import logging
import re
import os
import random
import requests
from urllib.parse import quote_plus

logger = logging.getLogger(__name__)

# Define Amazon Associate tag for affiliate links
AMAZON_ASSOCIATE_TAG = os.environ.get("AMAZON_ASSOCIATE_TAG", "yourtaghere-20")

def generate_sample_price(base_price, variation=0.2):
    """Generate a price around a base value with some variation"""
    variation_amount = base_price * variation
    return round(base_price + random.uniform(-variation_amount, variation_amount), 2)

def get_price_range(device_details):
    """
    Estimate price ranges based on device details
    
    Args:
        device_details (dict): Dictionary of device details
        
    Returns:
        dict: Base price and condition multiplier
    """
    # Default base price
    base_price = 100.0
    condition_multiplier = 1.0
    
    # Adjust for brand
    brand_prices = {
        'apple': 500.0,
        'samsung': 400.0,
        'google': 350.0,
        'sony': 300.0,
        'lg': 250.0,
        'microsoft': 400.0,
        'dell': 300.0,
        'hp': 250.0,
        'lenovo': 280.0,
        'asus': 270.0,
        'acer': 230.0,
        'huawei': 220.0,
        'oneplus': 300.0,
        'motorola': 180.0,
        'nokia': 150.0,
    }
    
    # Try to get brand-specific base price
    brand = device_details.get('brand', '').lower()
    if brand and brand in brand_prices:
        base_price = brand_prices[brand]
    
    # Adjust for iPhone models
    model = device_details.get('model', '').lower()
    
    if 'iphone' in model:
        if 'iphone 14' in model or 'iphone14' in model:
            base_price = 800.0
        elif 'iphone 13' in model or 'iphone13' in model:
            base_price = 700.0
        elif 'iphone 12' in model or 'iphone12' in model:
            base_price = 600.0
        elif 'iphone 11' in model or 'iphone11' in model:
            base_price = 500.0
        elif 'iphone x' in model or 'iphonex' in model:
            base_price = 400.0
        
        # Adjust for Pro/Max/Mini variants
        if 'pro max' in model:
            base_price *= 1.4
        elif 'pro' in model:
            base_price *= 1.25
        elif 'max' in model:
            base_price *= 1.2
        elif 'plus' in model:
            base_price *= 1.15
        elif 'mini' in model:
            base_price *= 0.8
    
    # Adjust for Samsung Galaxy models
    elif 'galaxy' in model and 'samsung' in brand:
        if 's21' in model:
            base_price = 650.0
        elif 's20' in model:
            base_price = 550.0
        elif 's10' in model:
            base_price = 400.0
        elif 'note 20' in model:
            base_price = 700.0
        elif 'note 10' in model:
            base_price = 550.0
        
    # Adjust for storage capacity
    specs = device_details.get('specs', '').lower()
    if specs:
        if '1tb' in specs:
            base_price *= 1.5
        elif '512gb' in specs:
            base_price *= 1.3
        elif '256gb' in specs:
            base_price *= 1.15
        elif '128gb' in specs:
            base_price *= 1.0
        elif '64gb' in specs:
            base_price *= 0.85
        elif '32gb' in specs:
            base_price *= 0.7
        
    # Adjust for condition
    condition = device_details.get('condition', '').lower()
    condition_factors = {
        'new': 1.0,
        'like new': 0.9,
        'excellent': 0.8,
        'good': 0.7,
        'fair': 0.5,
        'poor': 0.3
    }
    
    if condition in condition_factors:
        condition_multiplier = condition_factors[condition]
    
    # Calculate final price
    final_price = base_price * condition_multiplier
    
    return final_price

def generate_sample_products(device_details, base_price):
    """Generate sample product suggestions based on device details"""
    products = []
    
    brand = device_details.get('brand', '')
    model = device_details.get('model', '')
    specs = device_details.get('specs', '')
    
    # Create search query
    query = f"{brand} {model} {specs}".strip()
    
    # Sample product templates
    templates = [
        {
            "title": f"{brand} {model} {specs} (New)",
            "price": str(generate_sample_price(base_price * 1.2)),
            "link": f"https://www.amazon.com/s?k={quote_plus(query)}",
            "image_url": "https://via.placeholder.com/300x300?text=Product+Image"
        },
        {
            "title": f"{brand} {model} Premium Case",
            "price": str(generate_sample_price(base_price * 0.1)),
            "link": f"https://www.amazon.com/s?k={quote_plus(f'{brand} {model} case')}",
            "image_url": "https://via.placeholder.com/300x300?text=Case+Image"
        },
        {
            "title": f"Screen Protector Compatible with {brand} {model}",
            "price": str(generate_sample_price(base_price * 0.05)),
            "link": f"https://www.amazon.com/s?k={quote_plus(f'{brand} {model} screen protector')}",
            "image_url": "https://via.placeholder.com/300x300?text=Screen+Protector"
        },
        {
            "title": f"Fast Charger for {brand} {model}",
            "price": str(generate_sample_price(base_price * 0.15)),
            "link": f"https://www.amazon.com/s?k={quote_plus(f'{brand} {model} charger')}",
            "image_url": "https://via.placeholder.com/300x300?text=Charger+Image"
        },
        {
            "title": f"Wireless Earbuds Compatible with {brand} Devices",
            "price": str(generate_sample_price(base_price * 0.3)),
            "link": f"https://www.amazon.com/s?k={quote_plus('wireless earbuds')}",
            "image_url": "https://via.placeholder.com/300x300?text=Earbuds+Image"
        }
    ]
    
    return templates

def scrape_prices(device_details):
    """
    Generate price estimations based on device details
    
    Args:
        device_details (dict): Dictionary containing device details
        
    Returns:
        dict: Dictionary containing prices, sources, and suggested products
    """
    # Log what we're analyzing
    logger.info(f"Analyzing device details: {device_details}")
    
    # Construct search query from device details
    query_parts = []
    
    if device_details.get('brand'):
        query_parts.append(device_details['brand'])
    
    if device_details.get('model'):
        query_parts.append(device_details['model'])
    
    if device_details.get('specs'):
        query_parts.append(device_details['specs'])
    
    if device_details.get('condition'):
        query_parts.append(device_details['condition'])
    
    query = " ".join(query_parts)
    logger.info(f"Generated search query: {query}")
    
    # Calculate base price from device details
    base_price = get_price_range(device_details)
    logger.info(f"Estimated base price: ${base_price}")
    
    # Generate multiple price points with some variation
    num_prices = 5
    prices = [generate_sample_price(base_price) for _ in range(num_prices)]
    
    # Define sources
    sources = ["Amazon", "eBay", "BestBuy", "Swappa", "OfferUp"][:num_prices]
    
    # Generate product suggestions
    suggested_products = generate_sample_products(device_details, base_price)
    
    logger.info(f"Generated prices: {prices}")
    logger.info(f"Sources: {sources}")
    
    return {
        'prices': prices,
        'sources': sources,
        'suggested_products': suggested_products
    }
