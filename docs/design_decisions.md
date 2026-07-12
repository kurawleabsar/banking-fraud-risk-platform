# Design Decisions

## Why Medallion Architecture (Bronze/Silver/Gold)?

We use a medallion architecture instead of loading directly into one clean layer 
because banking data has regulatory and audit requirements that demand full 
history and reproducibility. Bronze preserves raw data exactly as received, 
immutable and append-only, so we can always answer "what did we actually 
receive, and when" — critical if a regulator asks us to reproduce a report 
as it existed months ago. Silver and Gold are both derived from Bronze, so 
if we discover a bug in our transformation logic, we can reprocess history 
from Bronze rather than having corrupted or lost the original data. This 
layered approach also separates failure domains: a broken transformation 
in Silver doesn't corrupt or overwrite the raw truth in Bronze.

## Why These 5 Entities?

Customer, Account, Transaction, Loan, and Branch represent the minimum set 
of entities needed to connect a person to their financial activity and risk 
exposure. Customer and Account establish who owns what; Transaction is the 
event stream that fraud detection depends on; Loan captures credit risk 
exposure needed for risk analytics and regulatory reporting (e.g., 
delinquency, default rates); and Branch provides the organizational/location 
context that ties accounts to physical business units, which regulators 
also care about for geographic risk concentration. Together these 5 entities 
support all three of our target use cases without needing additional source 
systems.

## Grain Decisions Per Consumer

Fraud detection needs transaction-level grain, often with rolling time-window 
aggregates (e.g., "transactions in the last 24 hours per account") since 
fraud patterns show up as anomalies in behavior over short windows. Risk 
analytics needs account- and loan-level grain, aggregating exposure, 
delinquency status, and balances at a point in time. Regulatory reporting 
needs point-in-time snapshots, often at the customer or loan level, since 
regulators require reproducible reports "as of" a specific date — this is 
exactly why Customer and Loan carry SCD Type 2 history.

## SCD Type 2 Usage

We apply SCD Type 2 to Customer and Loan because their key attributes 
(address, risk rating, loan status, delinquency) change relatively 
infrequently, and knowing their state at a specific point in time is 
essential for audits and regulatory reporting. We do not apply SCD2 to 
Account or Transaction: Transaction is already an immutable, append-only 
event log, so it doesn't need versioning — every row is already a permanent 
historical fact. Account's most frequently changing field, current_balance, 
is a derived value reconstructable from the Transaction log at any point in 
time, so applying SCD2 to it would explode a small reference table into 
something transaction-sized for no real benefit.