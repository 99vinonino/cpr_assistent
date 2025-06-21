#!/bin/bash

# Upload CPR Data to Cloud Storage
# Usage: ./upload_data.sh [PROJECT_ID] [BUCKET_NAME]

set -e

PROJECT_ID=${1:-"your-project-id"}
BUCKET_NAME=${2:-"$PROJECT_ID-cpr-data"}

echo "📤 Uploading CPR data to Cloud Storage..."
echo "Project: $PROJECT_ID"
echo "Bucket: $BUCKET_NAME"

# Create bucket if it doesn't exist
echo "🪣 Creating bucket..."
gsutil mb -l us-central1 gs://$BUCKET_NAME 2>/dev/null || echo "Bucket already exists"

# Upload all markdown files
echo "📁 Uploading markdown files..."
gsutil -m cp cpr_data/*.md gs://$BUCKET_NAME/

# Upload JSON file
echo "📄 Uploading JSON file..."
gsutil cp cpr_data/*.json gs://$BUCKET_NAME/

echo "✅ Upload complete!"
echo "🌐 Files available at: gs://$BUCKET_NAME/"
echo ""
echo "📝 Next steps:"
echo "1. Update gcp_app/config.py with bucket name: $BUCKET_NAME"
echo "2. Deploy your application" 