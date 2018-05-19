# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-05-19 04:07
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('customer', '0009_auto_20180518_0350'),
    ]

    operations = [
        migrations.CreateModel(
            name='Deal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deal_name', models.CharField(max_length=120)),
                ('amount', models.DecimalField(blank=True, decimal_places=2, max_digits=50, null=True)),
                ('closing_date', models.DateField()),
                ('stage', models.IntegerField(choices=[(1, 'Prospecting'), (2, 'Opportunity'), (3, 'Investigation'), (4, 'Presentation'), (5, 'Close Won'), (0, 'Close Lost')], default=1)),
            ],
        ),
        migrations.RemoveField(
            model_name='companydetails',
            name='company_owner',
        ),
        migrations.RemoveField(
            model_name='contact',
            name='deal_size',
        ),
        migrations.RemoveField(
            model_name='contact',
            name='stage',
        ),
        migrations.AddField(
            model_name='companydetails',
            name='fax',
            field=models.CharField(blank=True, max_length=120, null=True),
        ),
        migrations.AddField(
            model_name='contact',
            name='contact_owner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='owner', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='contact',
            name='title',
            field=models.CharField(blank=True, max_length=120, null=True),
        ),
        migrations.AddField(
            model_name='task',
            name='priority',
            field=models.IntegerField(choices=[(0, 'Low'), (1, 'Medium'), (2, 'High')], null=True),
        ),
        migrations.AddField(
            model_name='task',
            name='task_owner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='contact',
            name='phone',
            field=models.BigIntegerField(),
        ),
        migrations.AddField(
            model_name='deal',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customer.CompanyDetails'),
        ),
        migrations.AddField(
            model_name='deal',
            name='contact',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='customer.Contact'),
        ),
        migrations.AddField(
            model_name='deal',
            name='deal_owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
