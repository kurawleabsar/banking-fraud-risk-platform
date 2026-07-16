import pandas as pd
from faker import Faker
import random
from datetime import date

fake = Faker()
Faker.seed(42)
random.seed(42)

CUSTOMER_SEGMENTS = ["RETAIL", "PREMIUM", "BUSINESS", "PRIVATE_BANKING"]
SEGMENT_WEIGHTS = [0.70, 0.20, 0.08, 0.02]

RISK_RATINGS = ["LOW", "MEDIUM", "HIGH"]
RISK_WEIGHTS = [0.75, 0.20, 0.05]

KYC_STATUSES = ["VERIFIED", "PENDING", "EXPIRED"]
KYC_WEIGHTS = [0.90, 0.07, 0.03]

def generate_customer(customer_id: int) -> dict:
    date_of_birth = fake.date_of_birth(minimum_age=18, maximum_age=90)
    customer_since_date = fake.date_between(start_date="-15y", end_date="-1y")

    segment = random.choices(CUSTOMER_SEGMENTS, weights=SEGMENT_WEIGHTS)[0]
    risk_rating = random.choices(RISK_RATINGS, weights=RISK_WEIGHTS)[0]
    kyc_status = random.choices(KYC_STATUSES, weights=KYC_WEIGHTS)[0]

    return {
        "customer_id": f"CU{customer_id:06d}",
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "date_of_birth": date_of_birth,
        "ssn": fake.ssn(),
        "email": fake.email(),
        "phone_number": fake.phone_number(),
        "address_line1": fake.street_address(),
        "city": fake.city(),
        "state": fake.state_abbr(),
        "zip_code": fake.zipcode(),
        "occupation": fake.job(),
        "employer_name": fake.company(),
        "customer_since_date": customer_since_date,
        "customer_segment": segment,
        "risk_rating": risk_rating,
        "kyc_status": kyc_status,
        "effective_start_date": customer_since_date,
        "effective_end_date": None,
        "is_current": True,
    }

def generate_customers(num_customers: int = 5000) -> pd.DataFrame:
    customers = [generate_customer(i) for i in range(1, num_customers + 1)]
    return pd.DataFrame(customers)


if __name__ == "__main__":
    df = generate_customers(num_customers=5000)

    output_path = "data_generators/output/customers.csv"
    df.to_csv(output_path, index=False)

    print(f"Generated {len(df)} customers -> {output_path}")

    