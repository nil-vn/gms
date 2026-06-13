from flask_babel import _
from flask import request, redirect, jsonify, current_app
from flask import render_template, flash, url_for

from app.admin.models import Car, Customer, RepairOrder, RepairItem
from app.admin.services.forms import RepairOrderForm
from app.utils.db import db
from flask_login import login_required
from . import routes
from app.utils.constants import RepairStatus, CarStatus


@routes.route("/repairs")
@login_required
def repairs():
    all_repairs = RepairOrder.get_all()
    pending_repairs = [r for r in all_repairs if r.status == RepairStatus.PENDING.name]
    in_progress_repairs = [r for r in all_repairs if r.status == RepairStatus.IN_PROGRESS.name]
    done_repairs = [r for r in all_repairs if r.status == RepairStatus.DONE.name]

    return render_template(
        "repairs.html",
        repairs=all_repairs,
        pending_repairs=pending_repairs,
        in_progress_repairs=in_progress_repairs,
        done_repairs=done_repairs
    )


@routes.route("/repair/new", methods=["GET", "POST"])
@login_required
def repair_new():
    form = RepairOrderForm()
    
    if request.method == "POST":
        customer_id = request.form.get("customer_id")
        car_id = request.form.get("car_id")
        
        # Xử lý Khách vãng lai (Tạo nhanh Customer và Car)
        if not customer_id and request.form.get("walkin_name"):
            new_customer = Customer(
                name=request.form.get("walkin_name"),
                phone=request.form.get("walkin_phone"),
                status="Active",
                note="Khách vãng lai gửi sửa xe"
            )
            db.session.add(new_customer)
            db.session.flush() # Lấy ID ngay
            customer_id = new_customer.id
            
        if not car_id and request.form.get("walkin_license_plate"):
            new_car = Car(
                name=request.form.get("walkin_model", "Xe Khách"),
                model=request.form.get("walkin_model"),
                license_plate_no=request.form.get("walkin_license_plate"),
                status=CarStatus.SERVICE_ONLY.name,
                note="Xe khách vãng lai gửi sửa"
            )
            db.session.add(new_car)
            db.session.flush()
            car_id = new_car.id
            
        if not customer_id or not car_id:
            flash(_("Please select or create a customer and car."), "danger")
            return redirect(url_for("admin_routes.repair_new"))

        if form.validate_on_submit():
            try:
                repair = RepairOrder(
                    customer_id=customer_id,
                    car_id=car_id,
                    date_in=form.date_in.data,
                    date_out=form.date_out.data,
                    odometer=form.odometer.data,
                    status=form.status.data,
                    symptoms=form.symptoms.data,
                    note=form.note.data
                )
                db.session.add(repair)
                db.session.flush()

                # Add items
                item_types = request.form.getlist('item_type[]')
                item_names = request.form.getlist('item_name[]')
                item_quantities = request.form.getlist('item_quantity[]')
                item_prices = request.form.getlist('item_price[]')
                
                for i_type, name, qty, price in zip(item_types, item_names, item_quantities, item_prices):
                    if name and str(price).strip():
                        item = RepairItem(
                            repair_order_id=repair.id,
                            item_type=i_type,
                            name=name,
                            quantity=int(qty) if qty else 1,
                            unit_price=int(str(price).replace(',', ''))
                        )
                        db.session.add(item)
                
                db.session.commit()
                flash(_("Repair order created successfully!"), "success")
                return redirect(url_for("admin_routes.repairs"))
            except Exception as e:
                db.session.rollback()
                flash(_(f"Error creating repair order: {e}"), "danger")
        elif form.errors:
            for err_code, err_content in form.errors.items():
                for e in err_content:
                    flash(_(f"{err_code}: {e}"), "danger")

    customers = Customer.get_all()
    cars = Car.get_all()
    repair_status = RepairStatus
    from app.utils.constants import RepairItemType
    return render_template(
        "repair_new.html", 
        customers=customers, 
        cars=cars, 
        form=form, 
        repair_status=repair_status,
        item_types=RepairItemType
    )


@routes.route("/repair/<int:repair_id>", methods=["GET", "POST"])
@login_required
def repair_detail(repair_id):
    repair = RepairOrder.get_by_id(repair_id)
    if not repair:
        flash(_("Repair order not found."), "danger")
        return render_template("404.html"), 404

    form = RepairOrderForm(obj=repair)
    
    if request.method == "POST":
        if form.validate_on_submit():
            try:
                form.populate_obj(repair)
                
                # Cập nhật ID (vì form string field sẽ bị mất nếu disable trên UI)
                customer_id = request.form.get("customer_id")
                car_id = request.form.get("car_id")
                if customer_id: repair.customer_id = customer_id
                if car_id: repair.car_id = car_id

                # Clear old items
                for item in repair.items:
                    db.session.delete(item)
                
                # Add new items
                item_types = request.form.getlist('item_type[]')
                item_names = request.form.getlist('item_name[]')
                item_quantities = request.form.getlist('item_quantity[]')
                item_prices = request.form.getlist('item_price[]')
                
                for i_type, name, qty, price in zip(item_types, item_names, item_quantities, item_prices):
                    if name and str(price).strip():
                        item = RepairItem(
                            repair_order_id=repair.id,
                            item_type=i_type,
                            name=name,
                            quantity=int(qty) if qty else 1,
                            unit_price=int(str(price).replace(',', ''))
                        )
                        db.session.add(item)
                
                db.session.commit()
                flash(_("Repair order updated successfully!"), "success")
                return redirect(url_for('admin_routes.repair_detail', repair_id=repair.id))
            except Exception as e:
                db.session.rollback()
                flash(_(f"Error updating repair order: {e}"), "danger")
        elif form.errors:
            for err_code, err_content in form.errors.items():
                for e in err_content:
                    flash(_(f"{err_code}: {e}"), "danger")

    customers = Customer.get_all()
    cars = Car.get_all()
    repair_status = RepairStatus
    from app.utils.constants import RepairItemType
    return render_template(
        "repair_detail.html",
        repair=repair,
        form=form,
        customers=customers,
        cars=cars,
        repair_status=repair_status,
        item_types=RepairItemType
    )


@routes.route("/repair/<int:repair_id>/delete", methods=["GET"])
@login_required
def delete_repair(repair_id):
    repair = RepairOrder.get_by_id(repair_id)
    if not repair:
        flash(_("Repair order not found."), "danger")
        return redirect(url_for("admin_routes.repairs"))

    try:
        db.session.delete(repair)
        db.session.commit()
        flash(_("Repair order deleted successfully!"), "success")
    except Exception as e:
        db.session.rollback()
        flash(_(f"Error deleting repair order: {e}"), "danger")

    return redirect(url_for("admin_routes.repairs"))
