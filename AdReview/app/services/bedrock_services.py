'''import boto3
import os
import json
import time

# Initialize the Bedrock client
def get_bedrock_client():
    return boto3.client(
        'bedrock-runtime',
        region_name='us-west-2',  # You can change the region as needed
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
        aws_session_token=os.getenv('AWS_SESSION_TOKEN')
    )

bedrock_runtime = get_bedrock_client()

# Function to generate the request data for the prompt
def generate_req_data(project_name, description, company_guidelines, ad_for_platform, platform_guidelines, ad_type):
    prompt = f"""
    The parameters are:
    Project Name: {project_name}
    Description: {description}
    Company Guidelines: {company_guidelines}
    Ad for the Platform: {ad_for_platform}
    Platform Guidelines: {platform_guidelines}
    Type of the Ad: {ad_type}
    Ensure the ad adheres to the guidelines provided.
    """
    prompt_message = (
        "You are the head of marketing and you are asking your design team to create an Ad based on the given parameters. "
        "Provide a detailed and clear description of the ad with a title, guidelines for the designer, and any restrictions to follow. "
        "If the description is not provided, treat it as a search request and perform the necessary actions. "
        "If company guidelines are not provided, disregard them and use the platform name to identify the platform’s ad guidelines.\n\n"
        f"User prompt: {prompt}"
    )
    return prompt_message

def generate(prompt_message):
    kwargs = {
        "modelId": "meta.llama3-8b-instruct-v1:0",
        "contentType": "application/json",
        "accept": "application/json",
        "body": json.dumps({
            "prompt": prompt_message
        })
    }

    response = bedrock_runtime.invoke_model(**kwargs)

    body = json.loads(response['body'].read())

    ad_content = body.get('generation', 'No content generated.')

    formatted_ad = ad_content.replace("\\n", "\n").strip()

    return formatted_ad

def check_for_violations(given_ad, given_req, max_retries=10, delay=1):
    """
    Combines the review and violation check into one function. 
    It retries the API call up to `max_retries` times if no content is generated.
    """
    retries = 0
    while retries < max_retries:
        prompt_message = (
            f"Answer in the following format:\n\n"
            f"Guideline/Rule followed by Analysis of the Ad Content against the Requirements to specify if the guideline/rule is being followed\n\n"
            f"Calculate and display the percentage of guidelines being followed\n\n"
            f"Ad Content: {given_ad}\n\n"
            f"Requirements: {given_req}\n\n"
            f"Additionally, answer if the ad content is safe or harmful (Safe/Not Safe)."
        )

        # Define the model request for reviewing the ad and checking for violations
        review_kwargs = {
            "modelId": "meta.llama3-8b-instruct-v1:0",  # Specify model
            "contentType": "application/json",  # Request content type
            "accept": "application/json",  # Accept response as JSON
            "body": json.dumps({"prompt": prompt_message})  # Passing the user prompt as JSON body
        }

        # Call the API to generate the review and check violations
        response = bedrock_runtime.invoke_model(**review_kwargs)

        # Parse the response
        body = json.loads(response['body'].read())

        # Get the generated content (review and violation check)
        review_content = body.get('generation', '')

        if review_content:
            # Clean and format the response
            cleaned_content = review_content.strip()

            # Return the cleaned review content and safety status (if included)
            return cleaned_content
        else:
            # If no review content is generated, increment the retry counter and wait
            retries += 1
            print(f"Retry {retries}/{max_retries}... No content generated.")
            time.sleep(delay)  # Delay before retrying

    # If we reach here, it means the API failed to generate content after max_retries
    return "No meaningful content generated after multiple attempts. Please try again later."
'''
import boto3
import os
import json
import time

# Initialize the Bedrock client
def get_bedrock_client():
    return boto3.client(
        'bedrock-runtime',
        region_name='us-west-2',  # You can change the region as needed
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
        aws_session_token=os.getenv('AWS_SESSION_TOKEN')
    )

bedrock_runtime = get_bedrock_client()

# Function to generate the request data for the prompt
def generate_req_data(project_name, description, company_guidelines, ad_for_platform, platform_guidelines="Platform specific guidelines", ad_type="Generic"):
    prompt = f"""
    The parameters are:
    Project Name: {project_name}
    Description: {description}
    Company Guidelines: {company_guidelines}
    Ad for the Platform: {ad_for_platform}
    Platform Guidelines: {platform_guidelines}
    Type of the Ad: {ad_type}
    Ensure the ad adheres to the guidelines provided.
    """
    prompt_message = (
        "You are the head of marketing and you are asking your design team to create an Ad based on the given parameters. "
        "Provide a detailed and clear description of the ad with a title, guidelines for the designer, and any restrictions to follow. "
        "If the description is not provided, treat it as a search request and perform the necessary actions. "
        "If company guidelines are not provided, disregard them and use the platform name to identify the platforms ad guidelines.\n\n"
        f"User prompt: {prompt}"
    )
    
    return prompt_message

# Function to generate ad content using Bedrock's model
def generate(prompt_message):
    kwargs = {
        "modelId": "meta.llama3-8b-instruct-v1:0",  # Use the desired model
        "contentType": "application/json",
        "accept": "application/json",
        "body": json.dumps({
            "prompt": prompt_message
        })
    }

    response = bedrock_runtime.invoke_model(**kwargs)

    body = json.loads(response['body'].read())

    ad_content = body.get('generation', 'No content generated.')

    formatted_ad = ad_content.replace("\\n", "\n").strip()

    return formatted_ad

# Function to check for violations and review the ad content
def check_for_violations(given_ad, given_req, max_retries=10, delay=1):
    """
    Combines the review and violation check into one function.
    It retries the API call up to `max_retries` times if no content is generated.
    """
    retries = 0
    while retries < max_retries:
        prompt_message = (
            f"Answer in the following format:"
            f"Calculate and display the percentage of compliance being followed \n\n"
            f"Guideline/Rule to be followed by Analysis of the Ad Content against the Requirements to specify if the guideline/rule is being followed\n\n"
            f"Ad Content: {given_ad}\n\n"
            f"Requirements: {given_req}\n\n"
            f"Additionally, Give feedback on how to resolve or get a better compliance if the ad content is bad or harmful (Safe/Not Safe)."
        )

        # Define the model request for reviewing the ad and checking for violations
        review_kwargs = {
            "modelId": "meta.llama3-8b-instruct-v1:0",  # Specify model
            "contentType": "application/json",  # Request content type
            "accept": "application/json",  # Accept response as JSON
            "body": json.dumps({"prompt": prompt_message})  # Passing the user prompt as JSON body
        }

        # Call the API to generate the review and check violations
        response = bedrock_runtime.invoke_model(**review_kwargs)

        # Parse the response
        body = json.loads(response['body'].read())

        # Get the generated content (review and violation check)
        review_content = body.get('generation', '')

        if review_content:
            # Clean and format the response
            cleaned_content = review_content.strip()

            # Return the cleaned review content and safety status (if included)
            return cleaned_content
        else:
            # If no review content is generated, increment the retry counter and wait
            retries += 1
            print(f"Retry {retries}/{max_retries}... No content generated.")
            time.sleep(delay)  # Delay before retrying

    # If we reach here, it means the API failed to generate content after max_retries
    return "No meaningful content generated after multiple attempts. Please try again later."


