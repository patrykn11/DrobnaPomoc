from decimal import Decimal

from django.db import migrations

CATEGORIES = [
    {
        "name": "Hydraulika",
        "min_price": Decimal("100.00"),
        "max_price": Decimal("400.00"),
    },
    {
        "name": "Elektryka",
        "min_price": Decimal("100.00"),
        "max_price": Decimal("400.00"),
    },
    {
        "name": "Drobne naprawy",
        "min_price": Decimal("50.00"),
        "max_price": Decimal("250.00"),
    },
    {
        "name": "Sprzątanie",
        "min_price": Decimal("80.00"),
        "max_price": Decimal("300.00"),
    },
    {
        "name": "Zakupy",
        "min_price": Decimal("20.00"),
        "max_price": Decimal("80.00"),
    },
    {
        "name": "Prace w ogrodzie",
        "min_price": Decimal("60.00"),
        "max_price": Decimal("300.00"),
    },
]


def seed_categories(apps, schema_editor):
    ServiceCategory = apps.get_model("orders", "ServiceCategory")
    for category_data in CATEGORIES:
        ServiceCategory.objects.get_or_create(
            name=category_data["name"],
            defaults={
                "min_price": category_data["min_price"],
                "max_price": category_data["max_price"],
                "is_active": True,
            },
        )


def remove_categories(apps, schema_editor):
    ServiceCategory = apps.get_model("orders", "ServiceCategory")
    names = [cat["name"] for cat in CATEGORIES]
    ServiceCategory.objects.filter(name__in=names).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("orders", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(seed_categories, reverse_code=remove_categories),
    ]
