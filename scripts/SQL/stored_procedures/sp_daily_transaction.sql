/*
===============================================================================
Stored Procedure: sp_DailyTransaction
===============================================================================
Purpose:
    This stored procedure generates a daily aggregated transaction report based 
    on a specified date range. It calculates the total number of transactions and 
    the total transaction amount per day.

    This procedure is typically used for:
        - Daily operational reporting
        - Monitoring transaction activity
        - Analytics dashboards
        - Transaction auditing and reconciliation

Inputs:
    @start_date (DATE)  - Start date of the reporting period
    @end_date   (DATE)  - End date of the reporting period

Output Columns:
    Date                (DATE)   – Transaction date
    TotalTransactions   (INT)    – Number of transactions on that date
    TotalAmount         (MONEY)  – Sum of transaction amounts on that date

Logic Summary:
    - Filters transactions within the date range
    - Groups data by day (daily aggregation)
    - Calculates daily transaction count and total amount
    - Orders results by date ascending

Usage:
    EXEC sp_DailyTransaction 
        @start_date = '2024-01-18', 
        @end_date   = '2024-01-20';

Notes:
    - Using CAST(TransactionDate AS DATE) is easy to read but not index-friendly.
      For large datasets, consider using a range filter without CAST for better performance.
===============================================================================
*/

CREATE PROCEDURE sp_DailyTransaction
    @start_date DATE,
    @end_date DATE
AS
BEGIN
    SET NOCOUNT ON;

    /*
        ===============================================================================
        Main Query:
            Retrieves daily aggregated transaction counts and total amounts.
        ===============================================================================
    */
    SELECT 
        CAST(TransactionDate AS DATE) AS Date,
        COUNT(TransactionID) AS TotalTransactions,
        SUM(Amount) AS TotalAmount
    FROM dbo.FactTransaction
    WHERE CAST(TransactionDate AS DATE) BETWEEN @start_date AND @end_date
    GROUP BY CAST(TransactionDate AS DATE)
    ORDER BY CAST(TransactionDate AS DATE);
END;
GO

/*
===============================================================================
Example Execution
===============================================================================
*/

EXEC sp_DailyTransaction 
    @start_date = '2024-01-18',
    @end_date   = '2024-01-20';
GO
