# Generated by Django 4.0 on 2023-01-12 12:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('product', '0007_alter_carts_qty'),
    ]

    operations = [
        migrations.CreateModel(
            name='Orders',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('orderdate', models.DateField(auto_now_add=True, null=True)),
                ('status', models.CharField(choices=[('order_placed', 'order_placed'), ('ready_to_ship', 'ready_to_ship'), ('intransit', 'intrasit'), ('delivered', 'delivered')], default='order_placed', max_length=20)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auth.user')),
            ],
        ),
    ]