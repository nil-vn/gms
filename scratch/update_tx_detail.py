import os

file_path = "templates/admin/transaction_detail.html"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Add deposit_amount after selling_price
deposit_html = """
                        <div class="col-md-6">
                            <div class="mb-3">
                                <label class="form-label" for="deposit_amount">{{ _('Deposit Amount') }}</label>
                                <input id="deposit_amount" name="deposit_amount" type="text"
                                       class="form-control" value="{{ transaction.deposit_amount or '' }}"/>
                            </div>
                        </div>
"""

content = content.replace(
    """<label class="form-label" for="selling_price">{{ _('Unit Price') }}</label>
                                <input id="selling_price" name="selling_price" type="text"
                                       class="form-control" value="{{ transaction.selling_price or '' }}"/>
                            </div>
                        </div>""",
    """<label class="form-label" for="selling_price">{{ _('Selling Price') }}</label>
                                <input id="selling_price" name="selling_price" type="text"
                                       class="form-control" value="{{ transaction.selling_price or '' }}"/>
                            </div>
                        </div>""" + deposit_html
)


# Add other_transactions table after note
other_tx_html = """
                        <div class="col-md-12 mt-4">
                            <h6>{{ _('Other Transactions (Accessories/Services)') }}</h6>
                            <div class="table-responsive">
                                <table class="table table-bordered" id="other-tx-table">
                                    <thead>
                                        <tr>
                                            <th>{{ _('Accessory/Service Name') }}</th>
                                            <th>{{ _('Price') }}</th>
                                            <th style="width: 50px;"></th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        {% if transaction.items %}
                                            {% for item in transaction.items %}
                                            <tr>
                                                <td><input type="text" name="item_name[]" class="form-control" value="{{ item.name }}" placeholder="e.g. Dashcam"></td>
                                                <td><input type="number" name="item_price[]" class="form-control" value="{{ item.price }}" placeholder="e.g. 1500000"></td>
                                                <td><button type="button" class="btn btn-sm btn-danger remove-row-btn"><i class="ti ti-trash"></i></button></td>
                                            </tr>
                                            {% endfor %}
                                        {% else %}
                                            <tr>
                                                <td><input type="text" name="item_name[]" class="form-control" placeholder="e.g. Dashcam"></td>
                                                <td><input type="number" name="item_price[]" class="form-control" placeholder="e.g. 1500000"></td>
                                                <td><button type="button" class="btn btn-sm btn-danger remove-row-btn"><i class="ti ti-trash"></i></button></td>
                                            </tr>
                                        {% endif %}
                                    </tbody>
                                </table>
                                <button type="button" class="btn btn-sm btn-primary" id="add-row-btn">+ {{ _('Add Item') }}</button>
                            </div>
                        </div>
"""

content = content.replace(
    """</textarea>
                            </div>
                        </div>
                    </div>""",
    """</textarea>
                            </div>
                        </div>""" + other_tx_html + """
                    </div>"""
)

# Add JS dynamically
js_html = """
    document.getElementById('add-row-btn').addEventListener('click', function() {
        var tbody = document.querySelector('#other-tx-table tbody');
        var tr = document.createElement('tr');
        tr.innerHTML = '<td><input type="text" name="item_name[]" class="form-control" placeholder="e.g. Dashcam"></td>' +
                       '<td><input type="number" name="item_price[]" class="form-control" placeholder="e.g. 1500000"></td>' +
                       '<td><button type="button" class="btn btn-sm btn-danger remove-row-btn"><i class="ti ti-trash"></i></button></td>';
        tbody.appendChild(tr);
    });
    document.addEventListener('click', function(e) {
        if(e.target && (e.target.matches('.remove-row-btn') || e.target.closest('.remove-row-btn'))) {
            var btn = e.target.matches('.remove-row-btn') ? e.target : e.target.closest('.remove-row-btn');
            btn.closest('tr').remove();
        }
    });
"""

content = content.replace(
    """<script>
    // datetime pickers""",
    """<script>
""" + js_html + """
    // datetime pickers"""
)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)

print(f"Updated {file_path}")
