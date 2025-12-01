# 06_data_quality.md

## Data Quality Framework
The project implements the following checks:

### 1. Completeness
- No missing TransactionID, AccountID
- No null foreign keys in fact

### 2. Consistency
- Date formats normalized
- String columns uppercased

### 3. Uniqueness
- Deduplicate transactions
- Ensure primary key uniqueness

### 4. Referential Integrity
- Every FactTransaction.AccountID must exist in DimAccount
- Every DimAccount.CustomerID must exist in DimCustomer

---
