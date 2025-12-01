## Validation Queries
### 1. Row Count Check
```
SELECT COUNT(*) FROM FactTransaction;
```

### 2. FK Check
```
SELECT *
FROM FactTransaction f
LEFT JOIN DimAccount a ON f.AccountID = a.AccountID
WHERE a.AccountID IS NULL;
```

### 3. Duplicate PK Check
```
SELECT TransactionID, COUNT(*)
FROM FactTransaction
GROUP BY TransactionID
HAVING COUNT(*) > 1;
```

## Testing Per Dataset
- Validate joins
- Validate date formats
- Validate numeric columns

---
