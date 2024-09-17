# OCR Services Setup Guide

This guide provides step-by-step instructions for setting up accounts and authentication for Google Cloud Vision API, AWS Textract, and Microsoft Azure Computer Vision.

## Table of Contents
1. [Google Cloud Vision API Setup](#google-cloud-vision-api-setup)
2. [AWS Textract Setup](#aws-textract-setup)
3. [Microsoft Azure Computer Vision Setup](#microsoft-azure-computer-vision-setup)

## Google Cloud Vision API Setup

### 1. Create a Google Cloud Platform (GCP) Account
1. Go to [Google Cloud Console](https://console.cloud.google.com/).
2. Click on "Get Started for Free" or "Start Free" if you don't have an account.
3. Follow the prompts to create your account, providing the necessary information.

### 2. Set up a New Project
1. Once logged in, go to the [Google Cloud Console](https://console.cloud.google.com/).
2. Click on the project drop-down at the top of the page.
3. Click "New Project" in the top-right corner of the modal.
4. Enter a project name and click "Create".

### 3. Enable the Cloud Vision API
1. Go to the [Cloud Vision API page](https://console.cloud.google.com/apis/library/vision.googleapis.com).
2. Make sure your new project is selected in the top dropdown.
3. Click "Enable" to activate the API for your project.

### 4. Create a Service Account and Download JSON Key
1. Go to the [IAM & Admin > Service Accounts page](https://console.cloud.google.com/iam-admin/serviceaccounts).
2. Click "Create Service Account" at the top of the page.
3. Enter a service account name and click "Create".
4. For the "Service account permissions" step, you can skip it for now by clicking "Continue".
5. Click "Create Key", choose JSON as the key type, and click "Create".
6. The JSON key file will be downloaded to your computer. Keep this file secure.

### 5. Set Environment Variable
Set the `GOOGLE_APPLICATION_CREDENTIALS` environment variable to the path of your JSON key file:

- On Windows (Command Prompt):
  ```
  set GOOGLE_APPLICATION_CREDENTIALS=C:\path\to\your\service-account-file.json
  ```

- On macOS/Linux:
  ```
  export GOOGLE_APPLICATION_CREDENTIALS=/path/to/your/service-account-file.json
  ```

## AWS Textract Setup

### 1. Create an AWS Account
1. Go to the [AWS homepage](https://aws.amazon.com/).
2. Click "Create an AWS Account" or "Create a Free Account".
3. Follow the prompts to create your account, providing the necessary information.

### 2. Create an IAM User
1. Sign in to the [AWS Management Console](https://console.aws.amazon.com/).
2. Go to the IAM (Identity and Access Management) dashboard.
3. In the navigation pane, choose "Users" and then "Add user".
4. Enter a user name and select "Programmatic access" for Access type.
5. Click "Next: Permissions".
6. Choose "Attach existing policies directly" and search for "AmazonTextractFullAccess".
7. Select the checkbox next to "AmazonTextractFullAccess" and click "Next: Tags".
8. (Optional) Add tags if desired, then click "Next: Review".
9. Review the details and click "Create user".

### 3. Get Access Key ID and Secret Access Key
1. On the success page, you'll see the Access key ID and Secret access key.
2. Download the .csv file with these credentials or copy them somewhere secure.

### 4. Configure AWS CLI
Install the AWS CLI, then run:

```
aws configure
```

Enter your Access Key ID, Secret Access Key, default region (e.g., us-west-2), and output format (json).

Alternatively, you can set these as environment variables:

- On Windows (Command Prompt):
  ```
  set AWS_ACCESS_KEY_ID=your_access_key_id
  set AWS_SECRET_ACCESS_KEY=your_secret_access_key
  set AWS_DEFAULT_REGION=your_preferred_region
  ```

- On macOS/Linux:
  ```
  export AWS_ACCESS_KEY_ID=your_access_key_id
  export AWS_SECRET_ACCESS_KEY=your_secret_access_key
  export AWS_DEFAULT_REGION=your_preferred_region
  ```

## Microsoft Azure Computer Vision Setup

### 1. Create an Azure Account
1. Go to the [Azure portal](https://portal.azure.com/).
2. Click "Start free" or "Create a free account".
3. Follow the prompts to create your account, providing the necessary information.

### 2. Create a Computer Vision Resource
1. Sign in to the [Azure portal](https://portal.azure.com/).
2. Click "Create a resource" in the top-left corner.
3. Search for "Computer Vision" and select it from the results.
4. Click "Create".
5. Fill in the required details:
   - Subscription: Choose your subscription
   - Resource group: Create new or select existing
   - Region: Choose a region close to you
   - Name: Give your resource a unique name
   - Pricing tier: Choose 'Free F0' for testing, or a paid tier for production
6. Click "Review + create", then "Create" after review.

### 3. Get Endpoint URL and Subscription Key
1. Once deployment is complete, click "Go to resource".
2. In the left menu, under "Resource Management", click "Keys and Endpoint".
3. You'll see two keys and the endpoint URL. You can use either key.

You'll need to provide these when prompted by the OCR program:
- Endpoint URL (e.g., https://your-resource-name.cognitiveservices.azure.com/)
- One of the subscription keys

