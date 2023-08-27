# Generated by Django 4.2.4 on 2023-08-26 23:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_account_future_value'),
    ]

    operations = [
        migrations.CreateModel(
            name='Money',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.AlterField(
            model_name='account',
            name='future_value',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='account',
            name='value',
            field=models.FloatField(null=True),
        ),
    ]
