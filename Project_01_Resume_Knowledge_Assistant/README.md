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

## ⚙️ Runtime Configuration

The Resume Knowledge Assistant supports environment-based runtime configuration.

Runtime settings are loaded by `src/config.py` and can be configured using environment variables.

| Environment Variable | Default | Description |
|---|---|---|
| `GEMINI_API_KEY` | None | Gemini API key used by the LLM client |
| `USE_LLM` | `true` | Enables or disables Gemini LLM response generation |
| `DEBUG_MODE` | `false` | Enables additional application debug logging |
| `LOG_LEVEL` | `INFO` | Controls the application logging level |

---

### Gemini API Key

The Gemini API key must be available as an environment variable.

Example:

```bash
export GEMINI_API_KEY="your-api-key"
```

The application reads the value using:

```python
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
```

For local Linux or WSL development, the environment variable can be configured in `~/.bashrc`.

```bash
export GEMINI_API_KEY="your-api-key"
```

Reload the shell configuration:

```bash
source ~/.bashrc
```

Verify that the variable is available:

```bash
echo $GEMINI_API_KEY
```

> Never store API keys directly in `config.py`, Dockerfiles, GitHub workflow files, or source control.

---

### LLM Configuration

LLM response generation is controlled using the `USE_LLM` environment variable.

#### Enable Gemini LLM

```bash
export USE_LLM=true
```

The RAG pipeline can use Gemini to generate the final response.

```text
Question
   ↓
Query Rewrite
   ↓
Retrieval
   ↓
Parent Retrieval
   ↓
Reranking
   ↓
Context Compression
   ↓
Gemini LLM
   ↓
Generated Answer
```

#### Disable Gemini LLM

```bash
export USE_LLM=false
```

This disables Gemini response generation.

This mode is useful for:

- retrieval debugging
- pipeline inspection
- local development
- testing retrieval behavior
- reducing external API usage

The retrieval pipeline can still execute, while LLM generation is disabled.

---

### Debug Mode

Additional debug logging can be enabled using `DEBUG_MODE`.

#### Enable Debug Mode

```bash
export DEBUG_MODE=true
```

Debug mode enables additional system diagnostic logging.

Example:

```text
System statistics | Pages=8 Chunks=24 Vectors=24
```

#### Disable Debug Mode

```bash
export DEBUG_MODE=false
```

Debug mode is disabled by default and is recommended for normal runtime operation.

---

### Logging Configuration

The application uses centralized logging through:

```text
src/logger.py
```

The logging level is controlled using the `LOG_LEVEL` environment variable.

Supported standard Python logging levels include:

| Log Level | Purpose |
|---|---|
| `DEBUG` | Detailed diagnostic information |
| `INFO` | Normal application lifecycle information |
| `WARNING` | Unexpected conditions that do not stop the application |
| `ERROR` | Application operation failures |
| `CRITICAL` | Severe application failures |

The default logging level is:

```text
INFO
```

#### Enable Debug Logging

```bash
export LOG_LEVEL=DEBUG
```

Reload the shell environment if configured in `~/.bashrc`:

```bash
source ~/.bashrc
```

Start the application:

```bash
python main.py
```

Debug messages generated using:

```python
logger.debug(...)
```

will now be visible.

#### Restore Normal Logging

```bash
export LOG_LEVEL=INFO
```

---

### Debug Mode vs Log Level

`DEBUG_MODE` and `LOG_LEVEL` serve different purposes.

| Configuration | Responsibility |
|---|---|
| `DEBUG_MODE` | Controls whether the application generates additional diagnostic information |
| `LOG_LEVEL` | Controls which log messages are displayed and stored |

For complete debug logging, enable both:

```bash
export DEBUG_MODE=true
export LOG_LEVEL=DEBUG
```

The flow is:

```text
DEBUG_MODE=true
      ↓
Application generates debug information
      ↓
logger.debug(...)

LOG_LEVEL=DEBUG
      ↓
Logger accepts DEBUG messages
      ↓
Console + app.log
```

If:

```bash
export DEBUG_MODE=true
export LOG_LEVEL=INFO
```

the application may generate debug log calls, but the logger filters them because the active logging level is `INFO`.

---

### Recommended Runtime Profiles

#### Local Development

```bash
export USE_LLM=true
export DEBUG_MODE=true
export LOG_LEVEL=DEBUG
```

Recommended when developing or inspecting the RAG pipeline.

#### Normal Local Runtime

```bash
export USE_LLM=true
export DEBUG_MODE=false
export LOG_LEVEL=INFO
```

Recommended for normal application usage.

#### Retrieval Debugging

```bash
export USE_LLM=false
export DEBUG_MODE=true
export LOG_LEVEL=DEBUG
```

Recommended when inspecting retrieval, reranking, compression, and pipeline behavior without using the Gemini API.

#### Production Runtime

```bash
export USE_LLM=true
export DEBUG_MODE=false
export LOG_LEVEL=INFO
```

Recommended for Docker and production-style execution.

---

### Docker Runtime Configuration

Runtime configuration can be passed directly to the Docker container.

```bash
docker run \
    --name resume-assistant-api \
    -p 8000:8000 \
    -e GEMINI_API_KEY="$GEMINI_API_KEY" \
    -e USE_LLM=true \
    -e DEBUG_MODE=false \
    -e LOG_LEVEL=INFO \
    <dockerhub-username>/resume-knowledge-assistant:5.0.1
```

Docker Compose can also provide the runtime configuration:

```yaml
environment:
  GEMINI_API_KEY: ${GEMINI_API_KEY}
  USE_LLM: ${USE_LLM:-true}
  DEBUG_MODE: ${DEBUG_MODE:-false}
  LOG_LEVEL: ${LOG_LEVEL:-INFO}
```

This allows the same Docker image to run with different runtime profiles without rebuilding the image.

```text
Docker Image
     │
     ├── Development Configuration
     ├── Debug Configuration
     └── Production Configuration
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

