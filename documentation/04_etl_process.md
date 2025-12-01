## Extract
Using Python:
- `pd.read_csv()`
- `pd.read_excel()`
- `pd.read_sql()`

## Transform
Operations performed:
- Convert dates to `datetime`
- Standardize column names
- Merge 3 transaction sources
- Deduplicate based on `transaction_id`
- Rename for DWH naming consistency
- Clean dimensions (uppercase strings)

## Load
Using `pyodbc.executemany()` with fast_executemany enabled.

Load order (to respect FK constraints):
1. DimBranch
2. DimCustomer
3. DimAccount
4. FactTransaction

---
