# 02_architecture_design.md

## 1. High-Level Architecture
```
Data Sources → Python ETL → SQL DWH
```

### Components:
- **Extract:** Load CSV, Excel, SQL table
- **Transform:** Merge, deduplicate, cleanse data using pandas
- **Load:** Insert cleaned data into SQL Server DWH

## 2. ETL Flow Diagram
```
             +------------------+
             | transaction_csv  |
             +------------------+
                      |
                      v
             +------------------+
             | transaction_xlsx |
             +------------------+
                      |
                      v
             +------------------+
             |    sample_db     |
             +------------------+
                      |
                      v
        +---------------------------------+
        |  Python ETL (merge, clean, etc) |
        +---------------------------------+
                      |
                      v
        +-------------------------------+
        | SQL Server Data Warehouse     |
        | Dim + Fact tables             |
        +-------------------------------+
```

---
