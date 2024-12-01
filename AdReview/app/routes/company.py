'''from flask import Blueprint, render_template, request
from app.services.bedrock_services import generate_req_data, generate

company_bp = Blueprint('company', __name__)

@company_bp.route('/company', methods=['GET', 'POST'])
def company_view():
    if request.method == 'POST':
        # Extract the form data
        project_name = request.form.get('project_name', 'Unknown Project')
        description = request.form.get('description', 'No Description')
        ad_for_platform = request.form.get('ad_for_platform', 'General Platform')
        ad_type = request.form.get('ad_type', 'Generic')  # Optional
        platform_guidelines = request.form.get('platform_guidelines', 'No Platform Guidelines')  # Optional

        # Generate the request data for the ad
        prompt_message = generate_req_data(project_name, description, ad_for_platform, ad_type, platform_guidelines)
        
        # Generate the ad content based on the request data
        generated_ad = generate(prompt_message)

        # Render the submission details page with the form data and generated ad content
        return render_template('company/submission_details.html', 
                               project_name=project_name, 
                               description=description, 
                               ad_for_platform=ad_for_platform, 
                               ad_type=ad_type, 
                               ad_content=generated_ad)

    return render_template('company/index.html')
'''
'''from flask import Blueprint, render_template, request

company_bp = Blueprint('company', __name__)

@company_bp.route('/company', methods=['GET', 'POST'])
def company_view():
    if request.method == 'POST':
        project_name = request.form.get('project_name', 'Unknown Project')
        description = request.form.get('description', 'No Description')
        company_guidelines = request.form.get('company_guidelines', 'No Guidelines')
        ad_for_platform = request.form.get('ad_for_platform', 'General Platform')
        platform_guidelines = request.form.get('platform_guidelines', 'No Platform Guidelines')
        ad_type = request.form.get('ad_type', 'Generic')

        # Instead of generating the ad with AI, use the data provided
        ad_content = f"""
        **Project Name**: {project_name}
        **Ad Description**: {description}
        **Company Guidelines**: {company_guidelines}
        **Ad for Platform**: {ad_for_platform}
        **Platform Guidelines**: {platform_guidelines}
        **Ad Type**: {ad_type}
        """
        
        # Render result page with the provided ad content (direct submission)
        return render_template('company/submission_details.html', ad_content=ad_content, project_name=project_name)

    return render_template('company/index.html')'''

from flask import Blueprint, render_template, request, session
from app.services.bedrock_services import generate_req_data, generate

company_bp = Blueprint('company', __name__)

@company_bp.route('/company', methods=['GET', 'POST'])
def company_view():
    if request.method == 'POST':
        project_name = request.form.get('project_name', 'Unknown Project')
        description = request.form.get('description', 'No Description')
        company_guidelines = request.form.get('company_guidelines', 'No Guidelines')
        ad_for_platform = request.form.get('ad_for_platform', 'General Platform')
        platform_guidelines = request.form.get('platform_guidelines', 'No Platform Guidelines')
        ad_type = request.form.get('ad_type', 'Generic')

       # Generate the prompt message using the provided form data
        prompt_message = generate_req_data(project_name, description, company_guidelines, ad_for_platform, platform_guidelines, ad_type)

        # Generate the ad content using the prompt message (i.e., invoke the AI model)
        requirements_data = generate(prompt_message)

        # Store the generated ad content (requirements_data) in the session
        session['requirements_data'] = requirements_data

        print("Generated Requirements Data:", requirements_data)

        # Render the submission details page with the form data
        return render_template('company/submission_details.html', 
                               project_name=project_name, 
                               description=description,
                               company_guidelines=company_guidelines,
                               ad_for_platform=ad_for_platform,
                               platform_guidelines=platform_guidelines,
                               ad_type=ad_type,
                               requirements_data=requirements_data)

    return render_template('company/index.html')

@company_bp.route('/ongoing_projects', methods=['GET'])
def ongoing_projects():
    # Retrieve the stored requirements_data from the session
    requirements_data = session.get('requirements_data', 'No data available.')

    # Render the template and pass the requirements data
    return render_template('design/ongoing_projects.html', requirements_data=requirements_data)
