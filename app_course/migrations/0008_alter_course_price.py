# Generated by Django 4.2.4 on 2023-09-14 22:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_course', '0007_alter_lesson_options_course_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='price',
            field=models.PositiveIntegerField(default=1000, verbose_name='Цена курса'),
        ),
    ]
