from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash, check_password_hash
import os

load_dotenv()

app = Flask(__name__)

app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

from models import User, Employee


def create_admin():
    existing_admin = User.query.filter_by(email="admin@gmail.com").first()

    if not existing_admin:
        admin = User(
            name="Admin",
            email="admin@gmail.com",
            password=generate_password_hash("admin123"),
            role="admin"
        )

        db.session.add(admin)
        db.session.commit()
        print("Admin created successfully!")


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/services")
def services():
    return render_template("services.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            session["user_id"] = user.id
            session["user_name"] = user.name
            session["role"] = user.role

            flash("Login successful!", "success")

            if user.role == "admin":
                return redirect(url_for("admin_dashboard"))
            else:
                return redirect(url_for("employee_dashboard"))

        flash("Invalid email or password!", "danger")
        return redirect(url_for("login"))

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    flash("Logged out successfully!", "success")
    return redirect(url_for("login"))


@app.route("/admin/dashboard")
def admin_dashboard():
    if "user_id" not in session:
        return redirect(url_for("login"))

    if session.get("role") != "admin":
        flash("Access denied!", "danger")
        return redirect(url_for("login"))

    return render_template("admin_dashboard.html")

@app.route("/employee/dashboard")
def employee_dashboard():

    if "user_id" not in session:
        return redirect(url_for("login"))

    if session.get("role") != "employee":
        flash("Access denied!", "danger")
        return redirect(url_for("login"))

    employee = Employee.query.filter_by(
        user_id=session["user_id"]
    ).first()

    return render_template(
        "employee_dashboard.html",
        employee=employee
    )


@app.route("/employees/add", methods=["GET", "POST"])
def add_employee():
    print(session)
    if "user_id" not in session or session.get("role") != "admin":
        flash("Access denied!", "danger")
        return redirect(url_for("login"))

    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        phone = request.form["phone"]
        department = request.form["department"]
        position = request.form["position"]
        salary = request.form["salary"]
        address = request.form["address"]

        existing_user = User.query.filter_by(email=email).first()

        if existing_user:
            flash("Email already exists!", "danger")
            return redirect(url_for("add_employee"))

        employee_user = User(
            name=name,
            email=email,
            password=generate_password_hash("employee123"),
            role="employee"
        )

        db.session.add(employee_user)
        db.session.commit()

        new_employee = Employee(
            name=name,
            email=email,
            phone=phone,
            department=department,
            position=position,
            salary=salary,
            address=address,
            user_id=employee_user.id
        )

        db.session.add(new_employee)
        db.session.commit()

        flash("Employee added successfully! Default password is employee123", "success")
        return redirect(url_for("admin_dashboard"))

    return render_template("add_employee.html")


@app.route("/employees")
def view_employees():
    if "user_id" not in session or session.get("role") != "admin":
        flash("Access denied!", "danger")
        return redirect(url_for("login"))

    employees = Employee.query.all()
    return render_template("employees.html", employees=employees)


@app.route("/employees/edit/<int:id>", methods=["GET", "POST"])
def edit_employee(id):
    if "user_id" not in session or session.get("role") != "admin":
        flash("Access denied!", "danger")
        return redirect(url_for("login"))

    employee = Employee.query.get_or_404(id)
    user = User.query.get(employee.user_id)

    if request.method == "POST":
        new_email = request.form["email"]

        # Check if email already belongs to another user or employee
        existing_user = User.query.filter(User.email == new_email, User.id != user.id).first()
        existing_emp = Employee.query.filter(Employee.email == new_email, Employee.id != employee.id).first()
        if existing_user or existing_emp:
            flash("Email already exists for another user!", "danger")
            return redirect(url_for("edit_employee", id=id))

        employee.name = request.form["name"]
        employee.email = new_email
        employee.phone = request.form["phone"]
        employee.department = request.form["department"]
        employee.position = request.form["position"]
        employee.salary = request.form["salary"]
        employee.address = request.form["address"]

        user.name = request.form["name"]
        user.email = new_email

        db.session.commit()

        flash("Employee updated successfully!", "success")
        return redirect(url_for("view_employees"))

    return render_template("edit_employee.html", employee=employee)




@app.route("/employees/delete/<int:id>")
def delete_employee(id):
    if "user_id" not in session or session.get("role") != "admin":
        flash("Access denied!", "danger")
        return redirect(url_for("login"))

    employee = Employee.query.get_or_404(id)
    user = User.query.get(employee.user_id)

    db.session.delete(employee)
    db.session.delete(user)

    db.session.commit()

    flash("Employee deleted successfully!", "success")
    return redirect(url_for("view_employees"))



@app.route("/profile")
def profile():
    if "user_id" not in session:
        return redirect(url_for("login"))

    if session.get("role") != "employee":
        flash("Access denied!", "danger")
        return redirect(url_for("login"))

    employee = Employee.query.filter_by(user_id=session["user_id"]).first()

    return render_template("profile.html", employee=employee)



@app.route("/profile/edit", methods=["GET", "POST"])
def edit_profile():
    if "user_id" not in session:
        return redirect(url_for("login"))

    if session.get("role") != "employee":
        flash("Access denied!", "danger")
        return redirect(url_for("login"))

    employee = Employee.query.filter_by(user_id=session["user_id"]).first()
    user = User.query.get(session["user_id"])

    if request.method == "POST":
        new_email = request.form["email"]

        # Check if email already belongs to another user or employee
        existing_user = User.query.filter(User.email == new_email, User.id != user.id).first()
        existing_emp = Employee.query.filter(Employee.email == new_email, Employee.id != employee.id).first()
        if existing_user or existing_emp:
            flash("Email already exists for another user!", "danger")
            return redirect(url_for("edit_profile"))

        employee.phone = request.form["phone"]
        employee.address = request.form["address"]
        employee.email = new_email
        user.email = new_email

        db.session.commit()

        flash("Profile updated successfully!", "success")
        return redirect(url_for("profile"))

    return render_template("edit_profile.html", employee=employee)




@app.route("/api/employees", methods=["GET"])
def api_get_employees():
    employees = Employee.query.all()

    employee_list = []

    for emp in employees:
        employee_list.append({
            "id": emp.id,
            "name": emp.name,
            "email": emp.email,
            "phone": emp.phone,
            "department": emp.department,
            "position": emp.position,
            "salary": emp.salary,
            "address": emp.address
        })

    return jsonify(employee_list), 200


@app.route("/api/employees/<int:id>", methods=["GET"])
def api_get_employee(id):

    employee = Employee.query.get_or_404(id)

    data = {
        "id": employee.id,
        "name": employee.name,
        "email": employee.email,
        "phone": employee.phone,
        "department": employee.department,
        "position": employee.position,
        "salary": employee.salary,
        "address": employee.address
    }

    return jsonify(data), 200

@app.route("/api/employees", methods=["POST"])
def api_create_employee():

    data = request.get_json()

    user = User(
        name=data["name"],
        email=data["email"],
        password=generate_password_hash("employee123"),
        role="employee"
    )

    db.session.add(user)
    db.session.commit()

    employee = Employee(
        name=data["name"],
        email=data["email"],
        phone=data["phone"],
        department=data["department"],
        position=data["position"],
        salary=data["salary"],
        address=data["address"],
        user_id=user.id
    )

    db.session.add(employee)
    db.session.commit()

    return jsonify({
        "message": "Employee created successfully"
    }), 201

@app.route("/api/employees/<int:id>", methods=["PUT"])
def api_update_employee(id):

    employee = Employee.query.get_or_404(id)
    user = User.query.get(employee.user_id)

    data = request.get_json()

    employee.name = data["name"]
    employee.email = data["email"]
    employee.phone = data["phone"]
    employee.department = data["department"]
    employee.position = data["position"]
    employee.salary = data["salary"]
    employee.address = data["address"]

    user.name = data["name"]
    user.email = data["email"]

    db.session.commit()

    return jsonify({
        "message": "Employee updated successfully"
    }), 200

@app.route("/api/employees/<int:id>", methods=["DELETE"])
def api_delete_employee(id):

    employee = Employee.query.get_or_404(id)
    user = User.query.get(employee.user_id)

    db.session.delete(employee)
    db.session.delete(user)
    db.session.commit()

    return jsonify({
        "message": "Employee deleted successfully"
    }), 200





if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        create_admin()

    app.run(debug=True)