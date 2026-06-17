# Employee Intelligence Platform

A Multi-Agent Employee Analytics System built using LangGraph, Streamlit, SQLAlchemy, and OpenAI.

## Overview

The Employee Intelligence Platform is an AI-powered employee analytics assistant that allows users to query employee information, organizational structures, department analytics, promotion readiness, reporting hierarchies, and generate Excel reports while enforcing Role-Based Access Control (RBAC).

The system uses a multi-agent architecture where specialized agents collaborate to retrieve, analyze, authorize, and export organizational data.

---

## Features

### Multi-Agent Architecture

* Controller Agent
* Authorization Agent
* Employee Lookup Agent
* Team Lookup Agent
* Department Analytics Agent
* Analysis Agent
* Excel Export Agent

### Role-Based Access Control (RBAC)

Different users have different visibility levels:

| Role                | Access                   |
| ------------------- | ------------------------ |
| CEO                 | Full organization access |
| Department Director | Department-wide access   |
| Manager             | Direct team access       |
| Employee            | Personal profile access  |

### Employee Analytics

* Employee profile lookup
* Salary analysis
* Manager lookup
* Reporting hierarchy
* Team structure visualization
* Promotion readiness evaluation

### Department Analytics

* Department statistics
* Average salary analysis
* Employee count
* Performance metrics
* Department hierarchy

### Organization Analytics

* Company hierarchy
* Department heads
* Organization-wide statistics
* Top paid employees
* Largest department
* Performance insights

### Excel Report Generation

Export:

* Employee Reports
* Department Reports
* Team Reports
* Promotion Reports
* Company Reports

---

## Tech Stack

### Frontend

* Streamlit

### Backend

* Python
* LangGraph
* LangChain

### Database

* SQLite
* SQLAlchemy

### AI

* OpenAI GPT Models

### Data Processing

* Pandas
* OpenPyXL

---

## Project Structure

employee-intelligence-platform/

├── agents/

├── config/

├── database/

├── employee_api/

├── frontend/

├── graph/

├── logs/

├── prompts/

├── schemas/

├── tests/

├── tools/

├── utils/

├── streamlit_app.py

├── employees.db

├── requirements.txt

└── README.md

---

## System Workflow

1. User submits query
2. Controller Agent extracts intent and entities
3. Authorization Agent validates permissions
4. Data agents retrieve relevant information
5. Analysis Agent generates response
6. Excel Export Agent generates reports when requested
7. Streamlit UI displays results and agent trace

---

## Example Queries

### Employee Queries

* Tell me about Sarah Smith
* Who manages Ryan Cooper?
* Compare Sarah Smith's salary with department average

### Team Queries

* Who reports to Mark Tech?
* Show my team hierarchy
* Give me a performance summary of my team

### Department Queries

* Show HR department statistics
* List all employees in IT
* Generate promotion report for Sales

### Organization Queries

* Show company hierarchy
* Who are the department heads?
* Export complete company report

---

## Running the Application

Install dependencies:

```bash
pip install -r requirements.txt
```

Seed database:

```bash
python seed_data.py
```

Run Streamlit:

```bash
streamlit run streamlit_app.py
```

---

## Future Enhancements

* Agent tracing dashboard
* PDF report generation
* Real-time database integration
* Advanced workforce analytics
* Performance prediction models
* Cloud deployment

---

## License

MIT License
