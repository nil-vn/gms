import os

file_path = "templates/admin/cars.html"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# We will replace the entire <ul class="nav nav-tabs... to </div><!-- end of tab-content -->
# Let's find the start and end by splitting

parts = content.split('<ul class="nav nav-tabs invoice-tab mb-3" id="myTab" role="tablist">')
header_part = parts[0]
remaining = parts[1]

# find the end of tab content. It's right before <div class="col-xxl-8">
parts_end = remaining.split('<div class="col-xxl-8">')
footer_part = '<div class="col-xxl-8">' + parts_end[1]

macro_str = """
{% macro car_table(table_id, car_list) %}
<div class="table-responsive">
    <table class="table table-hover" id="{{ table_id }}">
        <thead>
        <tr>
            <th>{{ _('No.') }}</th>
            <th>{{ _('Name/Model') }}</th>
            <th>{{ _('Branch') }}</th>
            <th>{{ _('Situation') }}</th>
            <th>{{ _('Imported Date') }}</th>
            <th>{{ _('Selling Price') }}</th>
            <th>{{ _('Status') }}</th>
            <th class="text-end">{{ _('Actions') }}</th>
        </tr>
        </thead>
        <tbody>
        {% for car in car_list %}
        <tr>
            <td>{{ loop.index }}</td>
            <td>
                <div class="row align-items-center">
                    <div class="col">
                        <h6 class="mb-1"><a href="{{ url_for('admin_routes.car_detail', car_id=car.id) }}" class="text-truncate w-100">{{ car.name }}</a>
                        </h6>
                    </div>
                </div>
            </td>
            <td>
                <div class="col-auto pe-0">
                    <img src="{{ url_for('static', filename='admin/images/branch/'+ (car.branch|lower if car.branch else 'toyota') +'.svg') }}"
                         alt="{{ car.branch }}" class="wid-40 hei-40 rounded-circle" onerror="this.onerror=null; this.src='{{ url_for('static', filename='admin/images/branch/toyota.svg') }}';"/>
                </div>
            </td>
            <td><span class="badge bg-light-info">{{ car.car_situation or '-' }}</span></td>
            <td>{{ car.imported_date or '-'  }}</td>
            <td>{{ car.selling_price or '-'  }}</td>
            <td><span class="badge bg-light-success">{{ car.status or ''  }}</span></td>
            <td class="text-end">
                <ul class="list-inline mb-0">
                    <li class="list-inline-item"
                    ><a href="{{ url_for('admin_routes.car_detail', car_id=car.id) }}" class="avatar avatar-s btn-link-info btn-pc-default"><i
                            class="ti ti-eye f-20"></i></a
                    ></li>
                    <li class="list-inline-item"
                    ><a href="{{ url_for('admin_routes.delete_car', car_id=car.id) }}" class="avatar avatar-s btn-link-danger btn-pc-default"><i
                            class="ti ti-trash f-20"></i></a
                    ></li>
                </ul>
            </td>
        </tr>
        {% endfor %}
        </tbody>
    </table>
</div>
{% endmacro %}

<ul class="nav nav-tabs invoice-tab mb-3" id="myTab" role="tablist">
    <!-- 1. Tất cả -->
    <li class="nav-item" role="presentation">
        <button class="nav-link active" id="tab-1" data-bs-toggle="tab" data-bs-target="#pane-1" type="button" role="tab" aria-selected="true">
            <span class="d-flex align-items-center gap-2">{{_('All')}} <span class="avatar rounded-circle bg-light-primary">{{ cars|length }}</span></span>
        </button>
    </li>
    <!-- 2. Có sẵn -->
    <li class="nav-item" role="presentation">
        <button class="nav-link" id="tab-2" data-bs-toggle="tab" data-bs-target="#pane-2" type="button" role="tab" aria-selected="false">
            <span class="d-flex align-items-center gap-2">{{_('Available (inc. Awaiting)')}} <span class="avatar rounded-circle bg-light-warning">{{ available_cars|length }}</span></span>
        </button>
    </li>
    <!-- 3. Đang chờ giao -->
    <li class="nav-item" role="presentation">
        <button class="nav-link" id="tab-3" data-bs-toggle="tab" data-bs-target="#pane-3" type="button" role="tab" aria-selected="false">
            <span class="d-flex align-items-center gap-2">{{_('Awaiting Delivery')}} <span class="avatar rounded-circle bg-light-primary">{{ awaiting_delivery_cars|length }}</span></span>
        </button>
    </li>
    <!-- 4. Đã bán -->
    <li class="nav-item" role="presentation">
        <button class="nav-link" id="tab-4" data-bs-toggle="tab" data-bs-target="#pane-4" type="button" role="tab" aria-selected="false">
            <span class="d-flex align-items-center gap-2">{{_('Sold')}} <span class="avatar rounded-circle bg-light-success">{{ sold_cars|length }}</span></span>
        </button>
    </li>
    <!-- 5. Sơn sửa rồi -->
    <li class="nav-item" role="presentation">
        <button class="nav-link" id="tab-5" data-bs-toggle="tab" data-bs-target="#pane-5" type="button" role="tab" aria-selected="false">
            <span class="d-flex align-items-center gap-2">{{_('Refurbished')}} <span class="avatar rounded-circle bg-light-primary">{{ refurbished_cars|length }}</span></span>
        </button>
    </li>
    <!-- 6. Chưa sơn sửa -->
    <li class="nav-item" role="presentation">
        <button class="nav-link" id="tab-6" data-bs-toggle="tab" data-bs-target="#pane-6" type="button" role="tab" aria-selected="false">
            <span class="d-flex align-items-center gap-2">{{_('Not Refurbished')}} <span class="avatar rounded-circle bg-light-danger">{{ not_refurbished_cars|length }}</span></span>
        </button>
    </li>
    <!-- 7. Sơn sửa rồi - chưa vệ sinh -->
    <li class="nav-item" role="presentation">
        <button class="nav-link" id="tab-7" data-bs-toggle="tab" data-bs-target="#pane-7" type="button" role="tab" aria-selected="false">
            <span class="d-flex align-items-center gap-2">{{_('Refurbished/Pending Cleaning')}} <span class="avatar rounded-circle bg-light-warning">{{ refurbished_pending_cleaning_cars|length }}</span></span>
        </button>
    </li>
</ul>

<div class="tab-content" id="myTabContent">
    <div class="tab-pane fade show active" id="pane-1" role="tabpanel" tabindex="0">
        {{ car_table('pc-dt-simple-1', cars) }}
    </div>
    <div class="tab-pane fade" id="pane-2" role="tabpanel" tabindex="0">
        {{ car_table('pc-dt-simple-2', available_cars) }}
    </div>
    <div class="tab-pane fade" id="pane-3" role="tabpanel" tabindex="0">
        {{ car_table('pc-dt-simple-3', awaiting_delivery_cars) }}
    </div>
    <div class="tab-pane fade" id="pane-4" role="tabpanel" tabindex="0">
        {{ car_table('pc-dt-simple-4', sold_cars) }}
    </div>
    <div class="tab-pane fade" id="pane-5" role="tabpanel" tabindex="0">
        {{ car_table('pc-dt-simple-5', refurbished_cars) }}
    </div>
    <div class="tab-pane fade" id="pane-6" role="tabpanel" tabindex="0">
        {{ car_table('pc-dt-simple-6', not_refurbished_cars) }}
    </div>
    <div class="tab-pane fade" id="pane-7" role="tabpanel" tabindex="0">
        {{ car_table('pc-dt-simple-7', refurbished_pending_cleaning_cars) }}
    </div>
</div>
            </div>
        </div>
    </div>
"""

new_content = header_part + macro_str + footer_part

# Need to update the script block for simpleDatatables to initialize all 7 tables
new_content = new_content.replace(
    "['#pc-dt-simple-1', '#pc-dt-simple-2', '#pc-dt-simple-3', '#pc-dt-simple-4']",
    "['#pc-dt-simple-1', '#pc-dt-simple-2', '#pc-dt-simple-3', '#pc-dt-simple-4', '#pc-dt-simple-5', '#pc-dt-simple-6', '#pc-dt-simple-7']"
)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(new_content)
print("Updated cars.html")
