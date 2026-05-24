import os

file_path = "templates/admin/transactions.html"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

parts = content.split('<ul class="nav nav-tabs invoice-tab mb-3" id="myTab" role="tablist">')
header_part = parts[0]
remaining = parts[1]

# find the end of tab content. It's right before <div class="col-xxl-8">
parts_end = remaining.split('<div class="col-xxl-8">')
footer_part = '<div class="col-xxl-8">' + parts_end[1]

macro_str = """
{% macro transaction_table(table_id, tx_list) %}
<div class="table-responsive">
    <table class="table table-hover" id="{{ table_id }}">
        <thead>
        <tr>
            <th>{{ _('No.') }}</th>
            <th>{{ _('Customer Name') }}</th>
            <th>{{ _('Car Name') }}</th>
            <th>{{ _('Purchase Date') }}</th>
            <th>{{ _('Selling Price') }}</th>
            <th>{{ _('Deposit') }}</th>
            <th>{{ _('Other Transaction') }}</th>
            <th>{{ _('Total Amount') }}</th>
            <th>{{ _('Status') }}</th>
            <th class="text-end">{{ _('Actions') }}</th>
        </tr>
        </thead>
        <tbody>
        {% for transaction in tx_list %}
            {% for car in transaction.cars %}
            <tr>
                <td>{{ loop.index }}</td>
                <td>
                    <div class="row align-items-center">
                        <div class="col">
                            <h6 class="mb-1"><a href="{{ url_for('admin_routes.customer_detail', customer_id=transaction.customer.id) }}" class="text-truncate w-100">{{ transaction.customer.name }}</a></h6>
                        </div>
                    </div>
                </td>
                <td>
                    <div class="row align-items-center">
                        <div class="col">
                            <h6 class="mb-1"><a href="{{ url_for('admin_routes.car_detail', car_id=car.id) }}" class="text-truncate w-100">{{ car.name }}</a></h6>
                        </div>
                    </div>
                </td>
                <td>{{ transaction.purchase_date or '-' }}</td>
                <td>{{ "{:,.0f}".format(transaction.selling_price) if transaction.selling_price else '-' }}</td>
                <td>
                    {% if transaction.status == 'Đã thanh toán' or transaction.status == 'Paid' %}
                        -
                    {% else %}
                        {{ "{:,.0f}".format(transaction.deposit_amount) if transaction.deposit_amount else '-' }}
                    {% endif %}
                </td>
                <td>{{ "{:,.0f}".format(transaction.total_other_amount) if transaction.total_other_amount else '-' }}</td>
                <td><b>{{ "{:,.0f}".format(transaction.total_amount) if transaction.total_amount else '-' }}</b></td>
                <td><span class="badge bg-light-success">{{ transaction.status or '' }}</span></td>
                <td class="text-end">
                    <ul class="list-inline mb-0">
                        <li class="list-inline-item"><a href="{{ url_for('admin_routes.transaction_detail', transaction_id=transaction.id) }}" class="avatar avatar-s btn-link-info btn-pc-default"><i class="ti ti-eye f-20"></i></a></li>
                        <li class="list-inline-item"><a href="{{ url_for('admin_routes.delete_transaction', transaction_id=transaction.id) }}" class="avatar avatar-s btn-link-danger btn-pc-default"><i class="ti ti-trash f-20"></i></a></li>
                    </ul>
                </td>
            </tr>
            {% endfor %}
        {% endfor %}
        </tbody>
    </table>
</div>
{% endmacro %}

<ul class="nav nav-tabs invoice-tab mb-3" id="myTab" role="tablist">
    <li class="nav-item" role="presentation">
        <button class="nav-link active" id="tab-1" data-bs-toggle="tab" data-bs-target="#pane-1" type="button" role="tab" aria-selected="true">
            <span class="d-flex align-items-center gap-2">{{_('All')}} <span class="avatar rounded-circle bg-light-primary">{{ transactions|length }}</span></span>
        </button>
    </li>
    <li class="nav-item" role="presentation">
        <button class="nav-link" id="tab-2" data-bs-toggle="tab" data-bs-target="#pane-2" type="button" role="tab" aria-selected="false">
            <span class="d-flex align-items-center gap-2">{{_('Deposited')}} <span class="avatar rounded-circle bg-light-warning">{{ deposited_transactions|length }}</span></span>
        </button>
    </li>
    <li class="nav-item" role="presentation">
        <button class="nav-link" id="tab-3" data-bs-toggle="tab" data-bs-target="#pane-3" type="button" role="tab" aria-selected="false">
            <span class="d-flex align-items-center gap-2">{{_('Paid')}} <span class="avatar rounded-circle bg-light-success">{{ paid_transactions|length }}</span></span>
        </button>
    </li>
</ul>

<div class="tab-content" id="myTabContent">
    <div class="tab-pane fade show active" id="pane-1" role="tabpanel" tabindex="0">
        {{ transaction_table('pc-dt-simple-1', transactions) }}
    </div>
    <div class="tab-pane fade" id="pane-2" role="tabpanel" tabindex="0">
        {{ transaction_table('pc-dt-simple-2', deposited_transactions) }}
    </div>
    <div class="tab-pane fade" id="pane-3" role="tabpanel" tabindex="0">
        {{ transaction_table('pc-dt-simple-3', paid_transactions) }}
    </div>
</div>
            </div>
        </div>
    </div>
"""

new_content = header_part + macro_str + footer_part

# Need to update the script block for simpleDatatables to initialize all 3 tables
new_content = new_content.replace(
    "['#pc-dt-simple-1', '#pc-dt-simple-2', '#pc-dt-simple-3', '#pc-dt-simple-4']",
    "['#pc-dt-simple-1', '#pc-dt-simple-2', '#pc-dt-simple-3']"
)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(new_content)
