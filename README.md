# EduStream: Academic Infrastructure Ingestion Layer & Analytics Portal
### MSBA-692: Pipelines to Insights — Summer 2026 Capstone Project

---

## 📋 Executive Project Overview
EduStream is an enterprise-grade data engineering pipeline and interactive analytics portal designed to ingest, process, and visualize nationwide verified academic institutional datasets. Built with a focus on structural robustness and data availability, the system features a custom hybrid storage registration layer. This ensures that executive dashboard operations remain online and fully functional even during sudden upstream database cluster connection failures.

### Key Architectural Pillars
* **Fault-Tolerant Ingestion:** Features an automated graceful failover loop that detects primary PostgreSQL cluster status and automatically routes processing to a local CSV/API scrape cache layer.
* **Relational Warehousing:** Engineered with robust mapping patterns utilizing SQLAlchemy to interface with structured data models.
* **Parallel Callbacks & Reactive UI:** Powered by Plotly Dash and custom CSS themes to allow executive stakeholders to dynamically filter localized institutional density metrics instantly.

---

## 📁 Repository Directory Structure
This repository follows standard production layout paradigms to separate data processing, storage, visualization, and project documentation:

```text
├── dash_app/
│   └── app.py                     # Main interactive Plotly Dash analytical application
├── data/
│   ├── cleaned_universities.csv   # Local storage fallback warehouse layer (API Cache)
│   └── edustream_db.db            # SQLite local edge database configuration 
├── docs/
│   └── Wk1_DMorales.pdf           # Project proposal and historical milestones
├── etl/
│   ├── db_setup.py                # Database schema creation and table initialization
│   ├── etl_pipeline.py            # Extraction, transformation, and validation scripts
│   └── run_pipeline.py            # Master execution sequence runner
├── requirements.txt               # Pinpointed project dependencies and frameworks
└── README.md                      # Comprehensive deployment documentation
