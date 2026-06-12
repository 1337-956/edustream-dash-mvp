# EduStream Academic Infrastructure Analytics Platform (MVP)

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/)
[![Framework: Dash](https://img.shields.io/badge/framework-Dash%20%7C%20Plotly-orange)](https://dash.plotly.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 1. Business Problem & Project Overview
Siloed academic infrastructure datasets and brittle database connections often leave education leadership with delayed views when evaluating national institutional footprints. This repository hosts the **EduStream Analytics Platform MVP**, an end-to-end data engineering solution that extracts unstructured academic infrastructure records via public JSON REST endpoints, applies vectorized transformations, and structures clean visual analytics profiles for executive reporting. 

To ensure high availability for executive decision-makers, the core application features a hybrid data architecture that seamlessly bridges active relational database environments with localized flat-file failovers.

---

## 2. System Architecture & Data Journey
The infrastructure prioritizes fault tolerance, separating data access logic from the presentation layout to achieve zero-crash executive reporting.

```text
       ┌────────────────────────┐
       │ PostgreSQL DB (Fact)   │
       └───────────┬────────────┘
                   │ (Primary Query Connection)
                   ▼
  [Data Ingestion Layer: db_setup.py] ───(Failover)───> [Local Data Cache: cleaned_universities.csv]
                   │
                   ▼
   [Analytical Core: pandas matrix]
                   │
                   ▼
 [Presentation UI: dash_app/app.py (SLATE Theme)] ───> Interactive Bars & Donut Visuals
