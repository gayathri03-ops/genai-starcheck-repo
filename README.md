# GenAI StarCheck

A Generative AI project for answering user questions using information from a collection of documents.

## Problem

Finding accurate information across multiple documents can be time-consuming. Users may need to read several pages to locate relevant information and understand how different sections relate to one another. GenAI StarCheck aims to simplify this process by allowing users to ask questions in natural language. The application is designed to provide useful answers based on the available documents, with document references and page citations as part of the planned functionality.

## Who it is for

- **Students and researchers** who need to find answers across lengthy documents.
- **Professionals and knowledge workers** who want to retrieve information from document collections without manually searching every page.

## Signature feature

**Document-based question answering**

The goal is to let users ask questions in natural language and receive answers grounded in the supplied documents.

Planned capabilities include:
- Retrieving relevant information from documents.
- Answering questions that require information from multiple pages.
- Providing document and page references to help users verify answers.
- Handling questions that cannot be answered from the available documents.

## Hardest problem (my interview story)

One of the main technical challenges in this project is building a reliable question-answering system that can retrieve relevant information from lengthy documents and generate answers grounded in the source material.

The challenge is to preserve page numbers and headings during document processing, retrieve the right information for a question, and avoid generating unsupported answers.

**My implementation and solution:** Add the specific problem you encountered, how you debugged it, and the result you achieved as development progresses.

## Dataset

The dataset should contain relevant documents for the project's intended domain. Record the source, original URL, number of documents, total pages, and licence or usage terms for every source.

| Source | Link | Documents | Pages | Licence / terms |
|---|---|---:|---:|---|
| To be added | Original source URL | To be counted | To be counted | To be verified |

See [`DATASET.md`](DATASET.md) for dataset details.

## 10 real questions

1.Basic lookup: What is the main purpose of this document?

2.Specific detail: What are the key requirements mentioned in the document?

3.Date and deadline: What important dates, deadlines, or timelines are specified?

4.Definition: How does the document define its main concepts or terminology?

5.Process: What steps must be followed to complete the process described in the document?

6.Comparison: What are the main differences between the two methods, options, or approaches described in the documents?

7.Multi-page reasoning: What information from different sections is needed to understand the overall purpose of the document?

8.Cross-document reasoning: What common points and differences can be identified across the available documents?

9.Evidence-based answer: What evidence in the documents supports the main conclusion or recommendation?

10.Unanswerable question: What information is requested that cannot be found in the available documents? The system should clearly state that the information is unavailable instead of inventing an answer.
## Tech stack

- **Language:** Python
- **API framework:** FastAPI
- **Development server:** Uvicorn
- **AI/LLM integration:** To be specified based on the implemented model
- **Document processing and retrieval:** To be specified based on the implemented components

## Run it locally

### 1. Prerequisites

Install Python 3.12 and Git. Verify the installation:

```powershell
python --version
python -m pip --version
```

### 2. Clone the repository

```powershell
git clone https://github.com/gayathri03-ops/genai-starcheck-repo.git
cd genai-starcheck-repo
```

### 3. Create a virtual environment

**Windows PowerShell:**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, you can use the environment's Python executable directly instead.

### 4. Install dependencies

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements-dev.txt
```

### 5. Configure environment variables

```powershell
Copy-Item .env.example .env
```

Open `.env` and configure the required variables according to the project's implementation. Keep API keys and other secrets private.

### 6. Start the API server

```powershell
python -m uvicorn app.main:app --reload
```

The API should start at:

`http://127.0.0.1:8000`

### 7. Check the health endpoint

Open another PowerShell terminal and run:

```powershell
Invoke-RestMethod http://127.0.0.1:8000/health
```

You can also open the interactive API documentation at:

`http://127.0.0.1:8000/docs`

## Project structure

```text
genai-starcheck-repo/
├── app/                 # Application and API code
├── data/
│   └── sample/          # Sample documents
├── docs/
│   └── QUESTIONS.md    # Evaluation questions
├── tests/               # Automated tests
├── .env.example         # Environment configuration template
├── DATASET.md           # Dataset sources and terms
├── PROGRESS.md          # Development progress
├── requirements.txt     # Runtime dependencies
├── requirements-dev.txt # Development dependencies
└── README.md
```


## Future improvements

- Improve document retrieval and answer relevance.
- Support questions that require multiple documents or pages.
- Provide verifiable citations for generated answers.
- Evaluate answer quality using the ten real-user questions.
- Improve error handling, response times, and deployment reliability.

## Author

**Gayathri R.**

GitHub: [@gayathri03-ops](https://github.com/gayathri03-ops)
