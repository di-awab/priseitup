document.addEventListener('DOMContentLoaded', function() {
    // Device type selection changes available fields
    const deviceTypeSelect = document.getElementById('device-type');
    if (deviceTypeSelect) {
        deviceTypeSelect.addEventListener('change', updateFormFields);
    }
    
    // Initialize form fields based on initial device type
    if (deviceTypeSelect) {
        updateFormFields();
    }
    
    // File upload preview
    const photoInput = document.getElementById('photos');
    const previewContainer = document.getElementById('preview-container');
    if (photoInput && previewContainer) {
        photoInput.addEventListener('change', updatePhotoPreview);
    }
    
    // Form validation
    const estimateForm = document.getElementById('estimate-form');
    if (estimateForm) {
        estimateForm.addEventListener('submit', validateForm);
    }
});

function updateFormFields() {
    const deviceType = document.getElementById('device-type').value;
    const specsField = document.getElementById('specs');
    const specsLabel = document.querySelector('label[for="specs"]');
    const brandSelect = document.getElementById('brand');
    
    // Clear brands dropdown and add relevant options based on device type
    if (brandSelect) {
        const defaultOption = brandSelect.options[0];
        brandSelect.innerHTML = '';
        brandSelect.appendChild(defaultOption);
        
        const brands = getRelevantBrands(deviceType);
        brands.forEach(brand => {
            const option = document.createElement('option');
            option.value = brand;
            option.textContent = brand;
            brandSelect.appendChild(option);
        });
    }
    
    // Update specs placeholder based on device type
    if (specsField && specsLabel) {
        switch(deviceType) {
            case 'smartphone':
                specsLabel.textContent = 'Specifications:';
                specsField.placeholder = 'E.g., 128GB storage, 8GB RAM, Snapdragon 8 Gen 1, etc.';
                break;
            case 'laptop':
                specsLabel.textContent = 'Specifications:';
                specsField.placeholder = 'E.g., i7 processor, 16GB RAM, 512GB SSD, 15" display, etc.';
                break;
            case 'tablet':
                specsLabel.textContent = 'Specifications:';
                specsField.placeholder = 'E.g., 10" display, 64GB storage, WiFi only, etc.';
                break;
            case 'desktop':
                specsLabel.textContent = 'Specifications:';
                specsField.placeholder = 'E.g., Ryzen 7, 32GB RAM, 1TB SSD, RTX 3080, etc.';
                break;
            case 'monitor':
                specsLabel.textContent = 'Specifications:';
                specsField.placeholder = 'E.g., 27" 4K, 144Hz refresh rate, IPS panel, etc.';
                break;
            case 'tv':
                specsLabel.textContent = 'Specifications:';
                specsField.placeholder = 'E.g., 55" 4K OLED, HDR, Smart TV features, etc.';
                break;
            default:
                specsLabel.textContent = 'Specifications:';
                specsField.placeholder = 'Enter device specifications';
        }
    }
}

function getRelevantBrands(deviceType) {
    // Return relevant brands based on device type
    const brandsByType = {
        'smartphone': ['Apple', 'Samsung', 'Google', 'Xiaomi', 'Huawei', 'OnePlus', 'Motorola', 'Sony', 'LG', 'Nokia'],
        'laptop': ['Apple', 'Dell', 'HP', 'Lenovo', 'Asus', 'Acer', 'Microsoft', 'MSI', 'Samsung', 'LG'],
        'tablet': ['Apple', 'Samsung', 'Microsoft', 'Lenovo', 'Amazon', 'Huawei', 'Asus'],
        'desktop': ['Dell', 'HP', 'Lenovo', 'Apple', 'Asus', 'Acer', 'Alienware', 'Custom Build'],
        'monitor': ['Samsung', 'LG', 'Dell', 'Asus', 'Acer', 'BenQ', 'ViewSonic', 'AOC', 'HP'],
        'tv': ['Samsung', 'LG', 'Sony', 'TCL', 'Hisense', 'Vizio', 'Philips', 'Panasonic', 'Sharp'],
        'camera': ['Canon', 'Nikon', 'Sony', 'Fujifilm', 'Panasonic', 'Olympus', 'Leica'],
        'headphones': ['Sony', 'Bose', 'Apple', 'Sennheiser', 'JBL', 'Beats', 'Audio-Technica', 'Jabra'],
        'smartwatch': ['Apple', 'Samsung', 'Garmin', 'Fitbit', 'Fossil', 'Huawei', 'Amazfit'],
        'speaker': ['Sonos', 'Bose', 'JBL', 'Sony', 'Ultimate Ears', 'Harman Kardon', 'Anker']
    };
    
    return brandsByType[deviceType] || ['Other'];
}

function updatePhotoPreview() {
    const photoInput = document.getElementById('photos');
    const previewContainer = document.getElementById('preview-container');
    
    if (!photoInput || !previewContainer) return;
    
    // Clear previous previews
    previewContainer.innerHTML = '';
    
    // Check if any files were selected
    if (photoInput.files.length === 0) {
        previewContainer.style.display = 'none';
        return;
    }
    
    // Show preview container
    previewContainer.style.display = 'block';
    
    // Create and display preview for each selected file
    for (let i = 0; i < photoInput.files.length; i++) {
        if (i >= 4) break; // Limit previews to 4 images
        
        const file = photoInput.files[i];
        
        // Only process image files
        if (!file.type.match('image.*')) continue;
        
        const previewDiv = document.createElement('div');
        previewDiv.className = 'preview-item';
        
        const img = document.createElement('img');
        img.className = 'img-thumbnail';
        img.file = file;
        
        previewDiv.appendChild(img);
        previewContainer.appendChild(previewDiv);
        
        const reader = new FileReader();
        reader.onload = (function(aImg) { 
            return function(e) { 
                aImg.src = e.target.result; 
            }; 
        })(img);
        
        reader.readAsDataURL(file);
    }
    
    // Add info about additional images if more than 4 were selected
    if (photoInput.files.length > 4) {
        const moreInfo = document.createElement('div');
        moreInfo.className = 'more-images-info';
        moreInfo.textContent = `+${photoInput.files.length - 4} more images`;
        previewContainer.appendChild(moreInfo);
    }
}

function validateForm(event) {
    let isValid = true;
    const deviceType = document.getElementById('device-type');
    const brand = document.getElementById('brand');
    const model = document.getElementById('model');
    
    // Reset previous error messages
    document.querySelectorAll('.error-message').forEach(el => el.remove());
    
    // Check required fields
    if (deviceType.value === '') {
        showError(deviceType, 'Please select a device type');
        isValid = false;
    }
    
    if (brand.value === '') {
        showError(brand, 'Please select a brand');
        isValid = false;
    }
    
    if (model.value.trim() === '') {
        showError(model, 'Please enter a model');
        isValid = false;
    }
    
    if (!isValid) {
        event.preventDefault();
    }
}

function showError(element, message) {
    const errorDiv = document.createElement('div');
    errorDiv.className = 'error-message text-danger mt-1';
    errorDiv.textContent = message;
    element.parentNode.appendChild(errorDiv);
    element.classList.add('is-invalid');
}
