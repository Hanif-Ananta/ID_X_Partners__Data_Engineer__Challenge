# 09_how_to_run.md

## Requirements
- Python 3.9+
- SQL Server
- ODBC Driver 17
- Requirements: pandas, pyodbc

## Steps
1. Clone repo
2. Place raw files inside `/data` folder
3. Configure SQL Server connection inside `etl_pipeline.py`
4. Run script:
```
scripts/python/etl_pipeline.py
```
5. Check tables in SSMS

---
