from django.conf import settings
from django.utils.safestring import mark_safe
from django.core.validators import FileExtensionValidator
from django.db import models



# Create your models here.
class ProductCategory(models.Model):
    category_name = models.CharField(verbose_name="Product Category", max_length=100, unique=True, blank=False, null=False)
    def __str__(self):
        return self.category_name


class Product(models.Model):
    category = models.ForeignKey(ProductCategory, verbose_name="Product Category", related_name="products", on_delete=models.CASCADE)
    product_name = models.CharField(verbose_name="Product", max_length=100, unique=True, blank=False, null=False)
    description = models.TextField(verbose_name="Description", blank=True, null=True)
    price = models.FloatField(verbose_name="Price", default=0.0, null=False)
    color = models.CharField(verbose_name="Color", max_length=50, blank=False, null=False)
    quantity = models.IntegerField(verbose_name="Quantity", default=0.0, null=False)
    def __str__(self):
        return self.product_name


class ProductImage(models.Model):
    product = models.ForeignKey(Product, verbose_name="Product", related_name="product_images", on_delete=models.CASCADE)
    picture = models.ImageField(
        verbose_name="Image",
        upload_to="product/images/",
        validators=[FileExtensionValidator(['png', 'jpg', 'jpeg'])],
        blank=True, null=True
    )
    def image(self):
        return mark_safe('<img src="/../../media/%s" width="80" />' % (self.picture))

    image.allow_tags = True
    def __str__(self):
        return f"{self.product} - {self.picture}"



class Order(models.Model):
    class OrderStatus(models.TextChoices):
        PENDING = "Pending", "Pending"
        PROCESSING = "Processing", "Processing"
        SUCCESS = "Success", "Success"
    client = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="Client", related_name="client_orders", on_delete=models.CASCADE)
    order_number = models.CharField(verbose_name="Order Number", max_length=100, unique=True, blank=False, null=False)
    status = models.CharField(verbose_name="Status", choices=OrderStatus.choices, default=OrderStatus.PENDING, max_length=10)
    shipping_address = models.CharField(verbose_name="Shipping Address", max_length=100, blank=True, null=True)
    total_amount = models.FloatField(verbose_name="Total Amount", default=0.0, null=False)
    payment_method = models.CharField(verbose_name="Payment Method", max_length=10, blank=False, null=False)
    payment_id = models.CharField(verbose_name="Payment ID", max_length=10, blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.order_number} - {self.client.first_name} {self.client.last_name}"

    @classmethod
    def get_pending_waiting_orders(cls):
        return cls.objects.filter(status__in=['Pending', 'Processing'])


class OrderDetail(models.Model):
    order = models.ForeignKey(Order, verbose_name="Order", related_name="order_details", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, verbose_name="Product", on_delete=models.CASCADE)
    quantity = models.IntegerField(verbose_name="Quantity", default=0.0, null=False)
    def __str__(self):
        return f"{self.order.order_number} - {self.product}"



class StockMovement(models.Model):
    class MovementType(models.TextChoices):
        STOCK_IN = "Stock In", "Stock In"
        STOCK_OUT = "Stock Out", "Stock Out"

    product = models.ForeignKey(Product, verbose_name="Product", related_name="stock_movements", on_delete=models.CASCADE)
    movement_type = models.CharField(verbose_name="Movement", choices=MovementType.choices, max_length=10)
    quantity = models.IntegerField(verbose_name="Quantity", default=0, null=False)
    total_price = models.FloatField(verbose_name="Total Price", default=0.0, null=False)
    processed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    date_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product} - {self.movement_type} - {self.quantity}"

    def save(self, *args, **kwargs):
        # Update the product quantity based on the stock movement
        if self.movement_type == 'Stock In':
            self.product.quantity += self.quantity
        elif self.movement_type == 'Stock Out':
            self.product.quantity -= self.quantity

        # Calculate and update the total price based on the quantity and any other relevant data
        self.total_price = self.product.price * self.quantity

        # Save the StockMovement instance and update the related ProductDetail
        super().save(*args, **kwargs)
        self.product.save()
