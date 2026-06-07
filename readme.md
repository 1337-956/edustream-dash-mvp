# EduStream Academic Infrastructure Analytics Platform (MVP)

An end-to-end data engineering and business intelligence application that extracts unstructured academic infrastructure records via public JSON REST endpoints, applies vectorized transformations, and structures clean visual analytics profiles for executive reporting.

## 1. Project Architecture & Execution Guide

### System Dependencies
Ensure the following libraries are installed in your active Python development environment:
* `dash` & `dash-bootstrap-components` (Visualization UI Framework)
* `pandas` (Vectorized Data Transformation Matrix)
* `requests` (API REST Endpoint Data Ingestion)
* `psycopg2-binary` & `sqlalchemy` (PostgreSQL Dialect Database Connectivity)

### Operational Launch Steps
1. Execute the dashboard application script directly from your terminal:
   ```bash
   python app.py
   ```   