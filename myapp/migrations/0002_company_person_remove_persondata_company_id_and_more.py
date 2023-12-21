# Generated by Django 4.2.3 on 2023-12-15 05:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("myapp", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Company",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("company_id", models.IntegerField(unique=True)),
            ],
        ),
        migrations.CreateModel(
            name="Person",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255, unique=True)),
            ],
        ),
        migrations.RemoveField(
            model_name="persondata",
            name="company_id",
        ),
        migrations.RemoveField(
            model_name="persondata",
            name="face_recognition",
        ),
        migrations.AddField(
            model_name="persondata",
            name="company",
            field=models.ForeignKey(
                default=1.2,
                on_delete=django.db.models.deletion.CASCADE,
                to="myapp.company",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="persondata",
            name="person",
            field=models.ForeignKey(
                default=1.7,
                on_delete=django.db.models.deletion.CASCADE,
                to="myapp.person",
            ),
            preserve_default=False,
        ),
    ]
