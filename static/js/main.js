document.addEventListener('DOMContentLoaded', function() {
    // Form elements
    const priceForm = document.getElementById('priceForm');
    const descriptionInput = document.getElementById('deviceDescription');
    const imageUpload = document.getElementById('deviceImages');
    const previewContainer = document.getElementById('imagePreviewContainer');
    
    // Results elements
    const loadingIndicator = document.getElementById('loadingIndicator');
    const resultsContainer = document.getElementById('resultsContainer');
    const suggestionsContainer = document.getElementById('suggestionsContainer');
    const estimatedPrice = document.getElementById('estimatedPrice');
    const priceRange = document.getElementById('priceRange');
    const detailsList = document.getElementById('detailsList');
    const sourcesList = document.getElementById('sourcesList');
    const errorMessage = document.getElementById('errorMessage');
    const productGrid = document.getElementById('productGrid');
    
    // Image preview functionality
    imageUpload.addEventListener('change', function(event) {
        previewContainer.innerHTML = '';
        
        const files = event.target.files;
        if (files.length > 0) {
            for (let i = 0; i < files.length; i++) {
                const file = files[i];
                
                // Only process image files
                if (!file.type.match('image.*')) {
                    continue;
                }
                
                const reader = new FileReader();
                
                reader.onload = function(e) {
                    const img = document.createElement('img');
                    img.src = e.target.result;
                    img.className = 'image-preview';
                    previewContainer.appendChild(img);
                };
                
                reader.readAsDataURL(file);
            }
        }
    });
    
    // Form submission handler
    priceForm.addEventListener('submit', function(event) {
        event.preventDefault();
        
        // Basic validation
        if (!descriptionInput.value.trim()) {
            showError('Please enter a device description');
            return;
        }
        
        // Hide any previous error messages
        hideError();
        
        // Show loading indicator
        loadingIndicator.style.display = 'block';
        
        // Hide previous results
        resultsContainer.style.display = 'none';
        suggestionsContainer.style.display = 'none';
        
        // Create form data
        const formData = new FormData(priceForm);
        
        // Send request to server
        fetch('/analyze', {
            method: 'POST',
            body: formData
        })
        .then(response => {
            if (!response.ok) {
                return response.json().then(data => {
                    throw new Error(data.error || 'An error occurred');
                });
            }
            return response.json();
        })
        .then(data => {
            // Hide loading indicator
            loadingIndicator.style.display = 'none';
            
            // Display results
            displayResults(data);
        })
        .catch(error => {
            // Hide loading indicator
            loadingIndicator.style.display = 'none';
            
            // Show error message
            showError(error.message);
        });
    });
    
    // Function to display results
    function displayResults(data) {
        // Update estimated price
        estimatedPrice.textContent = `$${data.estimated_price}`;
        
        // Update price range
        if (data.price_range && data.price_range.min !== data.price_range.max) {
            priceRange.textContent = `Price range: $${data.price_range.min} - $${data.price_range.max}`;
        } else {
            priceRange.textContent = '';
        }
        
        // Update device details
        detailsList.innerHTML = '';
        if (data.device_details) {
            const details = data.device_details;
            
            if (details.brand) {
                addDetailItem('Brand', details.brand);
            }
            
            if (details.model) {
                addDetailItem('Model', details.model);
            }
            
            if (details.specs) {
                addDetailItem('Specifications', details.specs);
            }
            
            if (details.condition) {
                addDetailItem('Condition', details.condition);
            }
        }
        
        // Update sources
        sourcesList.innerHTML = '';
        if (data.sources && data.sources.length > 0) {
            const uniqueSources = [...new Set(data.sources)];
            uniqueSources.forEach(source => {
                const li = document.createElement('li');
                li.textContent = source;
                sourcesList.appendChild(li);
            });
        } else {
            const li = document.createElement('li');
            li.textContent = 'No sources available';
            sourcesList.appendChild(li);
        }
        
        // Show results container
        resultsContainer.style.display = 'block';
        
        // Update product suggestions
        productGrid.innerHTML = '';
        if (data.suggested_products && data.suggested_products.length > 0) {
            data.suggested_products.forEach(product => {
                const productCard = createProductCard(product);
                productGrid.appendChild(productCard);
            });
            
            // Show suggestions container
            suggestionsContainer.style.display = 'block';
        } else {
            suggestionsContainer.style.display = 'none';
        }
        
        // Scroll to results
        resultsContainer.scrollIntoView({ behavior: 'smooth' });
    }
    
    // Function to add a detail item to the details list
    function addDetailItem(label, value) {
        const li = document.createElement('li');
        li.className = 'list-group-item';
        
        const labelSpan = document.createElement('span');
        labelSpan.className = 'detail-label';
        labelSpan.textContent = label + ': ';
        
        const valueSpan = document.createElement('span');
        valueSpan.className = 'detail-value';
        valueSpan.textContent = value;
        
        li.appendChild(labelSpan);
        li.appendChild(valueSpan);
        
        detailsList.appendChild(li);
    }
    
    // Function to create a product card for suggested products
    function createProductCard(product) {
        const col = document.createElement('div');
        col.className = 'col-md-4 col-sm-6 mb-4';
        
        const card = document.createElement('div');
        card.className = 'card product-card h-100';
        
        // Product image
        const img = document.createElement('img');
        img.className = 'card-img-top product-img';
        img.src = product.image_url || 'https://via.placeholder.com/300x300?text=No+Image';
        img.alt = product.title;
        
        // Card body
        const cardBody = document.createElement('div');
        cardBody.className = 'card-body d-flex flex-column';
        
        // Product title
        const title = document.createElement('h5');
        title.className = 'card-title product-title';
        title.textContent = product.title;
        
        // Product price
        const price = document.createElement('p');
        price.className = 'card-text product-price';
        price.textContent = `$${product.price}`;
        
        // Buy button
        const button = document.createElement('a');
        button.className = 'btn btn-primary mt-auto';
        button.href = product.link;
        button.target = '_blank';
        button.textContent = 'Buy on Amazon';
        
        // Append elements
        cardBody.appendChild(title);
        cardBody.appendChild(price);
        cardBody.appendChild(button);
        
        card.appendChild(img);
        card.appendChild(cardBody);
        
        col.appendChild(card);
        
        return col;
    }
    
    // Function to show error message
    function showError(message) {
        errorMessage.textContent = message;
        errorMessage.style.display = 'block';
    }
    
    // Function to hide error message
    function hideError() {
        errorMessage.style.display = 'none';
    }
});
