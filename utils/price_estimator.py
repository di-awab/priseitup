import logging
import random
import numpy as np
from sklearn.linear_model import LinearRegression

def estimate_price(device_type, brand, model, specs, condition, region, scraped_data):
    """
    Estimate the price of a device based on its specifications and condition.
    
    Args:
        device_type (str): Type of device (smartphone, laptop, etc.)
        brand (str): Brand name
        model (str): Model name
        specs (str): Device specifications
        condition (str): Device condition (New, Like New, Good, Fair, Poor)
        region (str): User's region/country
        scraped_data (dict): Data scraped from various sources
        
    Returns:
        float: Estimated price
    """
    logging.info(f"Estimating price for {brand} {model}")
    
    try:
        # Start with the average price from scraped data
        base_price = scraped_data.get("average_price", 0)
        
        # If no scraped data, use a fallback method
        if base_price == 0:
            base_price = get_fallback_price(device_type, brand, model)
        
        # Apply condition adjustment
        condition_multiplier = get_condition_multiplier(condition)
        
        # Apply regional price adjustment
        region_multiplier = get_region_multiplier(region)
        
        # Apply specs adjustment (extract key features from specs text)
        specs_multiplier = analyze_specs(device_type, specs)
        
        # Calculate final price
        estimated_price = base_price * condition_multiplier * region_multiplier * specs_multiplier
        
        # Round to nearest dollar amount
        estimated_price = round(estimated_price, 0)
        
        logging.info(f"Estimated price: ${estimated_price}")
        return estimated_price
        
    except Exception as e:
        logging.error(f"Error in price estimation: {str(e)}")
        # Fallback to basic estimate
        return get_fallback_price(device_type, brand, model)

