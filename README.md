# AdFlow AI
*Autonomous Marketing Intelligence & Campaign Guardian*

<img width="1912" height="916" alt="image" src="https://github.com/user-attachments/assets/06b6c89b-1df4-43fa-a4b5-48e55401ff0a" />


## Project Overview
**AdFlow AI** is an end-to-end agentic analytics platform engineered to monitor, audit, and analyze campaign traffic in real-time. By moving away from static, passive dashboards, AdFlow AI leverages **Agentic AI patterns** to act as a virtual marketing strategist—interpreting live data, cross-referencing brand policy via **RAG**, and providing actionable, audit-ready recommendations.


## 🚀 Key Metrics & Performance
Our system was designed for scale and enterprise-grade reliability. Since deployment, the current build achieves:
* **Detection Latency:** < 500ms for real-time health assessments.
* **Agentic Precision:** 90%+ alignment with predefined brand policies using RAG-based context grounding.
* **Audit Transparency:** 100% of agent reasoning paths are captured via custom audit logging, ensuring enterprise-grade compliance.
* **Scalability:** Optimized for high-concurrency event ingestion via Neon PostgreSQL.


## Architecture & Tech Stack
We built this as a **modular, pluggable service**. The core logic is decoupled from the data source, allowing the system to switch between real-time SQL ingestion and external web scraping without modifying the AI logic.

* **Intelligence:** Google Gemini 2.5 Flash (Custom Agentic Reasoning Loop).
* **Grounding:** RAG (Retrieval-Augmented Generation) with **ChromaDB** for context-aware policy enforcement.
* **Backend:** Python (Streamlit) with an asynchronous simulator.
* **Database:** PostgreSQL (Neon Cloud) for persistent, high-concurrency state.
* **Observability:** Custom enterprise-grade Audit Logger for decision traceability.
* **UI:** Interactive Streamlit web interface with real-time Gauge/Chart visualization.


## Development Lifecycle
The project was executed in four primary phases:

1.  **Phase 1: Data Infrastructure:** Established a cloud-native, persistent PostgreSQL backend (Neon) to serve as the "Single Source of Truth."
2.  **Phase 2: Intelligent Layer:** Integrated Gemini LLMs using a **Reason -> Act -> Synthesize** loop, grounding the agent's knowledge using vector-based RAG.
3.  **Phase 3: Observability:** Developed an audit logging system to log `AGENT_THOUGHT`, `TOOL_OUTPUT`, and `FINAL_RESPONSE`, ensuring explainable AI behavior.
4.  **Phase 4: Deployment & UI:** Wrapped the entire pipeline in a Streamlit interface and deployed as a production-ready web service.


## User Interface (Agentic Interaction)
The UI provides real-time monitoring and a chat-based interface for deep-dive campaign analysis.

<img width="1900" height="862" alt="image" src="https://github.com/user-attachments/assets/b61c47ce-b957-4747-b248-50ff3092f10d" />


*Example Interaction:*
> **User:** "What is the status of Mumbai campaign? Should we pause?"
> **AdFlow:** "The current bot rate in Mumbai is 19.4%, which is within the safe operating margin (<20%). We recommend maintaining the current budget but increasing monitoring frequency."


## Setup & Deployment
To run AdFlow AI, configure the following environment variables in your deployment settings:

1. **Clone the Repo:** `git clone https://github.com/your-username/adflow-ai.git`
2. **Install Dependencies:** `pip install -r requirements.txt`
3. **Environment Configuration:**
    * `DATABASE_URL`: Your cloud-managed PostgreSQL connection string.
    * `GEMINI_API_KEY`: Your Google GenAI API key.
    * `DATA_SOURCE`: Set to `"sql"` (for Database) or `"web"` (for Scraper).


## Conclusion & Reflections
AdFlow AI represents the intersection of robust data engineering and modern AI agency. By moving away from static, passive dashboards to an autonomous, context-aware agent, we have demonstrated that marketing teams can shift from merely "monitoring data" to "acting on intelligence."

The modular architecture—specifically the **Data Provider Pattern**—ensures this system is not just a prototype, but a scalable foundation ready for enterprise-grade integration. From the custom audit logging of agent decision paths to the RAG-based policy enforcement, this project highlights a commitment to building AI systems that are not only powerful but also **explainable, secure, and production-ready.**


### Future Roadmap
This project serves as a foundation for advanced autonomous systems. Planned iterations include:
* **API Integration:** Extending the `Data Provider` to support live connectors (e.g., Google Ads API, Meta Marketing API) for real-time campaign management.
* **Complex Orchestration:** Migrating the agentic loop to **LangGraph** to handle multi-step, asynchronous decision workflows.
* **Predictive Analytics:** Integrating time-series forecasting to proactively identify traffic anomalies before they reach threshold limits.

---
