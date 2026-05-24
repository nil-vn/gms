from datetime import datetime
from types import SimpleNamespace
from flask_babel import lazy_gettext as _

from app.admin.models import Customer, Transaction, Car


def get_all_customers():
    customers = Customer.get_all()
    return customers

def get_recently_count(model):
    now = datetime.utcnow()
    # tháng hiện tại
    start_current_month = datetime(now.year, now.month, 1)
    # tháng trước
    if now.month == 1:
        start_prev_month = datetime(now.year - 1, 12, 1)
    else:
        start_prev_month = datetime(now.year, now.month - 1, 1)

    # số user tháng hiện tại
    current_count = model.current_count(start_current_month)

    # số user tháng trước
    prev_count = model.prev_count(start_current_month, start_prev_month)

    # tính % tăng trưởng
    growth_rate = 0
    if prev_count > 0:
        growth_rate = ((current_count - prev_count) / prev_count) * 100

    return SimpleNamespace(
        total=current_count,
        monthly_increase=round(growth_rate, 2)
    )


def get_revenue_last_6_months():
    now = datetime.utcnow()
    results = []
    # from current month back to 5 months ago
    for i in range(5, -1, -1):
        # calculate year and month
        y = now.year
        m = now.month - i
        while m <= 0:
            m += 12
            y -= 1
            
        start_date = datetime(y, m, 1)
        if m == 12:
            end_date = datetime(y + 1, 1, 1)
        else:
            end_date = datetime(y, m + 1, 1)
            
        # Get transactions in this month
        transactions = Transaction.query.filter(
            Transaction.created_at >= start_date,
            Transaction.created_at < end_date
        ).all()
        
        month_revenue = sum(t.total_amount for t in transactions if getattr(t, 'total_amount', None))
        results.append({
            "month": f"{m:02d}/{y}",
            "revenue": month_revenue
        })
    return results

def get_car_status_stats():
    cars = Car.get_all()
    stats = {}
    for car in cars:
        status = car.situation_label if car.car_situation else _('Unknown')
        if status not in stats:
            stats[status] = 0
        stats[status] += 1
    
    # Format for chart
    labels = list(stats.keys())
    series = list(stats.values())
    return {
        "labels": labels,
        "series": series
    }

def get_metrics():
    return SimpleNamespace(
        customers=get_recently_count(Customer),
        transactions=get_recently_count(Transaction),
        cars=get_recently_count(Car),
        revenue_6_months=get_revenue_last_6_months(),
        car_stats=get_car_status_stats()
    )


def get_revenue_by_range(range_type: str = "6m"):
    from datetime import timedelta
    now = datetime.utcnow()
    results = []

    if range_type == "1m":
        # Last 30 days (daily)
        for i in range(29, -1, -1):
            day_start = (now - timedelta(days=i)).replace(hour=0, minute=0, second=0, microsecond=0)
            day_end = day_start + timedelta(days=1)

            transactions = Transaction.query.filter(
                Transaction.created_at >= day_start,
                Transaction.created_at < day_end
            ).all()

            revenue = sum(t.total_amount for t in transactions if getattr(t, 'total_amount', None))
            results.append({
                "label": day_start.strftime("%d/%m"),
                "revenue": revenue
            })

    elif range_type == "3m":
        # Last 12 weeks (weekly)
        today_midnight = now.replace(hour=0, minute=0, second=0, microsecond=0)
        for i in range(11, -1, -1):
            week_start = today_midnight - timedelta(days=(i+1)*7 - 1)
            week_end = week_start + timedelta(days=7)

            transactions = Transaction.query.filter(
                Transaction.created_at >= week_start,
                Transaction.created_at < week_end
            ).all()

            revenue = sum(t.total_amount for t in transactions if getattr(t, 'total_amount', None))
            results.append({
                "label": f"{week_start.strftime('%d/%m')}-{(week_end - timedelta(days=1)).strftime('%d/%m')}",
                "revenue": revenue
            })

    elif range_type == "1y":
        # Last 12 months (monthly)
        for i in range(11, -1, -1):
            y = now.year
            m = now.month - i
            while m <= 0:
                m += 12
                y -= 1

            start_date = datetime(y, m, 1)
            if m == 12:
                end_date = datetime(y + 1, 1, 1)
            else:
                end_date = datetime(y, m + 1, 1)

            transactions = Transaction.query.filter(
                Transaction.created_at >= start_date,
                Transaction.created_at < end_date
            ).all()

            revenue = sum(t.total_amount for t in transactions if getattr(t, 'total_amount', None))
            results.append({
                "label": f"{m:02d}/{y}",
                "revenue": revenue
            })

    else:  # "6m"
        # Last 6 months (monthly)
        for i in range(5, -1, -1):
            y = now.year
            m = now.month - i
            while m <= 0:
                m += 12
                y -= 1

            start_date = datetime(y, m, 1)
            if m == 12:
                end_date = datetime(y + 1, 1, 1)
            else:
                end_date = datetime(y, m + 1, 1)

            transactions = Transaction.query.filter(
                Transaction.created_at >= start_date,
                Transaction.created_at < end_date
            ).all()

            revenue = sum(t.total_amount for t in transactions if getattr(t, 'total_amount', None))
            results.append({
                "label": f"{m:02d}/{y}",
                "revenue": revenue
            })

    return results