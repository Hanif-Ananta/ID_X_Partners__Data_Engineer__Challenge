# 05_database_design.md

## Star Schema
Fact table: **FactTransaction**
Dimensions:
- DimCustomer
- DimAccount
- DimBranch

## DDL Summary
### DimBranch
```
BranchID PK
BranchName
BranchLocation
```

### DimCustomer
```
CustomerID PK
CustomerName
Address
CityName
StateName
Age
Gender
Email
```

### DimAccount
```
AccountID PK
CustomerID FK → DimCustomer
AccountType
Balance
DateOpened
Status
```

### FactTransaction
```
TransactionID PK
AccountID FK → DimAccount
BranchID FK → DimBranch
TransactionDate
Amount
TransactionType
```

---
