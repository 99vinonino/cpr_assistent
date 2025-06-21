#!/bin/bash

# GCP Deployment Script for CPR Legal Assistant
# Usage: ./deploy.sh [PROJECT_ID] [REGION]

set -e

# Default values
PROJECT_ID=${1:-"your-project-id"}
REGION=${2:-"us-central1"}
SERVICE_NAME="cpr-legal-assistant"
IMAGE_NAME="gcr.io/$PROJECT_ID/$SERVICE_NAME"

echo "🚀 Deploying CPR Legal Assistant to GCP"
echo "Project: $PROJECT_ID"
echo "Region: $REGION"
echo "Service: $SERVICE_NAME"

# Check if gcloud is authenticated
if ! gcloud auth list --filter=status:ACTIVE --format="value(account)" | grep -q .; then
    echo "❌ Not authenticated with gcloud. Please run: gcloud auth login"
    exit 1
fi

# Set project
echo "📋 Setting GCP project..."
gcloud config set project $PROJECT_ID

# Enable required APIs
echo "🔧 Enabling required APIs..."
gcloud services enable aiplatform.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable storage.googleapis.com
gcloud services enable cloudbuild.googleapis.com
gcloud services enable containerregistry.googleapis.com

# Create Cloud Storage buckets
VECTOR_BUCKET_NAME="$PROJECT_ID-vectors"
DATA_BUCKET_NAME="$PROJECT_ID-cpr-data"

echo "🪣 Creating Cloud Storage buckets..."
gsutil mb -l $REGION gs://$VECTOR_BUCKET_NAME 2>/dev/null || echo "Vector bucket already exists"
gsutil mb -l $REGION gs://$DATA_BUCKET_NAME 2>/dev/null || echo "Data bucket already exists"

# Upload data files if they exist locally
if [ -d "cpr_data" ]; then
    echo "📤 Uploading data files to Cloud Storage..."
    gsutil -m cp cpr_data/*.md gs://$DATA_BUCKET_NAME/ 2>/dev/null || echo "No markdown files to upload"
    gsutil cp cpr_data/*.json gs://$DATA_BUCKET_NAME/ 2>/dev/null || echo "No JSON files to upload"
    echo "✅ Data uploaded to gs://$DATA_BUCKET_NAME/"
else
    echo "⚠️  No local cpr_data directory found. Please upload data files manually to gs://$DATA_BUCKET_NAME/"
fi

# Build and push Docker image
echo "🐳 Building Docker image..."
docker build --platform=linux/amd64 -t $IMAGE_NAME .

echo "📤 Pushing image to Container Registry..."
docker push $IMAGE_NAME

# Deploy to Cloud Run
echo "🚀 Deploying to Cloud Run..."
gcloud run deploy $SERVICE_NAME \
    --image $IMAGE_NAME \
    --platform managed \
    --region $REGION \
    --allow-unauthenticated \
    --memory 2Gi \
    --cpu 2 \
    --timeout 300 \
    --set-env-vars "GOOGLE_CLOUD_PROJECT=$PROJECT_ID,GOOGLE_CLOUD_REGION=$REGION,VECTOR_BUCKET_NAME=$VECTOR_BUCKET_NAME,DATA_BUCKET_NAME=$DATA_BUCKET_NAME"

# Get the service URL
SERVICE_URL=$(gcloud run services describe $SERVICE_NAME --region=$REGION --format="value(status.url)")

echo "✅ Deployment complete!"
echo "🌐 Service URL: $SERVICE_URL"
echo ""
echo "📝 Next steps:"
echo "1. Set up authentication (service account key or workload identity)"
echo "2. Test the application"
echo "3. Set up monitoring and logging" 