from app import db
from datetime import datetime

class PriceEstimate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    device_type = db.Column(db.String(64), nullable=False)
    brand = db.Column(db.String(64), nullable=False)
    model = db.Column(db.String(128), nullable=False)
    specs = db.Column(db.Text)
    condition = db.Column(db.String(64))
    region = db.Column(db.String(64), default='US')
    estimated_price = db.Column(db.Float)
    photo_paths = db.Column(db.Text)  # JSON string of photo paths
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<PriceEstimate {self.brand} {self.model}>'

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    device_type = db.Column(db.String(64), nullable=False)
    brand = db.Column(db.String(64), nullable=False)
    model = db.Column(db.String(128), nullable=False)
    specs = db.Column(db.Text)
    current_price = db.Column(db.Float)
    affiliate_link = db.Column(db.String(512))
    image_url = db.Column(db.String(512))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<Product {self.brand} {self.model}>'

class ScrapedPrice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    device_type = db.Column(db.String(64), nullable=False)
    brand = db.Column(db.String(64), nullable=False)
    model = db.Column(db.String(128), nullable=False)
    specs = db.Column(db.Text)
    condition = db.Column(db.String(64))
    source = db.Column(db.String(64))  # e.g., 'ebay', 'amazon'
    price = db.Column(db.Float)
    scrape_date = db.Column(db.DateTime, default=datetime.utcnow)
    region = db.Column(db.String(64), default='US')

    def __repr__(self):
        return f'<ScrapedPrice {self.source} {self.brand} {self.model}>'
