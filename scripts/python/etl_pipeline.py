import pandas as pd
import pyodbc

# ===========================
#  LOAD FROM CSV + EXCEL AND CONVERT DATES ON CSV
# ===========================
transactions_csv = pd.read_csv("../../data/transaction_csv.csv")
transactions_csv["transaction_date"] = pd.to_datetime(transactions_csv["transaction_date"])
transactions_excel = pd.read_excel("../../data/transaction_excel.xlsx")

# ===========================
#  CONNECTION TO SAMPLE DB
# ===========================
connection_string = """
                    DRIVER={ODBC Driver 17 for SQL Server};
                    SERVER=Mirekell;
                    DATABASE=sample;
                    Trusted_Connection=yes;
                    """
conn_sample = pyodbc.connect(connection_string)

# ---- LOAD TRANSACTION FROM SOURCE TABLE ----
query = "SELECT * FROM sample.dbo.transaction_db"
transaction_db = pd.read_sql(query, conn_sample)

# Combine all transactions (CSV + Excel + DB)
transactions_all = pd.concat([transactions_csv, transactions_excel, transaction_db], ignore_index=True)

# Sorting + renaming for DWH fact table
fact_transactions = (
    transactions_all
    .drop_duplicates()
    .sort_values('transaction_id')
    .reset_index(drop=True)
    .rename(columns={
        'transaction_id': 'TransactionID',
        'account_id': 'AccountID',
        'transaction_date': 'TransactionDate',
        'amount': 'Amount',
        'transaction_type': 'TransactionType',
        'branch_id': 'BranchID'
    })
)

# ===========================
#  DIM CUSTOMER
# ===========================
sql_query = """
            SELECT
                cu.customer_id AS CustomerID,
                UPPER(cu.customer_name) AS CustomerName,
                UPPER(cu.address) AS Address,
                UPPER(ci.city_name) AS CityName,
                UPPER(st.state_name) AS StateName,
                cu.age AS Age,
                UPPER(cu.gender) AS Gender,
                cu.email AS Email
            FROM dbo.customer cu
            LEFT JOIN dbo.city ci ON cu.city_id = ci.city_id
            LEFT JOIN dbo.state st ON ci.state_id = st.state_id
            """
dim_customer = pd.read_sql(sql_query, conn_sample)

# ===========================
#  DIM ACCOUNT
# ===========================
query = """
        SELECT
            account_id AS AccountID,
            customer_id AS CustomerID,
            account_type AS AccountType,
            balance AS Balance,
            date_opened AS DateOpened,
            status AS Status 
        FROM sample.dbo.account
        """
dim_account = pd.read_sql(query, conn_sample)

# ===========================
#  DIM BRANCH
# ===========================
query = """
        SELECT
            branch_id AS BranchID,
            branch_name AS BranchName,
            branch_location AS BranchLocation 
        FROM sample.dbo.branch
        """
dim_branch = pd.read_sql(query, conn_sample)

# ===========================
#  CONNECT TO DWH
# ===========================
conn_string_DWH = """
                  DRIVER={ODBC Driver 17 for SQL Server};
                  SERVER=Mirekell;
                  DATABASE=DWH;
                  Trusted_Connection=yes;
                  """
conn_DWH = pyodbc.connect(conn_string_DWH)
cursor_DWH = conn_DWH.cursor()

# ===========================
#  DROP & CREATE TABLES
# ===========================
DWH_ddl_query = """
                -- DROP TABLES IN CORRECT ORDER TO AVOID FK ERRORS
                IF OBJECT_ID('FactTransaction', 'U') IS NOT NULL DROP TABLE FactTransaction;
                IF OBJECT_ID('DimAccount', 'U') IS NOT NULL DROP TABLE DimAccount;
                IF OBJECT_ID('DimCustomer', 'U') IS NOT NULL DROP TABLE DimCustomer;
                IF OBJECT_ID('DimBranch', 'U') IS NOT NULL DROP TABLE DimBranch;

                -- RECREATE TABLES

                CREATE TABLE DimBranch (
                    BranchID INT PRIMARY KEY,
                    BranchName VARCHAR(100),
                    BranchLocation VARCHAR(100)
                );

                CREATE TABLE DimCustomer (
                    CustomerID INT PRIMARY KEY,
                    CustomerName VARCHAR(100),
                    Address VARCHAR(200),
                    CityName VARCHAR(100),
                    StateName VARCHAR(100),
                    Age INT,
                    Gender VARCHAR(10),
                    Email VARCHAR(100)
                );

                CREATE TABLE DimAccount (
                    AccountID INT PRIMARY KEY,
                    CustomerID INT,
                    AccountType VARCHAR(50),
                    Balance INT,
                    DateOpened DATETIME2,
                    Status VARCHAR(20),
                    FOREIGN KEY (CustomerID) REFERENCES DimCustomer(CustomerID)
                );

                CREATE TABLE FactTransaction (
                    TransactionID INT PRIMARY KEY,
                    AccountID INT,
                    TransactionDate DATETIME2,
                    Amount INT,
                    TransactionType VARCHAR(50),
                    BranchID INT,
                    FOREIGN KEY (AccountID) REFERENCES DimAccount(AccountID),
                    FOREIGN KEY (BranchID) REFERENCES DimBranch(BranchID)
                );
                """

cursor_DWH.execute(DWH_ddl_query)
conn_DWH.commit()
print("DWH tables recreated successfully!")

# ===========================
#  INSERT HELPER
# ===========================
cursor_DWH.fast_executemany = True

def load_table(df, table_name):
    cols = ",".join(df.columns)
    placeholders = ",".join(["?"] * len(df.columns))
    insert_query = f"""
        INSERT INTO {table_name} ({cols})
        VALUES ({placeholders})
    """
    data = list(df.itertuples(index=False, name=None))
    
    cursor_DWH.executemany(insert_query, data)
    conn_DWH.commit()
    print(f"{table_name} loaded ({len(df)} rows)")


# ===========================
#  LOAD DIM + FACT TABLES
# ===========================


# 1. CUSTOMER
load_table(
    dim_customer,
    "dbo.DimCustomer"
)

# 2. BRANCH
load_table(
    dim_branch,
    "dbo.DimBranch"
)

# 3. ACCOUNT
load_table(
    dim_account,
    "dbo.DimAccount"
)

# 4. FACT TRANSACTION
load_table(
    fact_transactions,
    "dbo.FactTransaction"
)
print("\n DWH Load Completed Successfully!")
