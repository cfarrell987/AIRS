import pandas
import pandas as pd


def table_clean(in_csv):
    df = pd.read_csv(in_csv)
    df.head(1)
    df.drop(['id', 'eol', 'order_number', 'company', 'rtd_location', 'image', 'last_audit_date', 'next_audit_date',
             'deleted_at', 'expected_checkin', 'purchase_cost', 'checkin_counter', 'checkout_counter',
             'requests_counter', 'user_can_checkout', 'custom_fields', 'model.id', 'status_label.id',
             'status_label.status_type', 'category.id', 'manufacturer.id', 'location.id', 'assigned_to.id',
             'assigned_to.first_name', 'assigned_to.last_name', 'assigned_to.employee_number', 'assigned_to.type',
             'warranty_expires.formatted', 'created_at.datetime', 'created_at.formatted',
             'updated_at.datetime', 'updated_at.formatted', 'purchase_date.formatted', 'last_checkout.datetime',
             'last_checkout.formatted', 'available_actions.checkout', 'available_actions.checkin',
             'available_actions.clone', 'available_actions.restore', 'available_actions.update',
             'available_actions.delete', 'rtd_location.id', 'rtd_location.name', 'last_checkout',
             'location', 'assigned_to',	'supplier.id', 'supplier.name',
             'last_audit_date.datetime', 'last_audit_date.formatted', 'next_audit_date.date',
             'next_audit_date.formatted', 'warranty_expires', 'purchase_date'], inplace=True, axis=1)

    df.to_csv(in_csv, index=False)