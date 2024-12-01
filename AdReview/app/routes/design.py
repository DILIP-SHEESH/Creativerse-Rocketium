from flask import Blueprint, render_template, request
from app.services.rekognition_service import extract_text_from_image, extract_labels_from_image
from app.services.bedrock_services import check_for_violations

# Design Blueprint for handling uploaded images
design_bp = Blueprint('design', __name__)

@design_bp.route('/design', methods=['GET', 'POST'])
def design_view():
    if request.method == 'POST':
        file = request.files['image']
        if file:
            image_bytes = file.read()

            # Extract text and labels from the image
            extracted_text = extract_text_from_image(image_bytes)
            extracted_labels = extract_labels_from_image(image_bytes)

            # Check for violations using Bedrock
            violation_result = check_for_violations(extracted_text, extracted_labels)

            return render_template('design/result.html', 
                                   extracted_text=extracted_text, 
                                   extracted_labels=extracted_labels, 
                                   violation_result=violation_result)

    return render_template('design/index.html')

@design_bp.route('/ongoing_projects')
def ongoing_projects():
    # In a real app, you might fetch the actual ongoing projects from a database.
    ongoing_projects_list = [
        {"name": "Project 1", "status": "In Progress"},
        {"name": "Project 2", "status": "Pending"},
        {"name": "Project 3", "status": "Completed"}
    ]
    return render_template('design/ongoing_projects.html', projects=ongoing_projects_list)