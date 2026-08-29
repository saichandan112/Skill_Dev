# AI Learning Journey — Complete Study Material

This document expands the repository structure in `AI GitHub Repository Structure.md` into complete, actionable learning material you can follow and store in your repository.

---

## How to use this material
- Follow modules in order (01 → 09) unless you already know prerequisites.
- Each module contains: Overview, Prerequisites, Key Topics, Hands-on Exercises, Mini Project, Suggested Resources, and Estimated Time.
- Keep progress in `LEARNING_LOG.md` and add completed exercises to `Projects/` folders.

---

## Intro: Setup & Essentials

Objectives
- Set up a reproducible dev environment
- Learn Git/GitHub and repository organization

Prerequisites
- Basic computer literacy

Steps
1. Install Python (3.10+) or use Conda.
2. Create a project virtual environment per project:

```bash
python -m venv .venv
.venv\Scripts\activate  # windows
pip install --upgrade pip
```

3. Install common packages for early modules:

```bash
pip install numpy pandas scikit-learn matplotlib jupyterlab
```

4. Git quickstart
- `git init` / `git clone` / `git branch` / `git commit` / `git push` (link to GitHub remote)

Resources
- Pro Git book (online)
- GitHub Learning Lab

---

## 01-Python — Foundations

Overview: Core Python language, idiomatic code, data structures, OOP, modules, testing.

Prerequisites: None

Key Topics
- Syntax, variables, types
- Control flow, functions, modules
- Lists, dicts, sets, tuples
- List/dict comprehensions, generators
- OOP: classes, inheritance, dunder methods
- File I/O and JSON
- Virtual environments and packaging
- Unit testing with `pytest`

Hands-on Exercises
- Implement utilities: CSV parser, small CLI tool
- Practice with coding katas (e.g., Advent of Code problems)

Mini Project
- Employee Management App (CRUD with JSON storage)

Resources
- "Automate the Boring Stuff with Python" (Al Sweigart)
- Real Python tutorials

Estimated time: 2–4 weeks

---

## 02-Data-Analysis

Overview: Data cleaning, manipulation, visualization

Key Topics
- NumPy arrays and performance
- Pandas DataFrame ops: ingestion, cleaning, grouping, joins
- Exploratory Data Analysis (EDA): visualization with Matplotlib / Seaborn
- Basic statistics and aggregation

Exercises
- Clean a messy CSV and produce a short analysis report
- Implement pivot-table style aggregations

Mini Project
- Python Data Analyzer: build scripts that ingest CSVs, produce plots and a short report

Resources
- DataCamp / Kaggle micro-courses
- "Python for Data Analysis" (Wes McKinney)

Estimated time: 2–3 weeks

---

## 03-Machine-Learning

Overview: Fundamentals of supervised and unsupervised ML

Key Topics
- Regression: linear, regularization (Ridge/Lasso)
- Classification: logistic regression, decision trees, random forests
- Model evaluation: cross-validation, confusion matrix, ROC-AUC
- Feature engineering and pipelines

Exercises
- Build a churn predictor with scikit-learn
- Hyperparameter tuning with GridSearchCV

Mini Project
- Customer Churn Prediction: dataset ingestion, preprocessing, model, evaluation report

Resources
- Andrew Ng (Coursera) — ML course
- scikit-learn documentation

Estimated time: 3–5 weeks

---

## 04-Deep-Learning

Overview: Neural networks, PyTorch/TensorFlow basics

Key Topics
- Neural network fundamentals
- Layers, activations, loss functions
- Training loop, optimization, regularization
- CNNs for images, RNNs/transformers for sequences
- Model serialization and serving basics

Exercises
- Implement a simple feedforward network in PyTorch
- Train a small CNN on a subset of CIFAR-10

Mini Project
- Digit recognizer or image classifier with training + evaluation + README

Resources
- Deep Learning Specialization (Coursera)
- PyTorch tutorials

