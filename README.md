# ID_X_Partners__Data_Engineer__Challenge
# End-to-End Data Engineering Pipeline (Python + SQL Server)

This project demonstrates a complete **ETL Data Engineering pipeline** using Python (pandas + pyodbc) and SQL Server. The pipeline loads raw data from CSV, Excel, and SQL databases into a clean **Data Warehouse (DWH)** following a proper star schema.

## 🚀 Tech Stack
- Python (pandas, pyodbc)
- SQL Server
- SSMS
- CSV + Excel + SQL data sources

## 📂 Repository Structure
```
/
├── documentation/
├── scripts/
├── data/
└── README.md
```

## 📦 Features
- Multi-source ingestion (CSV, Excel, SQL)
- Data cleaning & standardization
- Star schema DWH creation
- ETL pipeline with loading order handling FKs
- Data quality validation

## 📘 Documentation
Full documentation available in `/documentation` folder.

## ▶️ How to Run ETL
- Restore the sample database from `/data` folder first.
- Then run the python script: 
```
python scripts/python/etl_pipeline.py
```

## 📊 Result
DWH containing:
- DimBranch
- DimCustomer
- DimAccount
- FactTransaction

Ready for analytics and dashboarding.

---
