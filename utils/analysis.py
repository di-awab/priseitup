import logging
import os
import re

logger = logging.getLogger(__name__)

# Use a simpler approach without transformers library
logger.info("Using basic text analysis approach")

# Generic extraction function
def extract_device_info(description):
    """
    Extract device information using generic pattern matching and rules-based approach
    
    Args:
        description (str): Device description text
        
    Returns:
        dict: Extracted device details
    """
    # Lower case for easier matching
    text = description.lower()
    
    # Initialize empty device details
    device_details = {
        'brand': '',
        'model': '',
        'specs': '',
        'condition': ''
    }
    
    # Common electronics brands
    brands = [
        'apple', 'samsung', 'sony', 'lg', 'google', 'huawei', 'xiaomi', 
        'oneplus', 'microsoft', 'nokia', 'motorola', 'asus', 'acer', 
        'dell', 'hp', 'lenovo', 'toshiba', 'msi', 'nintendo', 'xbox',
        'playstation', 'oppo', 'vivo', 'realme', 'honor'
    ]
    
    # Try to extract brand
    for brand in brands:
        if brand in text:
            device_details['brand'] = brand.title()
            break
    
    # Try to extract product lines and models (simplified example)
    if 'iphone' in text:
        device_details['brand'] = 'Apple'
        
        # Try to extract iPhone model
        for i in range(3, 15):  # iPhone 3 to iPhone 14
            if f'iphone {i}' in text or f'iphone{i}' in text:
                device_details['model'] = f'iPhone {i}'
                break
        
        # Check for iPhone models with "Pro", "Max", "Plus", "mini" etc.
        if 'pro max' in text and not device_details.get('model'):
            device_details['model'] = 'iPhone Pro Max'
        elif 'pro' in text and not device_details.get('model'):
            device_details['model'] = 'iPhone Pro'
        elif 'max' in text and not device_details.get('model'):
            device_details['model'] = 'iPhone Max'
        elif 'plus' in text and not device_details.get('model'):
            device_details['model'] = 'iPhone Plus'
        elif 'mini' in text and not device_details.get('model'):
            device_details['model'] = 'iPhone Mini'
        elif not device_details.get('model'):
            device_details['model'] = 'iPhone'
    
    elif 'galaxy' in text and device_details['brand'] == 'Samsung':
        device_details['model'] = 'Galaxy'
        
        # Try to detect Galaxy S series
        if 's21' in text:
            device_details['model'] += ' S21'
        elif 's20' in text:
            device_details['model'] += ' S20'
        elif 's10' in text:
            device_details['model'] += ' S10'
        elif 's9' in text:
            device_details['model'] += ' S9'
        elif 's8' in text:
            device_details['model'] += ' S8'
        
        # Try to detect Galaxy Note series
        elif 'note 20' in text:
            device_details['model'] += ' Note 20'
        elif 'note 10' in text:
            device_details['model'] += ' Note 10'
        elif 'note 9' in text:
            device_details['model'] += ' Note 9'
        
        # Try to detect Galaxy A series
        elif 'a52' in text:
            device_details['model'] += ' A52'
        elif 'a51' in text:
            device_details['model'] += ' A51'
        elif 'a50' in text:
            device_details['model'] += ' A50'
    
    # Extract storage capacity
    storage_patterns = ['gb', 'tb']
    words = text.split()
    for i, word in enumerate(words):
        if any(pattern in word for pattern in storage_patterns) and i > 0:
            try:
                # Check if previous word is a number or contains a number
                prev_word = words[i-1]
                if prev_word.isdigit():
                    device_details['specs'] = f"{prev_word}{word}"
                elif any(c.isdigit() for c in prev_word):
                    # Extract digit part from the word
                    digits = ''.join(c for c in prev_word if c.isdigit())
                    device_details['specs'] = f"{digits}{word}"
            except (IndexError, ValueError):
                pass
    
    # Extract condition
    condition_keywords = {
        'new': ['new', 'brand new', 'sealed', 'unopened'],
        'like new': ['like new', 'mint', 'mint condition', 'perfect condition'],
        'excellent': ['excellent', 'excellent condition', 'barely used'],
        'good': ['good', 'good condition', 'used'],
        'fair': ['fair', 'fair condition', 'worn'],
        'poor': ['poor', 'poor condition', 'damaged', 'broken']
    }
    
    for condition, keywords in condition_keywords.items():
        if any(keyword in text for keyword in keywords):
            device_details['condition'] = condition
            break
    
    # If no condition found, default to "used"
    if not device_details.get('condition'):
        device_details['condition'] = 'used'
    
    return device_details


def analyze_device_description(description):
    """
    Analyze device description to extract key details using pattern matching
    
    Args:
        description (str): Device description text
        
    Returns:
        dict: Extracted device details
    """
    try:
        # Use our generic extraction function
        return extract_device_info(description)
    
    except Exception as e:
        logger.exception(f"Error analyzing device description: {e}")
        # Create basic fallback for extreme cases
        return {
            'brand': '',
            'model': '',
            'specs': '',
            'condition': 'used'
        }