Estimated time: 4–6 weeks

---

## 05-Generative-AI

Overview: Prompt engineering, LLMs, frameworks, and cloud provider integrations

Key Topics
- LLM fundamentals: tokenization, context window, temperature
- Prompt engineering patterns and safety
- LangChain fundamentals: chains, agents, memory
- Azure OpenAI and OpenAI API usage
- Semantic search basics

Exercises
- Build prompt templates and evaluate output variability
- Connect to OpenAI/Azure OpenAI with a simple prompt-response app

Mini Project
- PDF Question Answering Bot (ingest PDF, embed, query LLM)

Resources
- OpenAI API docs
- LangChain docs and examples

Estimated time: 3–6 weeks

---

## 06-RAG (Retrieval-Augmented Generation)

Overview: Creating knowledge-grounded LLM applications with vector stores

Key Topics
- Embeddings and vector similarity
- Vector stores: FAISS, ChromaDB, Pinecone
- Chunking and indexing documents
- Hybrid search (BM25 + dense)

Exercises
- Index a directory of documents and run similarity queries

Mini Project
- Enterprise RAG System: ingest company docs, build QA interface, logging

Resources
- FAISS docs, Pinecone quickstart, Chroma docs

Estimated time: 2–4 weeks

---

## 07-AI-Agents

Overview: Multi-step agents that call tools and perform workflows

Key Topics
- Agent patterns (tool-using agents, chat-based agents)
- LangGraph, AutoGen, CrewAI concepts
- Safety and orchestration

Exercises
- Create a simple agent that chains web search + summarization

Mini Project
- AI-Agent: scheduler assistant that integrates calendar and summarization

Estimated time: 3–5 weeks

---

## 08-Deployment

Overview: Putting models and services into production

Key Topics
- FastAPI for model-serving endpoints
- Containerization with Docker
- CI/CD basics and GitHub Actions
- Deployment on Azure (App Service, AKS) or other cloud

Exercises
- Wrap a trained model behind a FastAPI endpoint and containerize it

Mini Project
- Dockerized model server + GitHub Action to build and push image

Resources
- FastAPI docs
- Docker docs

Estimated time: 2–4 weeks

---

## 09-SAP-AI

Overview: Integrating AI with SAP platforms (SAP BTP, AI Core)

Key Topics
- SAP Business Technology Platform basics
- AI Core / AI Foundation concepts
- Integrating RAG and assistants into SAP workflows

Exercises
- High-level design: connect a RAG system to SAP service layer

Mini Project
- SAP Knowledge Assistant: create a demo for searching SAP docs

Estimated time: 3–6 weeks (SAP-specific onboarding may be needed)

---

## Portfolio Projects (Guides & Deliverables)
For each portfolio project include:
- Objective and user story
- Dataset or input shape
- High-level design and architecture diagram
- Implementation steps and checkpoints
- Tests and evaluation metrics
- Deployment instructions

Example projects (with recommended outcomes)
- PDF-Chatbot: ingest PDFs, build embeddings, serve via a chat UI
- Invoice-Processor: extract fields with OCR + structured output
- Enterprise-RAG: scalable vector store + secure access patterns

---

## Resources & Books
- "Python for Data Analysis" — Wes McKinney
- "Hands-On Machine Learning" — Aurélien Géron
- OpenAI / LangChain docs
- FAISS & Pinecone docs

---

## Assessment & Portfolio Tips
- Keep small, polished projects with clear READMEs and reproducible instructions.
- Add unit tests where applicable and a short demo video for portfolio projects.
- Tag projects with labels in GitHub and use GitHub Pages to host demos.

---

## Appendix: Templates
- README template: purpose, setup, how to run, demo link.
- ROADMAP.md sample (put milestones and dates in it).
- LEARNING_LOG.md sample entry format.

---

_End of material — add this file to your `AI-Learning-Journey` repository under `AI_Learning/`._