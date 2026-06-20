"""Fix out-of-sync emails between User and Employee tables."""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), nullable=False, default="employee")


class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    department = db.Column(db.String(100), nullable=False)
    position = db.Column(db.String(100), nullable=False)
    salary = db.Column(db.Float, nullable=False)
    address = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)


with app.app_context():
    employees = Employee.query.all()
    fixed = 0
    for emp in employees:
        user = db.session.get(User, emp.user_id)
        if user and user.email != emp.email:
            print(f"OUT OF SYNC: '{emp.name}' -> employee.email='{emp.email}', user.email='{user.email}'")
            user.email = emp.email
            fixed += 1
        else:
            print(f"OK: '{emp.name}' -> email='{emp.email}'")

    if fixed > 0:
        db.session.commit()
        print(f"\nFixed {fixed} out-of-sync email(s).")
    else:
        print("\nAll emails are in sync.")
