from types import SimpleNamespace
import os
import socket
import uuid

from flask import redirect, request, make_response, jsonify
from flask import flash, url_for, current_app
from flask_babel import _ as _t, get_locale

from app.admin.models import User, Customer
from app.admin.services.forms import (
    RegisterForm,
)
from app.utils.db import db
from werkzeug.security import generate_password_hash

from flask import render_template
from flask_login import login_required
from . import routes
from ..services.analytics import get_metrics
from app.utils.settings import get_setting, set_setting


@routes.route("/")
@routes.route("/dashboard")
@login_required
def dashboard():
    metric = get_metrics()
    return render_template("dashboard.html", metric=metric)

ALLOWED_LOGO_EXTENSIONS = {"png", "jpg", "jpeg", "svg", "webp"}
MAX_LOGO_SIZE_BYTES = 5 * 1024 * 1024  # 2 MB


def _save_logo_file(file) -> str:
    """Save uploaded logo file, return relative static path or empty string on failure."""
    if not file or not file.filename:
        return ""
    ext = file.filename.rsplit(".", 1)[-1].lower() if "." in file.filename else ""
    if ext not in ALLOWED_LOGO_EXTENSIONS:
        return ""
    # Read content to check size
    content = file.read()
    if len(content) > MAX_LOGO_SIZE_BYTES:
        return ""
    uploads_dir = os.path.join(current_app.static_folder, "common", "img", "uploads")
    os.makedirs(uploads_dir, exist_ok=True)
    # Remove old logo files
    for old_file in os.listdir(uploads_dir):
        if old_file.startswith("system_logo."):
            try:
                os.remove(os.path.join(uploads_dir, old_file))
            except OSError:
                pass
    filename = f"system_logo.{ext}"
    filepath = os.path.join(uploads_dir, filename)
    with open(filepath, "wb") as f:
        f.write(content)
    return f"common/img/uploads/{filename}"


@routes.route("/system", methods=["GET", "POST"])
@login_required
def system():
    if request.method == "POST":
        set_setting("currency", request.form.get("currency", "JPY"))
        set_setting("theme", request.form.get("theme", "dark"))
        set_setting("language", request.form.get("language", "vi"))
        set_setting("system_name", request.form.get("system_name", "").strip())

        # Handle logo upload
        logo_file = request.files.get("system_logo")
        if logo_file and logo_file.filename:
            logo_path = _save_logo_file(logo_file)
            if logo_path:
                set_setting("system_logo", logo_path)
            else:
                flash(_t("Invalid logo file. Use PNG, JPG, SVG or WEBP under 2 MB."), "warning")
        elif request.form.get("remove_logo") == "1":
            # Remove existing logo
            from app.utils.settings import get_setting as _gs
            old_logo = _gs("system_logo")
            if old_logo:
                old_path = os.path.join(current_app.static_folder, old_logo.replace("/", os.sep))
                try:
                    os.remove(old_path)
                except OSError:
                    pass
            set_setting("system_logo", "")

        flash(_t("Settings saved successfully!"), "success")
        response = make_response(redirect(url_for("admin_routes.system")))
        response.set_cookie("lang", request.form.get("language", "vi"), max_age=30*24*60*60, path="/")
        return response

    # Detect server host, local IP and port for admin QR code
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 1))
        local_ip = s.getsockname()[0]
    except Exception:
        local_ip = "127.0.0.1"
    finally:
        s.close()

    pc_name = socket.gethostname()
    host_parts = request.host.split(":")
    port = host_parts[1] if len(host_parts) > 1 else "80"

    qr_urls = {
        "ip": f"http://{local_ip}:{port}/admin",
        "hostname": f"http://{pc_name}:{port}/admin",
        "localhost": f"http://127.0.0.1:{port}/admin"
    }

    settings = {
        "currency": get_setting("currency"),
        "theme": get_setting("theme"),
        "language": str(get_locale()),
        "system_name": get_setting("system_name"),
        "system_logo": get_setting("system_logo"),
    }
    return render_template("system.html", settings=settings, qr_urls=qr_urls)


