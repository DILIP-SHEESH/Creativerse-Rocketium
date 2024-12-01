# app/services/rekognition_service.py
import boto3
import os

# Initialize Rekognition client with credentials from environment variables
rekognition_client = boto3.client(
    'rekognition', 
    region_name=os.getenv('AWS_REGION', 'us-west-2'),
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
    aws_session_token=os.getenv('AWS_SESSION_TOKEN')
)

def extract_text_from_image(image_bytes):
    try:
        response = rekognition_client.detect_text(
            Image={'Bytes': image_bytes}
        )
        text_detections = response['TextDetections']
        extracted_text = ' '.join([item['DetectedText'] for item in text_detections])
        return extracted_text
    except Exception as e:
        return f"Error extracting text: {str(e)}"

def extract_labels_from_image(image_bytes):
    try:
        response = rekognition_client.detect_labels(
            Image={'Bytes': image_bytes},
            MaxLabels=10
        )
        labels = response['Labels']
        extracted_labels = ', '.join([label['Name'] for label in labels])
        return extracted_labels
    except Exception as e:
        return f"Error extracting labels: {str(e)}"
