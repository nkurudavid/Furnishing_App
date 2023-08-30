from django import template
from django.urls import reverse
from django.utils.html import escape
from django.utils.safestring import mark_safe
from django.template.defaultfilters import date  # Add this import
from main.models import Order

register = template.Library()

@register.simple_tag
def new_order_notification_link(user):
    if user.is_manager:
        pending_waiting_orders = Order.get_pending_waiting_orders()
        new_order_count = pending_waiting_orders.count()
        url = reverse('admin:main_order_changelist') + "?status__in=Pending,Processing"
        link = f'<a href="{url}" class="historylink" style="background-color: #ffa500; color: #FFFFFF; padding: 5px 20px;"><b>New Orders: ( {new_order_count} )</b></a>'
        return mark_safe(link)
    return ''  # Return an empty string if not a manager


@register.simple_tag
def new_order_table(user):
    if user.is_manager:
        pending_waiting_orders = Order.get_pending_waiting_orders()
        table_html = '<table style="width:100%; background:white">'
        table_html += '<tr style="background: orange"><th>Order ID</th><th>CLIENT</th><th>PAYMENT METHORD</th><th>AMOUNT</th><th>STATUS</th><th>DATE CREATED</th></tr>'
        for order in pending_waiting_orders:
            order_url = reverse('admin:main_order_change', args=[order.id])
            order_url = escape(order_url)
            table_html += f'<tr><td><a href="{order_url}">#{order.order_number}</a></td><td>{order.client}</td><td>{order.payment_method}</td><td>{order.total_amount}</td><td>{order.status}</td><td>{date(order.created_date, "Y-m-d H:i")}</td></tr>'
        table_html += '</table>'
        return mark_safe(table_html)
    return ''  # Return an empty string if not a manager