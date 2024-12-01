'''from flask import Blueprint, render_template, request
from app.services.rekognition_service import extract_text_from_image, extract_labels_from_image
from app.services.bedrock_services import generate, check_for_violations

# Initialize the Blueprint object for the main routes
main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    # Render the landing page (index.html)
    return render_template('index.html')

@main_bp.route('/upload', methods=['POST'])
def upload_image():
    # Check if 'image' exists in the request files
    if 'image' not in request.files:
        return "No file part", 400
    
    file = request.files['image']
    if file.filename == '':
        return "No selected file", 400
    
    # Read the image file bytes
    image_bytes = file.read()

    # Extract text and labels from the uploaded image using Rekognition
    extracted_text = extract_text_from_image(image_bytes)
    extracted_labels = extract_labels_from_image(image_bytes)

    # Generate ad content using Bedrock based on the extracted text and labels
    prompt_message = f"Create an ad based on the following text and labels: {extracted_text} {extracted_labels}"
    ad_content = generate(prompt_message)  # Call the generate function from bedrock_services

    # Check for violations using the generated ad content
    violation_result = check_for_violations(extracted_text, extracted_labels)  # Call the violation check function

    # Return the results to the template (rendering result.html)
    return render_template('result.html', 
                           extracted_text=extracted_text, 
                           extracted_labels=extracted_labels, 
                           ad_content=ad_content, 
                           violation_result=violation_result)

@main_bp.route('/generate_review', methods=['POST'])
def generate_review_req():
    # Get the ad content and generated requirements from the form data
    ad_content = request.form['ad_content']
    generated_requirements = request.form['generated_requirements']

    # Generate the review of the ad content
    review_content = check_for_violations(ad_content, generated_requirements)

    # Return the review content to the review template
    return render_template('review.html', review_content=review_content)
'''
from flask import Blueprint, render_template, request
from app.services.rekognition_service import extract_text_from_image, extract_labels_from_image
from app.services.bedrock_services import generate, check_for_violations

# Initialize the Blueprint object for the main routes
main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    # Render the landing page (index.html)
    return render_template('index.html')

@main_bp.route('/submit_ad', methods=['POST'])
def submit_ad():
    # Extract form data
    project_name = request.form['project_name']
    description = request.form['description']
    ad_for_platform = request.form['ad_for_platform']
    ad_type = request.form['ad_type']

    # Generate ad content based on the user's input
    prompt_message = f"Create an ad based on the following details: Project Name: {project_name}, Description: {description}, Platform: {ad_for_platform}, Ad Type: {ad_type}"
    ad_content = generate(prompt_message)  # Call Bedrock service to generate content

    # Check for violations on the generated ad content
    violation_result = check_for_violations(ad_content)

    # Store the details or send them to the designer (optional)
    # You can implement logic to store data in a database or send it to a designer email here

    # Return the submission confirmation and details to the user
    return render_template('submission_details.html', 
                           project_name=project_name, 
                           description=description, 
                           ad_for_platform=ad_for_platform, 
                           ad_type=ad_type, 
                           ad_content=ad_content,
                           violation_result=violation_result)

@main_bp.route('/upload', methods=['POST'])
def upload_image():
    # Check if 'image' exists in the request files
    if 'image' not in request.files:
        return "No file part", 400
    
    file = request.files['image']
    if file.filename == '':
        return "No selected file", 400
    
    # Read the image file bytes
    image_bytes = file.read()

    # Extract text and labels from the uploaded image using Rekognition
    extracted_text = extract_text_from_image(image_bytes)
    extracted_labels = extract_labels_from_image(image_bytes)

    # Generate ad content using Bedrock based on the extracted text and labels
    prompt_message = f"Create an ad based on the following text and labels: {extracted_text} {extracted_labels}"
    ad_content = generate(prompt_message)  # Call the generate function from bedrock_services

    # Check for violations using the generated ad content
    violation_result = check_for_violations(extracted_text, extracted_labels)  # Call the violation check function

    # Return the results to the template (rendering result.html)
    return render_template('result.html', 
                           extracted_text=extracted_text, 
                           extracted_labels=extracted_labels, 
                           ad_content=ad_content, 
                           violation_result=violation_result)

@main_bp.route('/generate_review', methods=['POST'])
def generate_review_req():
    # Get the ad content and generated requirements from the form data
    ad_content = request.form['ad_content']
    generated_requirements = request.form['generated_requirements']

    # Generate the review of the ad content
    review_content = check_for_violations(ad_content, generated_requirements)

    # Return the review content to the review template
    return render_template('review.html', review_content=review_content)
