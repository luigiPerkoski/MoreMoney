# Generated by Django 4.2.4 on 2023-08-26 23:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_money_alter_account_future_value_alter_account_value'),
    ]

    operations = [
        migrations.AddField(
            model_name='money',
            name='name',
            field=models.CharField(default=0, max_length=50),
            preserve_default=False,
        ),
    ]
