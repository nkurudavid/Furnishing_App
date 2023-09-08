from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.http import HttpRequest
from main.models import Product, Order, StockMovement
from decimal import Decimal


# Signal handler for new product creation (stock in)
@receiver(post_save, sender=Product)
def product_created(sender, instance, created, **kwargs):
    if created:
        StockMovement.objects.create(
            product=instance,
            movement_type=StockMovement.MovementType.STOCK_IN,
            quantity=instance.quantity,
            total_price=instance.price * instance.quantity,
            processed_by=_get_request_user()  # Set this to None for new product creation
        )



# Signal handler for order status change to "Success" (stock out)
@receiver(pre_save, sender=Order)
def order_status_change(sender, instance, **kwargs):
    if instance.pk:  # Check if the order already exists (not a new order)
        original_order = Order.objects.get(pk=instance.pk)
        if (
            original_order.status != Order.OrderStatus.SUCCESS
            and instance.status == Order.OrderStatus.SUCCESS
        ):
            for order_detail in instance.order_details.all():
                product = order_detail.product
                quantity = order_detail.quantity

                # Check if there is sufficient quantity in stock
                if product.quantity >= quantity:
                    # Stock out
                    StockMovement.objects.create(
                        product=product,
                        movement_type=StockMovement.MovementType.STOCK_OUT,
                        quantity=quantity,
                        total_price=product.price * quantity,
                        processed_by=None  # Get the user from the request
                    )

                    # Update product quantity (stock reduction)
                    product.quantity -= quantity
                    product.save()
                else:
                    # Insufficient stock, handle this case as needed
                    pass  # You may raise an exception or log the issue here



# Signal handler for product quantity change (stock in or stock out)
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
            movement_type = (
                StockMovement.MovementType.STOCK_IN
                if quantity_change > 0
                else StockMovement.MovementType.STOCK_OUT
            )
            quantity_change = abs(quantity_change)  # Ensure quantity change is positive

            # Stock movement
            StockMovement.objects.create(
                product=instance,
                movement_type=movement_type,
                quantity=quantity_change,
                total_price=Decimal(instance.price) * quantity_change,
                processed_by=None  # Set this to the user who made the change if applicable
            )



# Helper function to get the user from the request
def _get_request_user():
    request = HttpRequest()
    return request.user
