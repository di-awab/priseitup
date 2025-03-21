import os
import logging
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from werkzeug.utils import secure_filename
import json
from datetime import datetime
from utils.scraper import scrape_product_data
from utils.price_estimator import estimate_price, get_recommendations

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Setup database
class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

# Create Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key")

# Configure database
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///electronics.db")
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}

# Configure file uploads
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max upload

# Initialize the app with the extension
db.init_app(app)

# Import models after db initialization to avoid circular imports
with app.app_context():
    import models
    db.create_all()

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/estimate', methods=['POST'])
def estimate():
    try:
        # Get form data
        device_type = request.form.get('device_type')
        brand = request.form.get('brand')
        model = request.form.get('model')
        specs = request.form.get('specs')
        condition = request.form.get('condition')
        region = request.form.get('region', 'US')
        
        # Handle file upload
        photo_paths = []
        if 'photos' in request.files:
            photos = request.files.getlist('photos')
            for photo in photos:
                if photo and allowed_file(photo.filename):
                    filename = secure_filename(photo.filename)
                    # Add timestamp to prevent filename collisions
                    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
                    new_filename = f"{timestamp}_{filename}"
                    filepath = os.path.join(app.config['UPLOAD_FOLDER'], new_filename)
                    photo.save(filepath)
                    photo_paths.append(filepath.replace('static/', ''))
        
        # Get price estimate
        scraped_data = scrape_product_data(device_type, brand, model)
        estimated_price = estimate_price(device_type, brand, model, specs, condition, region, scraped_data)
        
        # Get product recommendations
        recommendations = get_recommendations(device_type, brand, model, price=estimated_price)
        
        # Save to database
        with app.app_context():
            new_estimate = models.PriceEstimate(
                device_type=device_type,
                brand=brand,
                model=model,
                specs=specs,
                condition=condition,
                region=region,
                estimated_price=estimated_price,
                photo_paths=json.dumps(photo_paths)
            )
            db.session.add(new_estimate)
            db.session.commit()
        
        return render_template('result.html', 
                              device_type=device_type,
                              brand=brand, 
                              model=model, 
                              specs=specs,
                              condition=condition,
                              region=region,
                              estimated_price=estimated_price,
                              recommendations=recommendations,
                              photo_paths=photo_paths)
    
    except Exception as e:
        logging.error(f"Error during price estimation: {str(e)}")
        flash(f"An error occurred: {str(e)}", "danger")
        return redirect(url_for('index'))

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(e):
    logging.error(f"Server error: {str(e)}")
    return render_template('500.html'), 500
