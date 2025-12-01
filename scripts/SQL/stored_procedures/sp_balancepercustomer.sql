/*
===============================================================================
Stored Procedure: sp_BalancePerCustomer
===============================================================================
Purpose:
    This stored procedure calculates the current balance for a given customer 
    by combining initial account balance with aggregated transactions 
    (deposits and withdrawals).

    It is useful for:
        - Customer account inquiry
        - Financial dashboards
        - Balance reconciliation
        - Transaction impact analysis

Inputs:
    @customer_name (VARCHAR 100)  
        - Partial or full name of the customer.
        - Supports wildcard searches (via LIKE).

Output Columns:
    CustomerName      (VARCHAR)  – Customer's full name
    AccountType       (VARCHAR)  – Type of account (e.g., Savings, Checking)
    InitialBalance    (INT)– Opening balance stored in DimAccount
    CurrentBalance    (INT)– Initial balance + net transaction effect

Logic Summary:
    - A CTE (TransactionSummary) aggregates transactions per AccountID:
        * Deposits increase balance
        * Withdrawals decrease balance
    - Joins customer → account → transaction summary
    - Filters active accounts only
    - Allows partial name matching for flexible searching

Business Rules:
    - Only accounts with Status = 'active' are included.
    - If an account has no transactions, TotalTransactionAmount defaults to 0.
    - TransactionType = 'Deposit' increases the balance; others decrease it.

Usage Example:
    EXEC sp_BalancePerCustomer @customer_name = 'Shelly';

Notes:
    - If multiple customers contain matching names (e.g., “She”), all are returned.
    - For better performance, ensure indexes exist on:
        * DimCustomer.CustomerName
        * DimAccount.CustomerID
        * FactTransaction.AccountID
===============================================================================
*/

CREATE PROCEDURE sp_BalancePerCustomer
    @customer_name VARCHAR(100)
AS
BEGIN
    SET NOCOUNT ON;

    /*
        ===============================================================================
        CTE: TransactionSummary
        Aggregates net transaction amount per account.
        Deposit  → Amount added
        Others   → Amount subtracted
        ===============================================================================
    */
    WITH TransactionSummary AS (
        SELECT
            AccountID,
            SUM(
                CASE 
                    WHEN TransactionType = 'Deposit' THEN Amount
                    ELSE -Amount
                END
            ) AS TotalTransactionAmount
        FROM dbo.FactTransaction
        GROUP BY AccountID
    )

    /*
        ===============================================================================
        Final Query:
        Returns customer name, account type, initial balance, and computed current balance.
        ===============================================================================
    */
    SELECT 
        c.CustomerName,
        a.AccountType,
        a.Balance AS InitialBalance,
        a.Balance + ISNULL(ts.TotalTransactionAmount, 0) AS CurrentBalance
    FROM DimCustomer c
    LEFT JOIN DimAccount a 
        ON c.CustomerID = a.CustomerID
    LEFT JOIN TransactionSummary ts 
        ON a.AccountID = ts.AccountID
    WHERE 
        c.CustomerName LIKE '%' + @customer_name + '%'
        AND a.Status = 'active';
END;
GO

/*
===============================================================================
Example Execution
===============================================================================
*/

EXEC sp_BalancePerCustomer @customer_name = 'Shelly';
GO
