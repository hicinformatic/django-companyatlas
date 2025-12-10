# Generated migration for companyatlas

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Company",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                (
                    "domain",
                    models.CharField(
                        help_text="Company domain (e.g., example.com)", max_length=255, unique=True
                    ),
                ),
                (
                    "siren",
                    models.CharField(
                        blank=True, help_text="French SIREN number", max_length=20, null=True
                    ),
                ),
                (
                    "vat_number",
                    models.CharField(
                        blank=True,
                        help_text="VAT/Tax identification number",
                        max_length=50,
                        null=True,
                    ),
                ),
                (
                    "stock_symbol",
                    models.CharField(
                        blank=True, help_text="Stock ticker symbol", max_length=10, null=True
                    ),
                ),
                ("name", models.CharField(help_text="Company name", max_length=255)),
                (
                    "legal_name",
                    models.CharField(blank=True, help_text="Legal/registered name", max_length=255),
                ),
                ("description", models.TextField(blank=True, help_text="Company description")),
                (
                    "founded_year",
                    models.IntegerField(blank=True, help_text="Year founded", null=True),
                ),
                (
                    "employee_count",
                    models.IntegerField(blank=True, help_text="Number of employees", null=True),
                ),
                (
                    "industry",
                    models.CharField(blank=True, help_text="Industry/sector", max_length=100),
                ),
                ("website", models.URLField(blank=True, help_text="Company website")),
                (
                    "country",
                    models.CharField(blank=True, help_text="ISO country code", max_length=2),
                ),
                ("city", models.CharField(blank=True, help_text="City", max_length=100)),
                ("address", models.TextField(blank=True, help_text="Full address")),
                (
                    "is_enriched",
                    models.BooleanField(
                        default=False, help_text="Whether company data has been enriched"
                    ),
                ),
                (
                    "enriched_at",
                    models.DateTimeField(
                        blank=True, help_text="Last enrichment timestamp", null=True
                    ),
                ),
                (
                    "enrichment_data",
                    models.JSONField(blank=True, default=dict, help_text="Raw enrichment data"),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "verbose_name": "Company",
                "verbose_name_plural": "Companies",
                "ordering": ["-created_at"],
            },
        ),
        migrations.AddIndex(
            model_name="company",
            index=models.Index(fields=["domain"], name="companyatla_domain_idx"),
        ),
        migrations.AddIndex(
            model_name="company",
            index=models.Index(fields=["siren"], name="companyatla_siren_idx"),
        ),
        migrations.AddIndex(
            model_name="company",
            index=models.Index(fields=["vat_number"], name="companyatla_vat_num_idx"),
        ),
        migrations.AddIndex(
            model_name="company",
            index=models.Index(fields=["-created_at"], name="companyatla_created_idx"),
        ),
    ]
