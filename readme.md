# Multi-Service SotA OCR Processor

## Overview

The Multi-Service OCR Processor is a Python program designed to help users maximize their use of free OCR (Optical Character Recognition) services offered by leading cloud providers. By integrating Google Cloud Vision API, Amazon Web Services (AWS) Textract, and Microsoft Azure Computer Vision, this tool allows users to process PDF files using the free tier limits of each service before needing to pay for additional usage.

The program reads PDF files from an input directory, processes them using the selected OCR service, and saves the results in a designated output directory. By providing easy switching between services, users can efficiently utilize the free quotas of all three providers, potentially processing a significant number of documents without incurring costs.

## Key Benefit: Maximizing Free Tier Usage

This project's primary purpose is to help users leverage the free tier offerings of multiple cloud OCR services:

- **Google Cloud Vision API**: Offers 1,000 free document text detections per month.
- **AWS Textract**: Provides 1,000 free pages per month for the first 3 months.
- **Microsoft Azure Computer Vision**: Offers 5,000 free transactions per month.

By using this tool, you can:

1. Easily switch between services to use their respective free quotas.
2. Potentially process thousands of pages per month without cost.
3. Compare the OCR results from different providers to choose the best for your needs.
4. Delay the need for paid services by fully utilizing available free tiers.

## Features

- Support for three leading OCR services:
  - Google Cloud Vision API
  - AWS Textract
  - Microsoft Azure Computer Vision
- Batch processing of PDF files
- Simple command-line interface for service selection
- Colored console output for better readability
- Basic error handling and logging

## Prerequisites

- Python 3.7 or higher
- An active account and proper authentication set up for the desired OCR service(s)
- Required Python libraries (see [Installation](#installation))

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/jimmc414/sota_ocr.git
   cd sota_ocr
   ```

2. (Optional) Create and activate a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required libraries:
   ```
   pip install google-cloud-vision google-cloud-storage boto3 azure-cognitiveservices-vision-computervision msrest rich
   ```

## Setup

Before using the OCR processor, you need to set up accounts and authentication for the desired OCR services. Please refer to our [OCR Services Setup Guide](OCR_SERVICES_SETUP_GUIDE.md) for detailed instructions on how to:

- Create accounts for Google Cloud Platform, AWS, and Microsoft Azure
- Set up the necessary APIs and resources
- Obtain and configure authentication credentials

## Usage

1. Place the PDF files you want to process in the `./documents` directory.

2. Run the program:
   ```
   python ocr_processor.py
   ```

3. When prompted, select the OCR service you want to use by entering the corresponding number:
   - 1 for Google Cloud Vision API
   - 2 for AWS Textract
   - 3 for Azure Computer Vision

4. Provide any additional information requested (e.g., bucket names, endpoints).

5. The program will process each PDF file and save the OCR results in the designated output directory:
   - `./google_ocr` for Google Cloud Vision API
   - `./aws_ocr` for AWS Textract
   - `./azure_ocr` for Azure Computer Vision

6. To maximize free tier usage, run the program multiple times, choosing a different service each time until you've utilized the free limits of all services.

## Output Formats

- Google Cloud Vision API: Text file containing extracted text
- AWS Textract: JSON file containing extracted text and additional information
- Azure Computer Vision: Text file containing extracted text

## Error Handling

The program implements basic error handling:
- Files that cannot be processed are skipped
- Error messages are printed to the console using colored output
- Basic error information (file name and error type) is logged for failed OCR attempts

## Limitations

- The program currently processes files sequentially
- Only top-level files in the input directory are processed
- Azure Computer Vision implementation may not handle multi-page PDFs correctly
- Users are responsible for tracking their own usage to avoid exceeding free tier limits

## Future Enhancements

- Implement parallel processing for improved performance
- Add support for additional file types (e.g., JPEG, PNG)
- Implement more advanced error handling and logging
- Add command-line arguments for customization (e.g., input/output directories, service selection)
- Integrate usage tracking to help users monitor their free tier consumption

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Notes

- This project uses the following OCR services:
  - [Google Cloud Vision API](https://cloud.google.com/vision)
  - [Amazon Textract](https://aws.amazon.com/textract/)
  - [Microsoft Azure Computer Vision](https://azure.microsoft.com/en-us/services/cognitive-services/computer-vision/)