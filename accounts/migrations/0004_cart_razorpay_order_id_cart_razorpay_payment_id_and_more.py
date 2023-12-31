# Generated by Django 4.2.6 on 2024-01-01 15:03

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0003_cart_coupon"),
    ]

    operations = [
        migrations.AddField(
            model_name="cart",
            name="razorpay_order_id",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name="cart",
            name="razorpay_payment_id",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name="cart",
            name="razorpay_payment_signature",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
