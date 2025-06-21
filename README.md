# CPR Legal Assistant

An AI-powered legal assistant that helps navigate Civil Procedure Rules (CPR) and Practice Directions using Retrieval-Augmented Generation (RAG) on Google Cloud Platform.

## 🚀 Features

- **Smart Legal Q&A**: Ask questions about civil procedure and get accurate, cited answers
- **Step-by-Step Checklists**: Generate actionable checklists for legal processes
- **User Type Differentiation**: Tailored responses for private individuals vs. legal professionals
- **Source Citations**: Always see which rules and practice directions inform the answers
- **Chat History**: Maintain conversation context across sessions
- **GCP Integration**: Powered by Vertex AI and Cloud Storage

## 📥 Data Setup

The legal documents (CPR and Practice Directions) are not included in this repository due to size constraints. To run the application:

1. **Download the data**: The markdown files are available from the vLex hackathon organizers
2. **Place in `cpr_data/` folder**: Extract the files to a `cpr_data/` directory in your project root
3. **File structure should be**:
   ```
   cpr_data/
   ├── cpr_data_links.json
   ├── 23 Part 7 - How to start Proceedings – The Claim Form.md
   ├── 24 Practice Direction 7A - How to Start Proceedings.md
   └── ... (other .md files)
   ```

## 🏗️ Architecture

```
User → Cloud Load Balancer → Cloud Run (App) → Vertex AI (Embeddings/LLM)
                                    ↓
                              Cloud Storage (Vector DB)
```

## 📁 Project Structure

```
├── gcp_app/                # GCP production version
│   ├── app.py              # Enhanced Streamlit app
│   ├── config.py           # GCP configuration
│   ├── data_utils.py       # Data processing
│   ├── gcp_embeddings.py   # Vertex AI embeddings
│   ├── gcp_llm.py          # Vertex AI LLM
│   └── gcp_retriever.py    # GCP-based retrieval
├── cpr_data/               # Legal documents (markdown) - download separately
├── Dockerfile              # Container configuration
├── deploy.sh               # Deployment script
├── gcp_requirements.txt    # GCP dependencies
└── README.md               # Documentation
```

## 🛠️ Local Development

### Prerequisites

- Python 3.11+
- pip
- Virtual environment
- CPR data files (see Data Setup above)
- Google Cloud Platform account with billing enabled

### Setup

1. **Clone and navigate to the project:**
   ```bash
   cd hackathon
   ```

2. **Download and extract the CPR data** to the `cpr_data/` folder

3. **Create virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

4. **Install GCP dependencies:**
   ```bash
   pip install -r gcp_requirements.txt
   ```

5. **Set up GCP authentication:**
   ```bash
   gcloud auth login
   gcloud config set project YOUR_PROJECT_ID
   ```

6. **Run the GCP version locally:**
   ```bash
   PYTHONPATH=. streamlit run gcp_app/app.py
   ```

## ☁️ GCP Deployment

### Prerequisites

- Google Cloud Platform account
- gcloud CLI installed and authenticated
- Docker installed
- Project with billing enabled
- CPR data files (see Data Setup above)

### Quick Deployment

1. **Set your project ID:**
   ```bash
   export PROJECT_ID="your-project-id"
   ```

2. **Make deploy script executable:**
   ```bash
   chmod +x deploy.sh
   ```

3. **Deploy:**
   ```bash
   ./deploy.sh $PROJECT_ID us-central1
   ```

### Manual Deployment

1. **Enable APIs:**
   ```bash
   gcloud services enable aiplatform.googleapis.com
   gcloud services enable run.googleapis.com
   gcloud services enable storage.googleapis.com
   ```

2. **Create service account:**
   ```bash
   gcloud iam service-accounts create rag-app-sa \
       --display-name="RAG App Service Account"
   
   gcloud projects add-iam-policy-binding $PROJECT_ID \
       --member="serviceAccount:rag-app-sa@$PROJECT_ID.iam.gserviceaccount.com" \
       --role="roles/aiplatform.user"
   ```

3. **Build and deploy:**
   ```bash
   docker build -t gcr.io/$PROJECT_ID/cpr-legal-assistant .
   docker push gcr.io/$PROJECT_ID/cpr-legal-assistant
   
   gcloud run deploy cpr-legal-assistant \
       --image gcr.io/$PROJECT_ID/cpr-legal-assistant \
       --platform managed \
       --region us-central1 \
       --allow-unauthenticated
   ```

## 🔧 Configuration

### Environment Variables

- `GOOGLE_CLOUD_PROJECT`: Your GCP project ID
- `GOOGLE_CLOUD_REGION`: GCP region (default: us-central1)
- `VECTOR_BUCKET_NAME`: Cloud Storage bucket for vectors

### Model Configuration

Edit `gcp_app/config.py` to change:
- Embedding model (default: `textembedding-gecko@001`)
- LLM model (default: `text-bison@001` or `gemini-pro`)
- Chunk size and overlap
- Number of retrieved results

## 💰 Cost Optimization

- **Embeddings**: Use `textembedding-gecko@001` (cheaper than gecko@002)
- **LLM**: Use `text-bison@001` for cost, `gemini-pro` for quality
- **Storage**: Cloud Storage is very cost-effective
- **Compute**: Cloud Run scales to zero when not in use

## 🔒 Security

- Service accounts with minimal required permissions
- No sensitive data in code
- Environment variables for configuration
- Container runs as non-root user

## 📊 Monitoring

- Cloud Run provides built-in metrics
- Vertex AI has usage monitoring
- Cloud Storage access logs
- Consider adding Cloud Logging for custom metrics

## 🚀 Next Steps

- [ ] Add Notion integration for checklist export
- [ ] Implement PDF generation
- [ ] Add user authentication
- [ ] Set up monitoring and alerting
- [ ] Add more legal document sources
- [ ] Implement conversation memory
- [ ] Add voice input/output

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## ⚖️ Legal Disclaimer

This tool is for informational purposes only and does not constitute legal advice. Always consult with a qualified legal professional for specific legal matters. 