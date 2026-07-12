import pandas as pd
from faker import Faker
import random

fake = Faker()
Faker.seed(42)
random.seed(42)


US_REGIONS = {
    "Northeast": ["NY", "NJ", "MA", "PA", "CT"],
    "Southeast": ["FL", "GA", "NC", "VA", "TN"],
    "Midwest": ["IL", "OH", "MI", "WI", "MN"],
    "Southwest": ["TX", "AZ", "NM", "OK"],
    "West": ["CA", "WA", "OR", "NV", "CO"],
}

def generate_branch(branch_id: int) -> dict:
    region = random.choice(list(US_REGIONS.keys()))
    state = random.choice(US_REGIONS[region])

    opened_date = fake.date_between(start_date="-30y", end_date="-1y")
    status = random.choices(["ACTIVE", "CLOSED"], weights=[0.9, 0.1])[0]

    return {
        "branch_id": f"BR{branch_id:05d}",
        "branch_name": f"{fake.city()} Branch",
        "region": region,
        "state": state,
        "city": fake.city(),
        "zip_code": fake.zipcode(),
        "opened_date": opened_date,
        "status": status,
        "manager_name": fake.name(),
    }

def generate_branches(num_branches: int = 50) -> pd.DataFrame:
    branches = [generate_branch(i) for i in range(1, num_branches + 1)]
    return pd.DataFrame(branches)


if __name__ == "__main__":
    df = generate_branches(num_branches=50)

    output_path = "data_generators/output/branches.csv"
    df.to_csv(output_path, index=False)

    print(f"Generated {len(df)} branches -> {output_path}")

    