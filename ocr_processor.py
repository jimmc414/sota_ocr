import os
import time
import json
from rich import print
from rich.console import Console

# For Google Cloud Vision API
from google.cloud import vision
from google.cloud import storage

# For AWS Textract
import boto3

# For Azure Computer Vision
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from msrest.authentication import CognitiveServicesCredentials

def process_google_vision(input_dir, output_dir, bucket_name, output_bucket_name):
    client = vision.ImageAnnotatorClient()
    storage_client = storage.Client()

    for filename in os.listdir(input_dir):
        if not filename.lower().endswith('.pdf'):
            continue

        input_path = os.path.join(input_dir, filename)

        print(f"[bold blue]Processing {filename} with Google Cloud Vision API...[/bold blue]")

        try:
            # Upload the file to GCS
            bucket = storage_client.bucket(bucket_name)
            blob = bucket.blob(filename)
            blob.upload_from_filename(input_path)

            gcs_source_uri = f'gs://{bucket_name}/{filename}'
            gcs_destination_uri = f'gs://{output_bucket_name}/{filename}/'

            mime_type = 'application/pdf'
            batch_size = 2

            feature = vision.Feature(type_=vision.Feature.Type.DOCUMENT_TEXT_DETECTION)

            gcs_source = vision.GcsSource(uri=gcs_source_uri)
            input_config = vision.InputConfig(gcs_source=gcs_source, mime_type=mime_type)

            gcs_destination = vision.GcsDestination(uri=gcs_destination_uri)
            output_config = vision.OutputConfig(gcs_destination=gcs_destination, batch_size=batch_size)

            async_request = vision.AsyncAnnotateFileRequest(
                features=[feature], input_config=input_config, output_config=output_config
            )

            operation = client.async_batch_annotate_files(requests=[async_request])

            print(f"[yellow]Waiting for operation to complete...[/yellow]")
            operation.result(timeout=180)

            # Process the output
            # The output is written to GCS as JSON files
            bucket = storage_client.bucket(output_bucket_name)
            blob_list = list(bucket.list_blobs(prefix=filename))

            text = ''

            for output_blob in blob_list:
                # Download the output json file
                json_string = output_blob.download_as_string()
                response = vision.AnnotateFileResponse.from_json(json_string)

                # The actual response for each page
                for page_response in response.responses:
                    annotation = page_response.full_text_annotation
                    text += annotation.text

            output_filename = f"{os.path.splitext(filename)[0]}_ocr.txt"
            output_path = os.path.join(output_dir, output_filename)

            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(text)

            print(f"[green]Successfully processed {filename}[/green]")

        except Exception as e:
            print(f"[red]Error processing {filename}: {e}[/red]")
            continue

def process_aws_textract(input_dir, output_dir, s3_bucket_name):
    textract_client = boto3.client('textract')
    s3_client = boto3.client('s3')

    for filename in os.listdir(input_dir):
        if not filename.lower().endswith('.pdf'):
            continue

        input_path = os.path.join(input_dir, filename)

        print(f"[bold blue]Processing {filename} with AWS Textract...[/bold blue]")

        try:
            # Upload the file to S3
            s3_client.upload_file(input_path, s3_bucket_name, filename)

            # Start Document Text Detection
            response = textract_client.start_document_text_detection(
                DocumentLocation={'S3Object': {'Bucket': s3_bucket_name, 'Name': filename}}
            )

            job_id = response['JobId']
            print(f"[yellow]Started job {job_id}, waiting for completion...[/yellow]")

            # Poll for job completion
            while True:
                job_status = textract_client.get_document_text_detection(JobId=job_id)
                status = job_status['JobStatus']
                if status in ['SUCCEEDED', 'FAILED']:
                    break
                time.sleep(5)

            if status == 'SUCCEEDED':
                # Retrieve and save the results
                pages = []
                next_token = None

                while True:
                    if next_token:
                        response = textract_client.get_document_text_detection(JobId=job_id, NextToken=next_token)
                    else:
                        response = textract_client.get_document_text_detection(JobId=job_id)

                    pages.append(response)
                    next_token = response.get('NextToken')
                    if not next_token:
                        break

                output_filename = f"{os.path.splitext(filename)[0]}_ocr.json"
                output_path = os.path.join(output_dir, output_filename)

                with open(output_path, 'w', encoding='utf-8') as f:
                    json.dump(pages, f)

                print(f"[green]Successfully processed {filename}[/green]")
            else:
                print(f"[red]Job {job_id} failed.[/red]")

        except Exception as e:
            print(f"[red]Error processing {filename}: {e}[/red]")
            continue

def process_azure_computer_vision(input_dir, output_dir, endpoint, subscription_key):
    client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))

    for filename in os.listdir(input_dir):
        if not filename.lower().endswith('.pdf'):
            continue

        input_path = os.path.join(input_dir, filename)
        output_filename = f"{os.path.splitext(filename)[0]}_ocr.txt"
        output_path = os.path.join(output_dir, output_filename)

        print(f"[bold blue]Processing {filename} with Azure Computer Vision...[/bold blue]")

        try:
            with open(input_path, 'rb') as image_file:
                image_data = image_file.read()

            # Call the Read API
            read_operation = client.read_in_stream(image_data, raw=True)

            # Get the operation location (URL with an ID at the end)
            operation_location = read_operation.headers["Operation-Location"]
            operation_id = operation_location.split("/")[-1]

            # Wait for the operation to complete
            print(f"[yellow]Waiting for operation to complete...[/yellow]")
            while True:
                read_result = client.get_read_result(operation_id)
                if read_result.status not in ['notStarted', 'running']:
                    break
                time.sleep(1)

            if read_result.status == 'succeeded':
                text = ""
                for page in read_result.analyze_result.read_results:
                    for line in page.lines:
                        text += line.text + '\n'

                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(text)

                print(f"[green]Successfully processed {filename}[/green]")
            else:
                print(f"[red]Error processing {filename}: Operation status {read_result.status}[/red]")

        except Exception as e:
            print(f"[red]Error processing {filename}: {e}[/red]")
            continue

def main():
    input_dir = './documents'

    print("[bold]Select the OCR service to use:[/bold]")
    print("1. Google Cloud Vision API")
    print("2. AWS Textract")
    print("3. Azure Computer Vision")
    choice = input("Enter the number of your choice: ")

    if choice == '1':
        output_dir = './google_ocr'
        os.makedirs(output_dir, exist_ok=True)
        bucket_name = input("Enter your GCS bucket name for input files: ")
        output_bucket_name = input("Enter your GCS bucket name for output files: ")
        process_google_vision(input_dir, output_dir, bucket_name, output_bucket_name)
    elif choice == '2':
        output_dir = './aws_ocr'
        os.makedirs(output_dir, exist_ok=True)
        s3_bucket_name = input("Enter your S3 bucket name for input files: ")
        process_aws_textract(input_dir, output_dir, s3_bucket_name)
    elif choice == '3':
        output_dir = './azure_ocr'
        os.makedirs(output_dir, exist_ok=True)
        endpoint = input("Enter your Azure endpoint URL: ")
        subscription_key = input("Enter your Azure subscription key: ")
        process_azure_computer_vision(input_dir, output_dir, endpoint, subscription_key)
    else:
        print("[red]Invalid choice. Exiting.[/red]")

if __name__ == '__main__':
    main()