def get_fallback_price(device_type, brand, model):
    """
    Get a fallback price when scraped data is unavailable.
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
    
    # Add some randomness for the model
    model_variation = 0.9 + (random.random() * 0.2)  # Between 0.9 and 1.1
    
    return base * multiplier * model_variation

def get_condition_multiplier(condition):
    """
    Get a price multiplier based on the device condition.
    """
    condition_multipliers = {
        "new": 1.0,
        "like new": 0.9,
        "good": 0.75,
        "fair": 0.6,
        "poor": 0.4
    }
    
    return condition_multipliers.get(condition.lower(), 0.7)  # Default to "good" if not specified

def get_region_multiplier(region):
    """
    Get a price multiplier based on the user's region.
    Different regions have different market values for electronics.
    """
    region_multipliers = {
        "us": 1.0,
        "ca": 1.05,  # Canada
        "uk": 1.1,
        "eu": 1.1,
        "au": 1.15,  # Australia
        "jp": 1.0,   # Japan
        "kr": 0.9,   # South Korea
        "cn": 0.85,  # China
        "in": 0.8,   # India
        "br": 1.2,   # Brazil
    }
    
    return region_multipliers.get(region.lower(), 1.0)  # Default to US pricing

def analyze_specs(device_type, specs):
    """
    Analyze device specifications to adjust the price.
    Higher specs generally mean higher price.
    
    This is a simplified implementation. In a real application, you would:
    1. Use NLP to extract key specs (storage, RAM, processor, etc.)
    2. Train a model on historical data to weigh each spec appropriately
    """
    if not specs:
        return 1.0  # No adjustment if no specs provided
    
    specs_lower = specs.lower()
    multiplier = 1.0
    
    # Check for high-end indicators in specs
    high_end_keywords = ["premium", "pro", "flagship", "high-end", "gaming"]
    if any(keyword in specs_lower for keyword in high_end_keywords):
        multiplier *= 1.15
    
    # Check for storage capacity
    if "tb" in specs_lower:  # Terabyte storage
        multiplier *= 1.2
    elif "512gb" in specs_lower or "500gb" in specs_lower:
        multiplier *= 1.1
    elif "256gb" in specs_lower or "250gb" in specs_lower:
        multiplier *= 1.05
    
    # Check for RAM
    if "32gb ram" in specs_lower or "32 gb ram" in specs_lower:
        multiplier *= 1.2
    elif "16gb ram" in specs_lower or "16 gb ram" in specs_lower:
        multiplier *= 1.1
    elif "8gb ram" in specs_lower or "8 gb ram" in specs_lower:
        multiplier *= 1.05
    
    # Check for processor (simplified)
    if "i9" in specs_lower or "ryzen 9" in specs_lower:
        multiplier *= 1.2
    elif "i7" in specs_lower or "ryzen 7" in specs_lower:
        multiplier *= 1.1
    elif "i5" in specs_lower or "ryzen 5" in specs_lower:
        multiplier *= 1.05
    
    # Check for age indicators
    old_keywords = ["old", "outdated", "2015", "2016", "2017"]
    if any(keyword in specs_lower for keyword in old_keywords):
        multiplier *= 0.8
    
    return multiplier

def train_price_model(historical_data):
    """
    Train a machine learning model to predict device prices.
    In a real application, this would use actual historical data.
    
    Args:
        historical_data: List of dictionaries with device features and prices
        
    Returns:
        model: Trained regression model
    """
    # This is a placeholder implementation
    # In a real app, you'd extract features from the historical data
    X = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])  # Example features
    y = np.array([100, 200, 300])  # Example prices
    
    model = LinearRegression()
    model.fit(X, y)
    
    return model

def get_recommendations(device_type, brand, model, price=None):
    """
    Get product recommendations based on the device.
    These would typically be similar or upgraded products.
    
    Args:
        device_type (str): Type of device
        brand (str): Brand name
        model (str): Model name
        price (float): Estimated price of current device
        
    Returns:
        list: List of recommended products
    """
    # In a real application, you would:
    # 1. Query a product database for similar/upgraded items
    # 2. Sort by relevance
    # 3. Add affiliate links
    
    # For this demo, we'll generate some sample recommendations
    recommendations = []
    
    # Sample product data (in real app, this would come from a database)
    if device_type.lower() == 'smartphone':
        recommendations = [
            {
                'name': f'{brand} {get_upgraded_model(model)}',
                'description': f'Upgraded version with better camera and faster processor',
                'price': price * 1.3 if price else 499.99,
                'image': 'https://cdn.shopify.com/s/files/1/0024/9803/5810/products/572541-Product-0-I-637726304838261215_800x800.jpg',
                'affiliate_link': 'https://www.amazon.com/s?k=smartphone'
            },
            {
                'name': f'{get_alternative_brand(brand)} {get_similar_model(model)}',
                'description': 'Similar specifications with different brand experience',
                'price': price * 1.1 if price else 449.99,
                'image': 'https://images.samsung.com/is/image/samsung/p6pim/uk/2307/gallery/uk-galaxy-z-fold5-f946-sm-f946bzbaeu3-thumb-534863401',
                'affiliate_link': 'https://www.amazon.com/s?k=smartphone'
            },
            {
                'name': f'{brand} {get_accessory(device_type)}',
                'description': 'Perfect accessory for your device',
                'price': price * 0.2 if price else 49.99,
                'image': 'https://img.favpng.com/25/22/1/battery-charger-smartphone-feature-phone-mobile-phone-accessories-png-favpng-7Z1wpb3PJ9HaM7E88XtxY2b4v.jpg',
                'affiliate_link': 'https://www.amazon.com/s?k=phone+accessories'
            }
        ]
    elif device_type.lower() == 'laptop':
        recommendations = [
            {
                'name': f'{brand} {get_upgraded_model(model)}',
                'description': 'Upgraded model with faster processor and more RAM',
                'price': price * 1.4 if price else 1299.99,
                'image': 'https://images.unsplash.com/photo-1541807084-5c52b6b3adef?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8bGFwdG9wfGVufDB8fDB8fHww&w=1000&q=80',
                'affiliate_link': 'https://www.amazon.com/s?k=laptop'
            },
            {
                'name': f'{get_alternative_brand(brand)} {get_similar_model(model)}',
                'description': 'Similar performance with different design philosophy',
                'price': price * 1.1 if price else 1099.99,
                'image': 'https://www.notebookcheck.net/uploads/tx_nbc2/Dell_XPS_15_9500_non-touch_FHD__15.jpg',
                'affiliate_link': 'https://www.amazon.com/s?k=laptop'
            },
            {
                'name': f'{brand} {get_accessory(device_type)}',
                'description': 'Essential accessory for your device',
                'price': price * 0.15 if price else 79.99,
                'image': 'https://cdn.shopify.com/s/files/1/0870/4886/products/Laptop-Case-Black-FW20.jpg',
                'affiliate_link': 'https://www.amazon.com/s?k=laptop+accessories'
            }
        ]
    else:
        # Generic recommendations for other device types
        recommendations = [
            {
                'name': f'Premium {device_type.title()}',
                'description': 'High-end model with excellent performance',
                'price': price * 1.5 if price else 499.99,
                'image': 'https://images.pexels.com/photos/1029757/pexels-photo-1029757.jpeg',
                'affiliate_link': f'https://www.amazon.com/s?k={device_type}'
            },
            {
                'name': f'Budget-friendly {device_type.title()}',
                'description': 'Great value for money with essential features',
                'price': price * 0.7 if price else 299.99,
                'image': 'https://images.pexels.com/photos/1029757/pexels-photo-1029757.jpeg',
                'affiliate_link': f'https://www.amazon.com/s?k=budget+{device_type}'
            },
            {
                'name': f'{device_type.title()} Accessory Kit',
                'description': 'Complete set of accessories for your device',
                'price': price * 0.2 if price else 59.99,
                'image': 'https://images.pexels.com/photos/1029757/pexels-photo-1029757.jpeg',
                'affiliate_link': f'https://www.amazon.com/s?k={device_type}+accessories'
            }
        ]
    
    return recommendations

def get_upgraded_model(model):
    """Get an upgraded version of the model name"""
    suffixes = ["Pro", "Plus", "Premium", "Ultra", "Max", "Next Gen"]
    if any(suffix in model for suffix in suffixes):
        return f"{model} 2"
    return f"{model} {random.choice(suffixes)}"

def get_similar_model(model):
    """Get a similar model name"""
    prefixes = ["A", "X", "Z", "Pro", "Elite", "Prime"]
    numbers = ["5", "7", "9", "10", "20", "500", "900"]
    return f"{random.choice(prefixes)}{random.choice(numbers)}"

def get_alternative_brand(brand):
    """Get a different brand in the same market segment"""
    premium_brands = ["Apple", "Samsung", "Sony", "Google", "Microsoft"]
    mid_tier_brands = ["Dell", "HP", "Lenovo", "Asus", "Acer", "LG"]
    budget_brands = ["Xiaomi", "Realme", "TCL", "Huawei"]
    
    if brand in premium_brands:
        alternatives = [b for b in premium_brands if b != brand]
    elif brand in mid_tier_brands:
        alternatives = [b for b in mid_tier_brands if b != brand]
    else:
        alternatives = [b for b in budget_brands if b != brand]
        
    if not alternatives:
        alternatives = mid_tier_brands
        
    return random.choice(alternatives)

def get_accessory(device_type):
    """Get a relevant accessory for the device type"""
    accessories = {
        "smartphone": ["Fast Charger", "Premium Case", "Screen Protector", "Power Bank", "Wireless Earbuds"],
        "laptop": ["Cooling Pad", "Carrying Case", "Wireless Mouse", "USB-C Hub", "External SSD"],
        "tablet": ["Smart Cover", "Stylus Pen", "Screen Protector", "Keyboard Case", "Stand"],
        "desktop": ["Mechanical Keyboard", "Gaming Mouse", "Large Monitor", "External SSD", "Webcam"],
        "camera": ["Extra Battery", "Memory Card", "Camera Bag", "Tripod", "Lens Cleaning Kit"],
        "headphones": ["Carry Case", "Replacement Ear Pads", "Headphone Stand", "Audio Cable", "Battery Pack"],
        "smartwatch": ["Extra Band", "Charging Dock", "Screen Protector", "Wireless Earbuds", "Band Adapter"],
    }
    
    device_accessories = accessories.get(device_type.lower(), ["Premium Accessory", "Protective Case", "Cleaning Kit"])
    return random.choice(device_accessories)
