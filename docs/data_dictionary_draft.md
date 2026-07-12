# Data Dictionary — Draft

## Branch

| Column          | Type      | Nullable | PII | Description                                   |
|-----------------|-----------|----------|-----|------------------------------------------------|
| branch_id       | STRING    | No       | N   | Unique identifier for the branch (PK)          |
| branch_name     | STRING    | No       | N   | Display name of the branch                     |
| region          | STRING    | No       | N   | Business region (e.g., Northeast, Midwest)      |
| state           | STRING    | No       | N   | US state code                                   |
| city            | STRING    | No       | N   | City where branch is located                    |
| zip_code        | STRING    | No       | N   | Postal code                                     |
| opened_date     | DATE      | No       | N   | Date branch opened                              |
| status          | STRING    | No       | N   | ACTIVE / CLOSED                                 |
| manager_name    | STRING    | Yes      | Y   | Name of branch manager (PII — employee)         |

## Customer

| Column               | Type      | Nullable | PII | Description                                          |
|----------------------|-----------|----------|-----|-------------------------------------------------------|
| customer_id          | STRING    | No       | N   | Unique identifier for the customer (PK)               |
| first_name           | STRING    | No       | Y   | Customer's first name                                 |
| last_name            | STRING    | No       | Y   | Customer's last name                                  |
| date_of_birth        | DATE      | No       | Y   | Date of birth                                         |
| ssn                  | STRING    | No       | Y   | Government-issued ID number (masked in non-Bronze)    |
| email                | STRING    | Yes      | Y   | Contact email                                          |
| phone_number         | STRING    | Yes      | Y   | Contact phone number                                   |
| address_line1        | STRING    | Yes      | Y   | Street address                                         |
| city                 | STRING    | Yes      | N   | City of residence                                      |
| state                | STRING    | Yes      | N   | State code                                             |
| zip_code             | STRING    | Yes      | N   | Postal code                                            |
| occupation           | STRING    | Yes      | Y   | Customer's stated occupation                           |
| employer_name        | STRING    | Yes      | Y   | Customer's employer                                    |
| customer_since_date  | DATE      | No       | N   | Date the customer relationship began                   |
| customer_segment     | STRING    | No       | N   | RETAIL / PREMIUM / BUSINESS / PRIVATE_BANKING          |
| risk_rating          | STRING    | No       | N   | LOW / MEDIUM / HIGH — internally assigned AML risk     |
| kyc_status           | STRING    | No       | N   | VERIFIED / PENDING / EXPIRED                           |
| effective_start_date | DATE      | No       | N   | SCD2: when this version of the row became active       |
| effective_end_date   | DATE      | Yes      | N   | SCD2: when this version was superseded (NULL if current)|
| is_current           | BOOLEAN   | No       | N   | SCD2: flags the currently active row                   |

## Account

| Column            | Type      | Nullable | PII | Description                                              |
|-------------------|-----------|----------|-----|------------------------------------------------------------|
| account_id        | STRING    | No       | N   | Unique identifier for the account (PK)                     |
| customer_id       | STRING    | No       | N   | FK to Customer — account owner                             |
| branch_id         | STRING    | Yes      | N   | FK to Branch — where account was opened                    |
| account_type      | STRING    | No       | N   | CHECKING / SAVINGS / CREDIT_CARD / MONEY_MARKET             |
| account_status    | STRING    | No       | N   | OPEN / CLOSED / FROZEN / DORMANT                            |
| currency          | STRING    | No       | N   | ISO currency code (e.g., USD, EUR)                          |
| current_balance   | DECIMAL   | No       | N   | Current account balance                                      |
| available_balance | DECIMAL   | No       | N   | Balance available for withdrawal (may differ from current)   |
| interest_rate     | DECIMAL   | Yes      | N   | Applicable interest rate (NULL for non-interest accounts)   |
| overdraft_limit   | DECIMAL   | Yes      | N   | Max overdraft allowed (NULL if not applicable)               |
| opened_date       | DATE      | No       | N   | Date account was opened                                     |
| closed_date       | DATE      | Yes      | N   | Date account was closed (NULL if still open)                |

