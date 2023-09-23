# Generated by Django 4.2.5 on 2023-09-23 08:54

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_number', models.CharField(max_length=100, unique=True, verbose_name='Order Number')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('quantity', models.IntegerField(default=0, verbose_name='Quantity')),
                ('status', models.CharField(choices=[('Pending', 'Pending'), ('Processing', 'Processing'), ('Completed', 'Completed'), ('Cancelled', 'Cancelled')], default='Pending', max_length=20, verbose_name='Status')),
                ('picture', models.ImageField(blank=True, null=True, upload_to='custom_orders/images/', validators=[django.core.validators.FileExtensionValidator(['png', 'jpg', 'jpeg'])], verbose_name='Design Image')),
                ('payment_amount', models.FloatField(blank=True, default=0.0, null=True, verbose_name='Total Amount')),
                ('payment_method', models.CharField(blank=True, max_length=50, null=True, verbose_name='Payment Method')),
                ('payment_id', models.CharField(blank=True, max_length=10, null=True, verbose_name='Payment ID')),
                ('payment_date', models.DateTimeField()),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='custom_orders', to=settings.AUTH_USER_MODEL, verbose_name='Client')),
            ],
        ),
        migrations.CreateModel(
            name='Material',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='Material Name')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('picture', models.ImageField(blank=True, null=True, upload_to='material/images/', validators=[django.core.validators.FileExtensionValidator(['png', 'jpg', 'jpeg'])], verbose_name='Image')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_number', models.CharField(max_length=100, unique=True, verbose_name='Order Number')),
                ('status', models.CharField(choices=[('Pending', 'Pending'), ('Processing', 'Processing'), ('Success', 'Success')], default='Pending', max_length=10, verbose_name='Status')),
                ('shipping_address', models.CharField(blank=True, max_length=100, null=True, verbose_name='Shipping Address')),
                ('total_amount', models.FloatField(default=0.0, verbose_name='Total Amount')),
                ('payment_method', models.CharField(max_length=50, verbose_name='Payment Method')),
                ('payment_id', models.CharField(blank=True, max_length=10, null=True, verbose_name='Payment ID')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='client_orders', to=settings.AUTH_USER_MODEL, verbose_name='Client')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(max_length=100, verbose_name='Product')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('price', models.FloatField(default=0.0, verbose_name='Price')),
                ('color', models.CharField(max_length=50, verbose_name='Color')),
                ('quantity', models.IntegerField(default=0.0, verbose_name='Quantity')),
            ],
        ),
        migrations.CreateModel(
            name='ProductCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(max_length=100, unique=True, verbose_name='Product Category')),
            ],
        ),
        migrations.CreateModel(
            name='StockMovement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('movement_type', models.CharField(choices=[('Stock In', 'Stock In'), ('Stock Out', 'Stock Out')], max_length=10, verbose_name='Movement')),
                ('quantity', models.IntegerField(default=0, verbose_name='Quantity')),
                ('total_price', models.FloatField(default=0.0, verbose_name='Total Price')),
                ('date_time', models.DateTimeField(auto_now_add=True)),
                ('processed_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stock_movements', to='main.product', verbose_name='Product')),
            ],
        ),
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('picture', models.ImageField(blank=True, null=True, upload_to='product/images/', validators=[django.core.validators.FileExtensionValidator(['png', 'jpg', 'jpeg'])], verbose_name='Image')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_images', to='main.product', verbose_name='Product')),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='main.productcategory', verbose_name='Product Category'),
        ),
        migrations.CreateModel(
            name='Pro_forma',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('Doable', 'Doable'), ('Undoable', 'Undoable')], max_length=20, verbose_name='Status')),
                ('payment_amount', models.FloatField(default=0.0, verbose_name='Payment Amount')),
                ('processing_period', models.IntegerField(default=0, verbose_name='Processing Period (Days)')),
                ('client_reaction', models.CharField(choices=[('Pending', 'Pending'), ('Accepted', 'Accepted'), ('Declined', 'Declined'), ('None', 'None')], default='Pending', max_length=20, verbose_name='Client Reaction')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('custom_order', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='feedbacks', to='main.customorder', verbose_name='Custom Order')),
                ('processed_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='OrderDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=0.0, verbose_name='Quantity')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_details', to='main.order', verbose_name='Order')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.product', verbose_name='Product')),
            ],
        ),
        migrations.AddField(
            model_name='customorder',
            name='material',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='custom_orders', to='main.material', verbose_name='Product Material'),
        ),
        migrations.AddField(
            model_name='customorder',
            name='processed_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]
