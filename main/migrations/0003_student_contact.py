# Generated by Django 4.2.4 on 2023-08-27 18:26

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("main", "0002_alter_student_card_issue_date_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="student",
            name="contact",
            field=models.CharField(max_length=20, null=True),
        ),
    ]