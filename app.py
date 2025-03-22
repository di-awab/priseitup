import os
import logging
import uuid
from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
import tempfile
from utils.analysis import analyze_device_description
from scrapers.price_scraper import scrape_prices

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Create Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "default-secret-key")

# Configure upload settings
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
TEMP_UPLOAD_FOLDER = tempfile.gettempdir()

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    """Render the main page"""
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    """Analyze device description and images to estimate price"""
    try:
        description = request.form.get('description', '')
        
        if not description:
            return jsonify({'error': 'Please provide a device description'}), 400
        
        # Handle file uploads
        image_paths = []
        if 'images' in request.files:
            images = request.files.getlist('images')
            for image in images:
                if image and allowed_file(image.filename):
                    filename = secure_filename(image.filename)
                    # Add unique identifier to avoid filename collisions
                    unique_filename = f"{uuid.uuid4()}_{filename}"
                    file_path = os.path.join(TEMP_UPLOAD_FOLDER, unique_filename)
                    image.save(file_path)
                    image_paths.append(file_path)
        
        # Analyze device description to extract key details
        logger.debug(f"Analyzing description: {description}")
        device_details = analyze_device_description(description)
        
        if not device_details:
            return jsonify({'error': 'Could not analyze the device description. Please be more specific.'}), 400
        
        # Scrape prices based on extracted details
        logger.debug(f"Scraping prices for: {device_details}")
        price_data = scrape_prices(device_details)
        
        # Calculate estimated price
        if price_data['prices']:
            estimated_price = sum(price_data['prices']) / len(price_data['prices'])
        else:
            estimated_price = 0
        
        # Get suggested products for affiliate marketing
        suggested_products = price_data.get('suggested_products', [])
        
        # Clean up temporary image files
        for image_path in image_paths:
            try:
                os.remove(image_path)
            except Exception as e:
                logger.error(f"Error removing temporary file {image_path}: {e}")
        
        return jsonify({
            'success': True,
            'device_details': device_details,
            'estimated_price': round(estimated_price, 2),
            'price_range': {
                'min': min(price_data['prices']) if price_data['prices'] else 0,
                'max': max(price_data['prices']) if price_data['prices'] else 0
            },
            'sources': price_data['sources'],
            'suggested_products': suggested_products
        })
    
    except Exception as e:
        logger.exception("Error in analyze endpoint")
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
