# 01_project_overview.md

## 1. Project Overview
This project implements an **End-to-End Data Engineering pipeline** using:
- **Python** (pandas, pyodbc)
- **Microsoft SQL Server**
- **SQL Server Management Studio (SSMS)**

The goal is to build a clean **Data Warehouse (DWH)** from multiple raw data sources:
- CSV transactions file
- Excel transactions file
- SQL database (`sample`)

The final result is a fully functional DWH containing:
- **DimCustomer**
- **DimAccount**
- **DimBranch**
- **FactTransaction**

All data transformations are performed in Python, and loaded into SQL Server via pyodbc.

---
