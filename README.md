AdFlow Sentinel (formerly AdFlow AI)
An Agentic, Production-Ready Marketing Analytics Platform

Project Overview
AdFlow Sentinel is an autonomous marketing intelligence platform designed to monitor, audit, and analyze campaign traffic in real-time. By leveraging Agentic AI (Gemini) and a Strategy-Pattern based data architecture, the system provides strategic insights while actively monitoring for fraudulent bot activity.

Architecture Highlights
This project was engineered to be production-ready, maintainable, and scalable. Key architectural decisions include:

Modular Data Provider (Strategy Pattern): Decoupled data ingestion from analysis. The system supports plug-and-play data sources (SQL, Web Scraping, APIs) via environment-based configuration without altering core agent logic.

Agentic Intelligence (RAG): Utilizes Gemini-powered agents to reason over live data and cross-reference with internal brand policies stored in a ChromaDB vector store.

Observability & Compliance: Integrated custom Audit Logging system to track every agent decision and data fetch—essential for enterprise AI compliance.

Cloud-Native Deployment: Deployed via Streamlit Cloud with a persistent Neon PostgreSQL backend, ensuring a production-grade environment accessible globally.

Tech Stack
Intelligence: Google Gemini API, LangChain (RAG)

Backend/API: Streamlit, Python

Database: PostgreSQL (Neon Cloud), ChromaDB

Observability: Custom Audit Logger

Deployment: Streamlit Cloud

Core Features
Strategic Health Monitoring: Real-time gauge visualization of bot-traffic percentages.

Context-Aware Analysis: The AI "reasons" about campaign health by consulting both live SQL data and static policy documentation.

Dynamic Ingestion: Easily switch between real-time database monitoring and web-based data scraping.

Setup Instructions
Clone the Repository: git clone [your-repo-link]

Install Dependencies: pip install -r requirements.txt

Environment Setup: Configure the following in your deployment environment:

DATABASE_URL: Your Neon connection string.

GEMINI_API_KEY: Your Google GenAI API key.

DATA_SOURCE: Set to "sql" or "web" to toggle data ingestion.
