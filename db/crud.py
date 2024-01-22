import os
import threading
import time
import pandas as pd
from sqlalchemy.orm import Session
import models.models as models, db.schemas as schemas
import requests
from decouple import config
from sqlalchemy import func
import sched
from datetime import datetime, timedelta

# Create customers
def create_customers(db: Session, customers_data: schemas.CustomersCreate):
    db_customers = models.Customers(**customers_data.dict())
    db.add(db_customers)
    db.commit()
    db.refresh(db_customers)
    return db_customers

# Get last customer sequence number from db
def get_last_customer_sequence_number(db: Session):
    last_sequence_number = db.query(models.Customers.id).order_by(models.Customers.id.desc()).first()
    if last_sequence_number:
        return last_sequence_number[0]
    else:
        return 0

def create_customers_new_user(db: Session, customers_request: schemas.CustomerCreateRequestBody):
    excel_file_path = os.getenv("CUSTOMERS_EXCEL_FILE")

    data_fields = pd.read_excel(excel_file_path)

    customer_names = data_fields['Name'].tolist()
    email_values = data_fields['Email'].tolist()
    phone_values = data_fields['Phone'].tolist()
    address_values = data_fields['Address'].tolist()
    registration_date_values = data_fields['Registration_Date'].tolist()

    sequence_number = get_last_customer_sequence_number(db) + 1

    new_customers = []
    for j in range(len(data_fields)):
        customer_code = f"CUST-FAL-23-24-{sequence_number}"

        name = customer_names[j] if customer_names else ""
        email = email_values[j] if email_values else ""
        phone = phone_values[j] if phone_values else ""
        address = address_values[j] if address_values else ""
        registration_date = registration_date_values[j] if registration_date_values else ""

        existing_customer = db.query(models.Customers).filter_by(
            name=name, email=email, phone=phone, address=address, registration_date=registration_date
        ).first()

        if existing_customer:
            continue

        customer = models.Customers(
            name=name,
            customer_code=customer_code,
            email=email,
            phone=phone,
            address=address,
            registration_date=registration_date,
            status="active",
            created_date=datetime.now(),
            last_updated_date=None
        )
        sequence_number += 1
        new_customers.append(customer)

    db.add_all(new_customers)
    db.commit()
    for customer in new_customers:
        db.refresh(customer)
    return new_customers

# Get customers by id
def get_customer_by_id(db: Session, id: int):
    return db.query(models.Customers).filter(models.Customers.id == id).first()

# Get all customers
def get_all_customers(db: Session):
    return db.query(models.Customers).all()

# Insert all customers
def insert_all_customers(db):
    falca_users_response = requests.get(config("USER_PROFILE_SERVICE_API")).json()

    data = falca_users_response.get("data", [])
    falca_users_response = data[0] if data else []

    excel_file_path = os.getenv("CUSTOMERS_EXCEL_FILE")

    data_fields = pd.read_excel(excel_file_path)

    customer_names = data_fields['Name'].tolist()
    email_values = data_fields['Email'].tolist()
    phone_values = data_fields['Phone'].tolist()
    address_values = data_fields['Address'].tolist()
    registration_date_values = data_fields['Registration_Date'].tolist()

    sequence_number = get_last_customer_sequence_number(db) + 1

    customers = []
    for i, falca_user in enumerate(falca_users_response):
        user_id = falca_user["id"]
        phone_number = falca_user["Phone"]
        center = falca_user["Center"]
        center_code = falca_user["CenterCode"]

        last_three_digits = phone_number[-3:]

        for j in range(len(data_fields)):
            customer_code = f"CUST-FAL-23-24-{sequence_number}"

            name = customer_names[j] if customer_names else ""
            email = email_values[j] if email_values else ""
            phone = phone_values[j] if phone_values else ""
            address = address_values[j] if address_values else ""
            registration_date = registration_date_values[j] if registration_date_values else ""

            existing_customer = db.query(models.Customers).filter_by(
                name=name, email=email, phone=phone, address=address, registration_date=registration_date
            ).first()

            if existing_customer:
                continue

            customer = models.Customers(
                name=name,
                customer_code=customer_code,
                email=email,
                phone=phone,
                address=address,
                registration_date=registration_date,
                status="active",
                created_date=datetime.now(),
                last_updated_date=None
            )
            sequence_number += 1
            customers.append(customer)
    db.add_all(customers)
    db.commit()
    db.close()
    print("Customers added successfully.")

scheduler = sched.scheduler(time.time, time.sleep)

def schedule_customers_inserting_task(db: Session):
    insert_all_customers(db)

    now = datetime.now()
    midnight = now.replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1)

    delta = (midnight - now).total_seconds()

    scheduler.enter(60, 1, schedule_customers_inserting_task, (db,))

def start_customer_scheduler(db: Session):
    now = datetime.now()
    midnight = now.replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1)

    delta = (midnight - now).total_seconds()

    scheduler.enter(60, 1, insert_all_customers, (db,))

    scheduler.enter(60 + 86400, 1, schedule_customers_inserting_task, (db,))

    scheduler_thread = threading.Thread(target=scheduler.run)
    scheduler_thread.start()
