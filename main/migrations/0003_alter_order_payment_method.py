# Generated by Django 4.2.3 on 2023-08-31 22:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_alter_orderdetail_quantity_alter_product_quantity_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='payment_method',
            field=models.CharField(max_length=50, verbose_name='Payment Method'),
        ),
    ]