@routes.route("/api/revenue-chart", methods=["GET"])
@login_required
def api_revenue_chart():
    from app.admin.services.analytics import get_revenue_by_range
    range_type = request.args.get("range", "6m")
    try:
        raw_data = get_revenue_by_range(range_type)
        labels = [item["label"] for item in raw_data]
        data = [item["revenue"] for item in raw_data]
        return jsonify({
            "status": "success",
            "labels": labels,
            "data": data
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


@routes.route("/api/metrics-trend", methods=["GET"])
@login_required
def api_metrics_trend():
    from app.admin.models import Car, Customer, Transaction, User
    import calendar
    from datetime import datetime
    
    now = datetime.utcnow()
    months = []
    for i in range(5, -1, -1):
        y = now.year
        m = now.month - i
        while m <= 0:
            m += 12
            y -= 1
        last_day = calendar.monthrange(y, m)[1]
        end_date = datetime(y, m, last_day, 23, 59, 59, 999999)
        months.append(end_date)
        
    try:
        # Cars
        cars_trend_total = []
        cars_trend_available = []
        cars_trend_sold = []
        for end_date in months:
            total = Car.query.filter(Car.created_at <= end_date).count()
            available = Car.query.filter(Car.created_at <= end_date, Car.status.in_(['AVAILABLE', 'AWAITING_DELIVERY'])).count()
            sold = Car.query.filter(Car.created_at <= end_date, Car.status == 'SOLD').count()
            cars_trend_total.append(total)
            cars_trend_available.append(available)
            cars_trend_sold.append(sold)
            
        # Customers
        cust_trend_total = []
        cust_trend_active = []
        cust_trend_potential = []
        for end_date in months:
            total = Customer.query.filter(Customer.created_at <= end_date).count()
            active = Customer.query.filter(Customer.created_at <= end_date, Customer.status == 'Active').count()
            potential = Customer.query.filter(Customer.created_at <= end_date, Customer.status == 'Inactive').count()
            cust_trend_total.append(total)
            cust_trend_active.append(active)
            cust_trend_potential.append(potential)
            
        # Transactions
        tx_trend_total = []
        tx_trend_paid = []
        tx_trend_deposited = []
        for end_date in months:
            txs = Transaction.query.filter(Transaction.created_at <= end_date).all()
            total = sum(t.total_amount or 0 for t in txs if t.status in ['PAID', 'DEPOSITED', 'Paid', 'paid'])
            paid = sum(t.total_amount or 0 for t in txs if t.status in ['PAID', 'Paid', 'paid'])
            deposited = sum(t.deposit_amount or 0 for t in txs if t.status == 'DEPOSITED')
            tx_trend_total.append(total)
            tx_trend_paid.append(paid)
            tx_trend_deposited.append(deposited)
            
        # Users
        users_trend_total = []
        users_trend_admin = []
        users_trend_staff = []
        for end_date in months:
            total = User.query.filter(User.created_date <= end_date).count()
            admin = User.query.filter(User.created_date <= end_date, User.role == 'admin').count()
            staff = User.query.filter(User.created_date <= end_date, User.role != 'admin').count()
            users_trend_total.append(total)
            users_trend_admin.append(admin)
            users_trend_staff.append(staff)
            
        return jsonify({
            "status": "success",
            "cars": {
                "total": cars_trend_total,
                "available": cars_trend_available,
                "sold": cars_trend_sold
            },
            "customers": {
                "total": cust_trend_total,
                "active": cust_trend_active,
                "potential": cust_trend_potential
            },
            "transactions": {
                "total": tx_trend_total,
                "paid": tx_trend_paid,
                "deposited": tx_trend_deposited
            },
            "users": {
                "total": users_trend_total,
                "admin": users_trend_admin,
                "staff": users_trend_staff
            }
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500





@routes.route("/set_language/<lang>")
def set_language(lang):
    if lang not in ["vi", "en", "ja"]:
        lang = "vi"
    response = redirect(request.referrer or url_for("admin_routes.dashboard"))
    response.set_cookie("lang", lang, max_age=60*60*24*365, path="/")
    return response
