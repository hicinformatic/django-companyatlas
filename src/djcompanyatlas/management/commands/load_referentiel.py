import csv
from pathlib import Path

from django.core.management.base import BaseCommand

from djcompanyatlas.models import Referentiel


class Command(BaseCommand):
    help = "Load Referentiel data from CSV file"

    def add_arguments(self, parser):
        parser.add_argument(
            "--csv",
            type=str,
            help="Path to CSV file (defaults to governance_sources.csv in data_sources)",
        )
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Clear existing Referentiel data before loading",
        )
        parser.add_argument(
            "--usage-type",
            type=str,
            choices=["description", "configuration", "characteristics"],
            help="Usage type for all loaded records (overridden by CSV column if present)",
        )

    def handle(self, *args, **options):
        # Determine CSV path
        if options["csv"]:
            csv_path = Path(options["csv"])
        else:
            # Default path
            csv_path = (
                Path(__file__).parent.parent.parent / "data_sources" / "governance_sources.csv"
            )

        if not csv_path.exists():
            self.stdout.write(
                self.style.ERROR(f"CSV file not found: {csv_path}")
            )
            return

        # Clear existing data if requested
        if options["clear"]:
            count = Referentiel.objects.count()
            Referentiel.objects.all().delete()
            self.stdout.write(
                self.style.WARNING(f"Deleted {count} existing Referentiel records")
            )

        # Load CSV
        created_count = 0
        updated_count = 0

        with open(csv_path, encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)

            for row in reader:
                # Skip empty rows
                if not row.get("code"):
                    continue

                # Prepare data
                data = {
                    "category": row.get("category", ""),
                    "description": row.get("description", ""),
                    "characteristics": row.get("characteristics", ""),
                    "priority": int(row.get("priority", 0)),
                }

                # Handle usage_type: CSV column takes priority over CLI argument
                if row.get("usage_type"):
                    data["usage_type"] = row["usage_type"]
                elif options.get("usage_type"):
                    data["usage_type"] = options["usage_type"]

                # Store name in metadata if present
                if row.get("name"):
                    data["metadata"] = {"name": row["name"]}

                # Create or update
                obj, created = Referentiel.objects.update_or_create(
                    code=row["code"],
                    defaults=data,
                )

                if created:
                    created_count += 1
                    self.stdout.write(
                        self.style.SUCCESS(f"Created: {row['code']}")
                    )
                else:
                    updated_count += 1
                    self.stdout.write(
                        self.style.SUCCESS(f"Updated: {row['code']}")
                    )

        self.stdout.write(
            self.style.SUCCESS(
                f"\nCompleted: {created_count} created, {updated_count} updated"
            )
        )
