# Generated by Django 5.1.3 on 2024-11-20 14:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('diary', '0002_alter_grade_grade'),
    ]

    operations = [
        migrations.AlterField(
            model_name='grade',
            name='grade',
            field=models.IntegerField(choices=[(2, '2'), (3, '3'), (4, '4'), (5, '5')]),
        ),
    ]
