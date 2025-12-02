import boto3
import os
import sys
import uuid
from urllib.parse import unquote_plus
from PIL import Image
import PIL.Image

# Initialize S3 client
s3_client = boto3.client('s3')

def convert_to_grayscale(image_path, grayscale_path):
    """Convert the image to grayscale and save it."""
    with Image.open(image_path) as image:
        grayscale_image = image.convert('L')  # 'L' mode is grayscale
        grayscale_image.save(grayscale_path)

def lambda_handler(event, context):
    processed_count = 0

    for record in event['Records']:
        bucket = record['s3']['bucket']['name']  # Same bucket
        key = unquote_plus(record['s3']['object']['key'])
        
        if not key.startswith("images/"):
            print(f"Skipping: {key} is not in 'images/' folder.")
            continue
        
        filename = key.replace('images/', '')

        if not filename:
            continue
        
        try:
            # Temporary paths for downloading and saving the grayscale image
            download_path = f"/tmp/{uuid.uuid4()}{filename}"
            grayscale_path = f"/tmp/grayscale-{filename}"
            
            # Download the image from S3
            s3_client.download_file(bucket, key, download_path)
            
            # Convert the image to grayscale
            convert_to_grayscale(download_path, grayscale_path)
            
            # Save the grayscale image to the same bucket but a different path
            output_key = f"grayscale/{filename}"  # Save in 'grayscale/' subdirectory

            # Upload
            s3_client.upload_file(grayscale_path, bucket, output_key)

            print(f"Successfully processed: {bucket}/{output_key}")
            processed_count += 1
        
        except Exception as e:
            print(f"Error processing {key}: {str(e)}")
    
    return {
        'statusCode': 200,
        'body': f"Successfully processed {processed_count} images."
    }

