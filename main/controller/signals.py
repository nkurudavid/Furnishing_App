from django.db.models.signals import post_save, pre_save
from django.core.mail import send_mail
from django.conf import settings
from django.dispatch import receiver
from django.core.exceptions import ValidationError

from main.models import Product, Order, StockMovement

# Signal handler for new Product creation (stock in)


@receiver(post_save, sender=Product)
def product_created(sender, instance, created, **kwargs):
    if created:
        # If a new Product instance is created, record a Stock In movement
        StockMovement.objects.create(
            product=instance,
            movement_type=StockMovement.MovementType.STOCK_IN,
            quantity=instance.quantity,
            total_price=instance.price * instance.quantity,
            processed_by=None  # Set the processed_by user as needed
        )


@receiver(pre_save, sender=Order)
def order_status_change(sender, instance, **kwargs):
    if instance.pk:  # Check if the order already exists (not a new order)
        original_order = Order.objects.get(pk=instance.pk)
        if (
            original_order.status != Order.OrderStatus.SUCCESS
            and instance.status == Order.OrderStatus.SUCCESS
        ):
            # Get the client's email from the order
            client_email = instance.client.email
            client_name = instance.client.first_name + " " + instance.client.last_name

            # Compose the email message
            subject = 'Your Order Has Been Delivered Successfully'
            message = f'Hello {client_name},\n\n'
            message += f'Furnishing Order System.\n'
            message += f'Your order with order number #{instance.order_number} has been delivered successfully.\n\n'

            # Include order details
            message += 'Order Details:\n'
            for order_detail in instance.order_details.all():
                product = order_detail.product
                quantity = order_detail.quantity
                subtotal = quantity * order_detail.product.price

                message += f'- Product: {product.product_name}\n'
                message += f'  Quantity: {quantity} meters\n'
                message += f'  Subtotal: Frw {subtotal:.2f}\n\n'

            message += f'Total Amount: Frw {instance.total_amount:.2f}\n\n'
            message += 'Thank you for shopping with us!\n\n'
            message += 'Best regards,\n'

            # Send email notification to the client
            from_email = settings.EMAIL_HOST_USER  # Use your email here
            recipient_list = [client_email]
            send_mail(subject, message, from_email,
                      recipient_list, fail_silently=False)

            # Update stock quantity for products related to this order
            for order_detail in instance.order_details.all():
                prod_data = order_detail.product
                quantity = order_detail.quantity

                # Check if there is sufficient quantity in stock
                if prod_data.quantity >= quantity:
                    # Update product quantity (stock reduction)
                    prod_data.quantity -= quantity
                    prod_data.save()
                else:
                    # Insufficient stock
                    raise ValidationError(
                        f"Insufficient stock for {prod_data} - Requested: {quantity}, Available: {prod_data.quantity}")


# Signal handler for Product quantity change (stock in or stock out)
@receiver(pre_save, sender=Product)
def product_quantity_change(sender, instance, **kwargs):
    try:
        original_product = Product.objects.get(pk=instance.pk)
    except Product.DoesNotExist:
        original_product = None

    if original_product is not None:
        # Calculate the quantity change
        quantity_change = instance.quantity - original_product.quantity

        if quantity_change != 0:
            # Check if this change is related to an order
            if hasattr(instance, 'order_details'):
                # This change is related to an order, skip stock movement recording
                return

            movement_type = (
                StockMovement.MovementType.STOCK_IN
                if quantity_change > 0
                else StockMovement.MovementType.STOCK_OUT
            )
            # Ensure quantity change is positive
            quantity_change = abs(quantity_change)

            # Stock movement
            StockMovement.objects.create(
                product=instance,
                movement_type=movement_type,
                quantity=quantity_change,
                total_price=instance.price * quantity_change,
                processed_by=None,  # Set this to the user who made the change if applicable
            )
