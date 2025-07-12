from flask import Blueprint, render_template, request, redirect, session, url_for
from app.forms.registeration_form import RegistrationForm
from app.forms.login_form import LoginForm
from app.services.account_service import AccountService
from app.models.role import Role
from app.States.context import UserContext

auth_routes = Blueprint("auth_routes", __name__)
account_service = AccountService()

# ------------------ اختيار نوع التسجيل ------------------
@auth_routes.route("/choose_signup")
def choose_signup():
    return render_template("html/choose_signup.html")

# ------------------ تسجيل الدخول ------------------
@auth_routes.route("/login", methods=["GET"])
def login_form():
    form = LoginForm()
    return render_template("html/login.html", form=form)

@auth_routes.route("/login", methods=["POST"])
def login_action():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        result = account_service.login(email, password)
        if result["success"]:
            account = result["account"]
            role = result["role"]

            # تحديد الحالة باستخدام الـ context
            context = UserContext(account)

            # ✅ تخزين بيانات المستخدم في الـ session
            session["user"] = {
                "id": account.id,
                "username": account.username,
                "role": account.role.name,
                "state": context.state.__class__.__name__
            }

            session["id"] = account.id
            session["role"] = role
            session["username"] = account.username

            # ✅ في حال كان مالك، خزّن session["owner"]
            if role == "owner":
                print("✅ Owner detected, redirecting to /owner/home")
                session["owner"] = {
                    "id": account.id,
                    "username": account.username,
                    "role": "owner"
                }
                session.modified = True
                return redirect(url_for("owner_routes.owner_home"))

            elif role == "user":
                return redirect(url_for("home"))

        # فشل تسجيل الدخول
        return render_template("html/login.html", form=form, error="Invalid email or password")

    # لم يتم التحقق من صحة النموذج
    return render_template("html/login.html", form=form)

# ------------------ تسجيل مستخدم ------------------
@auth_routes.route("/signup/user", methods=["GET", "POST"])
def signup_user():
    form = RegistrationForm()
    if request.method == "POST" and form.validate_on_submit():
        result = account_service.user_register(
            fname=form.fname.data,
            lname=form.lname.data,
            username=form.username.data,
            email=form.email.data,
            password=form.password.data
        )

        if result["success"]:
            return redirect(url_for("auth_routes.login_form"))
        else:
            return render_template("html/user_register.html", form=form, error=result.get("message"))

    return render_template("html/user_register.html", form=form)

# ------------------ تسجيل مالك ------------------
@auth_routes.route("/signup/owner", methods=["GET", "POST"])
def signup_owner():
    form = RegistrationForm()
    if request.method == "POST" and form.validate_on_submit():
        result = account_service.owner_register(
            fname=form.fname.data,
            lname=form.lname.data,
            username=form.username.data,
            email=form.email.data,
            password=form.password.data
        )

        if result["success"]:
            return redirect(url_for("auth_routes.login_form"))
        else:
            return render_template("html/owner_register.html", form=form, error=result.get("message"))

    return render_template("html/owner_register.html", form=form)
