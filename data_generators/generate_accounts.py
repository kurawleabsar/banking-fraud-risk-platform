import pandas as pd
from faker import Faker
import random

fake = Faker()
Faker.seed(42)
random.seed(42)

ACCOUNT_TYPES = ["CHECKING", "SAVINGS", "CREDIT_CARD", "MONEY_MARKET"]
ACCOUNT_TYPE_WEIGHTS = [0.45, 0.35, 0.15, 0.05]

ACCOUNT_STATUSES = ["OPEN", "CLOSED", "FROZEN", "DORMANT"]
ACCOUNT_STATUS_WEIGHTS = [0.85, 0.08, 0.03, 0.04]

customers_df = pd.read_csv("data_generators/output/customers.csv")
branches_df = pd.read_csv("data_generators/output/branches.csv")

customer_ids = customers_df["customer_id"].tolist()
branch_ids = branches_df["branch_id"].tolist()

def generate_account(account_id: int) -> dict:
    customer_id = random.choice(customer_ids)
    branch_id = random.choice(branch_ids)

    account_type = random.choices(ACCOUNT_TYPES, weights=ACCOUNT_TYPE_WEIGHTS)[0]
    account_status = random.choices(ACCOUNT_STATUSES, weights=ACCOUNT_STATUS_WEIGHTS)[0]

    opened_date = fake.date_between(start_date="-10y", end_date="-1d")
    closed_date = fake.date_between(start_date=opened_date, end_date="today") \
        if account_status == "CLOSED" else None

    current_balance = round(random.uniform(100, 50000), 2)
    available_balance = round(current_balance * random.uniform(0.9, 1.0), 2)

    interest_rate = round(random.uniform(0.01, 0.045), 4) \
        if account_type in ["SAVINGS", "MONEY_MARKET"] else None

    overdraft_limit = round(random.uniform(100, 1000), 2) \
        if account_type == "CHECKING" else None

    return {
        "account_id": f"AC{account_id:07d}",
        "customer_id": customer_id,
        "branch_id": branch_id,
        "account_type": account_type,
        "account_status": account_status,
        "currency": "USD",
        "current_balance": current_balance,
        "available_balance": available_balance,
        "interest_rate": interest_rate,
        "overdraft_limit": overdraft_limit,
        "opened_date": opened_date,
        "closed_date": closed_date,
    }

def generate_accounts(num_accounts: int = 7000) -> pd.DataFrame:
    accounts = [generate_account(i) for i in range(1, num_accounts + 1)]
    return pd.DataFrame(accounts)


if __name__ == "__main__":
    df = generate_accounts(num_accounts=7000)

    output_path = "data_generators/output/accounts.csv"
    df.to_csv(output_path, index=False)

    print(f"Generated {len(df)} accounts -> {output_path}")