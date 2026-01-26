# 🏕️ Camping La Rosaleda - AI Receptionist Agent

An intelligent virtual receptionist for Camping La Rosaleda, built with Google ADK (Agent Development Kit) and Vertex AI RAG Engine.

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Google Cloud](https://img.shields.io/badge/Google_Cloud-4285F4?style=for-the-badge&logo=google-cloud&logoColor=white)
![Vertex AI](https://img.shields.io/badge/Vertex_AI-4285F4?style=for-the-badge&logo=google-cloud&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)

## 🛠️ Tech Stack

| Category | Technology |
|----------|------------|
| **AI Framework** | ![Google ADK](https://img.shields.io/badge/Google_ADK-1.10.0-4285F4?style=flat-square&logo=google&logoColor=white) |
| **LLM** | ![Gemini](https://img.shields.io/badge/Gemini_2.0_Flash-8E75B2?style=flat-square&logo=google&logoColor=white) |
| **RAG Engine** | ![Vertex AI RAG](https://img.shields.io/badge/Vertex_AI_RAG_Engine-4285F4?style=flat-square&logo=google-cloud&logoColor=white) |
| **Deployment** | ![Cloud Run](https://img.shields.io/badge/Cloud_Run-4285F4?style=flat-square&logo=google-cloud&logoColor=white) ![Agent Engine](https://img.shields.io/badge/Agent_Engine-4285F4?style=flat-square&logo=google-cloud&logoColor=white) |
| **Observability** | ![Arize](https://img.shields.io/badge/Arize_AI-FF6B6B?style=flat-square) ![OpenTelemetry](https://img.shields.io/badge/OpenTelemetry-425CC7?style=flat-square&logo=opentelemetry&logoColor=white) |
| **Frontend** | ![Streamlit](https://img.shields.io/badge/Streamlit-1.53-FF4B4B?style=flat-square&logo=streamlit&logoColor=white) |
| **Package Manager** | ![UV](https://img.shields.io/badge/UV-DE5FE9?style=flat-square) |

## 📋 Features

- **RAG-Powered Responses**: Uses Vertex AI RAG Engine to retrieve accurate camping information
- **Exact Pricing**: Provides precise prices based on season (Low/Medium/High)
- **Multi-Channel Deployment**:
  - 🌐 Streamlit Web UI (Cloud Run)
  - 🤖 Vertex AI Agent Engine API
  - 💻 Local development with `adk web`
- **Observability**: Full tracing with Arize AI (EU region supported)
- **Spanish Language**: Fully localized for Spanish-speaking users

## 🏗️ Architecture

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│   Streamlit UI  │────▶│   Google ADK     │────▶│  Vertex AI RAG  │
│   (Cloud Run)   │     │   Agent Runner   │     │     Engine      │
└─────────────────┘     └──────────────────┘     └─────────────────┘
                               │                         │
                               ▼                         ▼
                        ┌──────────────┐         ┌─────────────────┐
                        │  Gemini 2.0  │         │  RAG Corpus     │
                        │    Flash     │         │  (Camping Data) │
                        └──────────────┘         └─────────────────┘
                               │
                               ▼
                        ┌──────────────┐
                        │   Arize AI   │
                        │   Tracing    │
                        └──────────────┘
```

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- [UV](https://docs.astral.sh/uv/) package manager
- Google Cloud account with billing enabled
- [gcloud CLI](https://cloud.google.com/sdk/docs/install) installed and configured

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Acquarts/google-adk-rag-agent-camping-receptionist.git
   cd google-adk-rag-agent-camping-receptionist
   ```

2. **Install dependencies**
   ```bash
   uv sync
   ```

3. **Configure environment variables**
   ```bash
   cp .env-example .env
   # Edit .env with your credentials
   ```

4. **Run locally**
   ```bash
   # Option 1: ADK Web Interface
   uv run adk web

   # Option 2: Streamlit UI
   uv run streamlit run app.py
   ```

## ⚙️ Configuration

Create a `.env` file with the following variables:

```env
# Google Cloud
GOOGLE_GENAI_USE_VERTEXAI=1
GOOGLE_CLOUD_PROJECT=your-project-id
GOOGLE_CLOUD_LOCATION=europe-west1

# RAG Corpus
RAG_CORPUS=projects/your-project/locations/europe-west1/ragCorpora/your-corpus-id

# Staging bucket for deployment
STAGING_BUCKET=gs://your-bucket-name

# (Optional) Arize Tracing
ARIZE_SPACE_ID=your-space-id
ARIZE_API_KEY=your-api-key
```

## 📦 Deployment

### Deploy to Cloud Run (Streamlit UI)

```bash
gcloud run deploy camping-la-rosaleda \
  --source . \
  --region europe-west1 \
  --allow-unauthenticated \
  --set-env-vars "GOOGLE_GENAI_USE_VERTEXAI=1,GOOGLE_CLOUD_PROJECT=your-project,GOOGLE_CLOUD_LOCATION=europe-west1,RAG_CORPUS=your-corpus"
```

### Deploy to Vertex AI Agent Engine

```bash
uv run python deployment/deploy.py
```

## 🗓️ Camping Seasons & Pricing

| Season | Dates |
|--------|-------|
| **Low** | Jan 1 - Apr 30, Oct 1 - Dec 31 |
| **Medium** | May 1 - Jul 10, Aug 16 - Sep 30 |
| **High** | Jul 11 - Aug 15 |

The agent automatically calculates prices based on the current season and provides exact totals for reservations.

## 📁 Project Structure

```
├── app.py                 # Streamlit UI
├── rag/
│   ├── agent.py           # Main agent definition
│   ├── prompts.py         # System prompts with pricing
│   └── tracing.py         # Arize observability setup
├── deployment/
│   └── deploy.py          # Vertex AI Agent Engine deployment
├── Dockerfile             # Cloud Run container
└── pyproject.toml         # Dependencies
```

## 🔍 Observability

This project uses [Arize AI](https://arize.com/) for LLM tracing and observability. Traces are sent to the EU endpoint (`otlp.eu-west-1a.arize.com`) for GDPR compliance.

## 📄 License

Apache License 2.0

## 👤 Author

**Adrian Acquaroni**

- GitHub: [@Acquarts](https://github.com/Acquarts)

---

<p align="center">
  Made with ❤️ using Google ADK and Vertex AI
</p>