## Transaction

| Column                | Type      | Nullable | PII | Description                                                    |
|------------------------|-----------|----------|-----|------------------------------------------------------------------|
| transaction_id         | STRING    | No       | N   | Unique identifier for the transaction (PK)                      |
| account_id             | STRING    | No       | N   | FK to Account                                                    |
| counterparty_account_id| STRING    | Yes      | N   | FK to Account — other side of a transfer (NULL if not a transfer)|
| transaction_type       | STRING    | No       | N   | DEBIT / CREDIT / TRANSFER / WITHDRAWAL / DEPOSIT / PAYMENT       |
| channel                | STRING    | No       | N   | ONLINE / ATM / POS / MOBILE / WIRE / BRANCH                      |
| amount                 | DECIMAL   | No       | N   | Transaction amount                                                |
| currency               | STRING    | No       | N   | ISO currency code                                                 |
| merchant_name          | STRING    | Yes      | N   | Merchant involved (NULL for internal transfers)                  |
| merchant_category_code | STRING    | Yes      | N   | MCC code — standardized merchant category                        |
| transaction_timestamp  | TIMESTAMP | No       | N   | Exact date/time of transaction                                    |
| transaction_status     | STRING    | No       | N   | COMPLETED / PENDING / DECLINED / REVERSED                        |
| ip_address             | STRING    | Yes      | Y   | IP address (for online/mobile channels)                         |
| device_id              | STRING    | Yes      | Y   | Device fingerprint (for online/mobile channels)                 |
| geo_country            | STRING    | Yes      | N   | Country where transaction occurred                               |
| geo_city               | STRING    | Yes      | N   | City where transaction occurred                                  |
| geo_latitude           | DECIMAL   | Yes      | N   | Latitude of transaction location                                  |
| geo_longitude          | DECIMAL   | Yes      | N   | Longitude of transaction location                                 |
| is_fraud_flag          | BOOLEAN   | No       | N   | Ground-truth fraud label (synthetic, for model training)         |
| ingestion_timestamp    | TIMESTAMP | No       | N   | When this record was ingested into Bronze                        |

## Loan

| Column               | Type      | Nullable | PII | Description                                                     |
|-----------------------|-----------|----------|-----|--------------------------------------------------------------------|
| loan_id               | STRING    | No       | N   | Unique identifier for the loan (PK)                                |
| customer_id           | STRING    | No       | N   | FK to Customer — loan holder                                       |
| account_id            | STRING    | Yes      | N   | FK to Account — linked disbursement/payment account                |
| loan_type             | STRING    | No       | N   | MORTGAGE / AUTO / PERSONAL / STUDENT / BUSINESS                    |
| principal_amount      | DECIMAL   | No       | N   | Original amount borrowed                                            |
| outstanding_balance   | DECIMAL   | No       | N   | Current remaining balance owed                                       |
| interest_rate         | DECIMAL   | No       | N   | Annual interest rate                                                 |
| interest_rate_type    | STRING    | No       | N   | FIXED / VARIABLE                                                    |
| term_months           | INTEGER   | No       | N   | Loan term length in months                                           |
| origination_date      | DATE      | No       | N   | Date loan was issued                                                 |
| maturity_date         | DATE      | No       | N   | Scheduled payoff date                                                |
| monthly_payment       | DECIMAL   | No       | N   | Expected monthly payment amount                                      |
| loan_status           | STRING    | No       | N   | ACTIVE / PAID_OFF / DEFAULT / DELINQUENT / CHARGED_OFF               |
| days_past_due         | INTEGER   | No       | N   | Number of days current payment is overdue (0 if current)             |
| collateral_value      | DECIMAL   | Yes      | N   | Value of collateral (NULL for unsecured loans like personal loans)   |
| effective_start_date  | DATE      | No       | N   | SCD2: when this version of the row became active                    |
| effective_end_date    | DATE      | Yes      | N   | SCD2: when this version was superseded (NULL if current)             |
| is_current            | BOOLEAN   | No       | N   | SCD2: flags the currently active row                                 |
