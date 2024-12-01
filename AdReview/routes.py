from flask import Blueprint, render_template, request
from app.services.rekognition_service import extract_text_from_image, extract_labels_from_image
from app.services.bedrock_services import generate_ad_content, generate_ad_review

# Initialize the Blueprint object
main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template('index.html')

@main_bp.route('/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return "No file part", 400
    
    file = request.files['image']
    if file.filename == '':
        return "No selected file", 400
    
    image_bytes = file.read()

    # Extract text and labels from the uploaded image using Rekognition
    extracted_text = extract_text_from_image(image_bytes)
    extracted_labels = extract_labels_from_image(image_bytes)

    # Generate ad content using Bedrock based on the extracted text and labels
    prompt_message = f"Create an ad based on the following text and labels: {extracted_text} {extracted_labels}"
    ad_content = generate_ad_content(prompt_message)

    # Review the generated ad content with given requirements
    generated_requirements = "Ensure the ad adheres to guidelines and looks professional."
    ad_review = generate_ad_review(ad_content, generated_requirements)

    # Return the results to the template
    return render_template('result.html', 
                           extracted_text=extracted_text, 
                           extracted_labels=extracted_labels, 
                           ad_content=ad_content, 
                           ad_review=ad_review)

@main_bp.route('/generate_review', methods=['POST'])
def generate_review_req():
    ad_content = request.form['ad_content']
    generated_requirements = request.form['generated_requirements']

    review_content = generate_ad_review(ad_content, generated_requirements)

    return render_template('review.html', review_content=review_content)
