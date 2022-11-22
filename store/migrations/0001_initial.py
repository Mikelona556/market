# Generated by Django 4.1.2 on 2022-11-01 09:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('home', '0004_alter_contact_options_product_slug_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title_g', models.CharField(max_length=30)),
                ('price', models.FloatField()),
                ('quantity', models.IntegerField()),
                ('amount', models.IntegerField(blank=True, null=True)),
                ('paid', models.BooleanField()),
                ('order_on', models.CharField(max_length=60)),
                ('payment_date', models.DateTimeField(auto_now_add=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Cart',
                'verbose_name_plural': 'Carts',
                'db_table': 'cart',
                'managed': True,
            },
        ),
    ]