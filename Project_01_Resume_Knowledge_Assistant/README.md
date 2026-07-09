# 🤖 Resume Knowledge Assistant

An AI-powered **Retrieval-Augmented Generation (RAG)** application that answers questions from resumes, certifications, project documents and technical notes using semantic search and Google Gemini.

---

## Features

- Semantic Search using FAISS
- Parent Document Retrieval
- Context Compression
- Cross Encoder Re-ranking
- Conversation Memory
- Streamlit Dashboard
- Retrieval Debugger
- Document Explorer
- Modular Architecture

---

## Screenshots

### Main Page

![Main Page](docs/screenshots/main_page.png)

---

### Debug Dashboard

![Debug](docs/screenshots/debug_page.png)

---

### Documents

![Documents](docs/screenshots/documents_page.png)

---

### Settings

![Settings](docs/screenshots/settings_page.png)

---

### About

![About](docs/screenshots/about_page.png)

---

## Project Architecture
![Architecture](docs/architecture.png)


---

## Project Structure
![Project Structure](docs/project_structure.png)


---

## Technology Stack

| Component | Technology |
|------------|------------|
| Language | Python 3.13 |
| UI | Streamlit |
| LLM | Google Gemini 2.5 Flash |
| Embeddings | all-MiniLM-L6-v2 |
| Re-ranking | Cross Encoder |
| Vector DB | FAISS |
| PDF Parsing | PyPDF |
| Testing | Custom Test Framework |

---

## Installation

```bash
git clone https://github.com/pacificpatel165/AI_Systems_Architect_Lab.git

cd Project_01_Resume_Knowledge_Assistant

pip install -r requirements/base.txt requirements/cpu.txt requirements/dev.txt

## Run CLI
python main.py

## Run Streamlit
python -m streamlit run ui/streamlit_app.py

## Run FastAPI
python -m uvicorn src.api.app:app --reload

## Display FastAPI 
http://127.0.0.1:8000/docs#/

## Run Tests
python main.py --test all
```

## 🐳 Docker

The FastAPI backend is containerized using Docker with a CPU-only
PyTorch runtime.

The Docker image includes:

- FastAPI API
- RAG pipeline
- FAISS vector store
- Sentence Transformer embeddings
- Cross-Encoder reranking
- CPU-only PyTorch
- Gemini integration

### Build the Image

```bash
docker build -t resume-knowledge-assistant:5.0.0 .
````

### Run the Container

```bash
docker run \
    --name resume-assistant-api \
    -p 8000:8000 \
    -e GEMINI_API_KEY="$GEMINI_API_KEY" \
    resume-knowledge-assistant:5.0.0
```

Open the FastAPI documentation:

```text
http://localhost:8000/docs
```

## 🐳 Docker Compose

Docker Compose manages the FastAPI service configuration.

Start the application:

```bash
docker compose up -d
```

Check the service:

```bash
docker compose ps
```

View logs:

```bash
docker compose logs -f
```

Stop the application:

```bash
docker compose down
```

## 🔄 Continuous Integration

The project uses GitHub Actions for Continuous Integration.

The CI pipeline runs automatically on:

* Push to `main`
* Pull requests targeting `main`

Pipeline stages:

```text
Code Quality and Tests
        │
        ├── Python 3.13
        ├── CPU PyTorch
        ├── Application Dependencies
        ├── Development Dependencies
        ├── Ruff
        └── RAG Test Suite
                │
                ▼
           Docker Build
```

The Docker image is built only after code quality checks and tests
complete successfully.

CI workflow:

```text
.github/workflows/ci.yaml
```

## 🔐 Environment Configuration

The application requires the following environment variable:

```text
GEMINI_API_KEY
```

For local Linux or WSL development, configure the variable in the shell
environment.

Example:

```bash
export GEMINI_API_KEY="YOUR_API_KEY"
```

The application reads configuration from the environment and does not
store the Gemini API key in the source code.

Docker Compose passes the environment variable into the container at
runtime.

## 🧪 Validation

Run code quality checks:

```bash
ruff check .
```

Run the complete RAG test suite:

```bash
python main.py --test all
```

Build the Docker image:

```bash
docker build -t resume-knowledge-assistant:ci .
```

These validation steps are also executed by the GitHub Actions CI
pipeline.

````

