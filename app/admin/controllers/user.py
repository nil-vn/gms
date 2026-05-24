from flask_babel import _
from flask import redirect, request
from flask import render_template, flash, url_for, current_app

from app.admin.models import User
from app.admin.services.forms import (
    RegisterForm, UserUpdateForm,
)
from app.utils.db import db
from flask_login import login_required
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename
import os
import uuid
from . import routes, logger


@routes.route("/user/new", methods=["GET", "POST"])
@login_required
def register():
    form = RegisterForm()
    if form.validate_on_submit():  # Check if username/email đã tồn tại
        existing_user = User.find(username=form.username.data, email=form.email.data)
        if existing_user:
            flash(_("Username or email already exists"), "danger")
            return render_template("user_new.html", form=form)

        try:
            password_hash = generate_password_hash(form.password.data)

            # Tạo user mới
            user = User(
                username=form.username.data,
                email=form.email.data,
                password_hash=password_hash,
                role=form.role.data,
                status=form.status.data
            )

            # handle avatar upload
            if 'avatar' in request.files:
                file = request.files['avatar']
                if file and file.filename:
                    upload_folder = os.path.join(current_app.root_path, '..', 'static', 'uploads', 'avatars')
                    os.makedirs(upload_folder, exist_ok=True)
                    original_filename = secure_filename(file.filename)
                    save_name = f"{uuid.uuid4().hex}_{original_filename}"
                    file_path = os.path.join(upload_folder, save_name)
                    file.save(file_path)
                    user.avatar = f"uploads/avatars/{save_name}"

            db.session.add(user)
            db.session.commit()
            flash(_("Account created successfully!"), "success")
        except Exception as e:
            db.session.rollback()
            logger.exception(e)
            flash(_("Could not create user"), "error")
        finally:
            return redirect(url_for('admin_routes.register'))
    elif form.errors:
        for err_code, err_content in form.errors.items():
            for e in err_content:
                flash(_(f"{err_code}: {e}"), "danger")
        return redirect(url_for('admin_routes.register'))
    return render_template("user_new.html", form=form)


@routes.route("/users")
@login_required
def users():
    all_users = User.get_all()
    admin_users = [u for u in all_users if str(getattr(u, 'role', '')).lower() == 'admin']
    staff_users = [u for u in all_users if str(getattr(u, 'role', '')).lower() != 'admin']
    return render_template("users.html", users=all_users, admin_users=admin_users, staff_users=staff_users)


@routes.route("/user/<int:user_id>/delete", methods=["GET"])
@login_required
def delete_user(user_id):
    user = User.get_by_id(user_id)
    if not user:
        flash(_("User not found."), "danger")
        return redirect(url_for("admin_routes.users"))

    try:    
        db.session.delete(user)
        db.session.commit()
        flash(_("User deleted successfully!"), "success")
    except Exception as e:
        db.session.rollback()  # rollback nếu lỗi
        flash(_(f"Error deleting user: {e}"), "danger")

    return redirect(url_for("admin_routes.users"))

@routes.route("/user/<user_id>", methods=["GET", "POST"])
@login_required
def user_detail(user_id):
    user = User.query.get_or_404(user_id)
    form = UserUpdateForm(obj=user)  # populate form với dữ liệu hiện tại

    if form.validate_on_submit():
        # Kiểm tra username/email có trùng với user khác không
        existing_user = User.query.filter(
            ((User.username == form.username.data) | (User.email == form.email.data)) &
            (User.id != user.id)
        ).first()
        if existing_user:
            flash(_("Username or email already exists"), "danger")
            return redirect(url_for('admin_routes.user_detail', user_id=user_id))

        try:
            # Cập nhật thông tin user
            user.username = form.username.data
            user.email = form.email.data
            user.role = form.role.data
            user.status = form.status.data

            # Nếu có nhập password mới, hash lại
            if form.password.data:
                user.password_hash = generate_password_hash(form.password.data)

            # handle avatar upload
            if 'avatar' in request.files:
                file = request.files['avatar']
                if file and file.filename:
                    # Delete old avatar file if it exists
                    if user.avatar:
                        old_path = os.path.join(current_app.root_path, '..', 'static', user.avatar)
                        if os.path.exists(old_path):
                            try:
                                os.remove(old_path)
                            except Exception:
                                pass
                    
                    upload_folder = os.path.join(current_app.root_path, '..', 'static', 'uploads', 'avatars')
                    os.makedirs(upload_folder, exist_ok=True)
                    original_filename = secure_filename(file.filename)
                    save_name = f"{uuid.uuid4().hex}_{original_filename}"
                    file_path = os.path.join(upload_folder, save_name)
                    file.save(file_path)
                    user.avatar = f"uploads/avatars/{save_name}"

            db.session.commit()
            flash(_("User updated successfully!"), "success")
        except Exception as e:
            db.session.rollback()
            logger.exception(e)
            flash(_("Could not update user"), "danger")
        finally:
            return redirect(url_for('admin_routes.user_detail', user_id=user_id))
    elif form.errors:
        for field, errors in form.errors.items():
            for e in errors:
                flash(_(f"{field}: {e}"), "danger")
        return redirect(url_for('admin_routes.user_detail', user_id=user_id))

    return render_template("user_detail.html", form=form, user=user)