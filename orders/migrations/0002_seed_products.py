from django.db import migrations


def seed_products(apps, schema_editor):
    Product = apps.get_model("orders", "Product")

    Product.objects.bulk_create([
        Product(
            name="Laptop",
            sku="LAP-001",
            price="999.99",
            stock=15
        ),
        Product(
            name="Keyboard",
            sku="KEY-001",
            price="49.99",
            stock=100
        ),
        Product(
            name="Mouse",
            sku="MOU-001",
            price="19.99",
            stock=200
        ),
    ])


def reverse_seed(apps, schema_editor):
    Product = apps.get_model("orders", "Product")
    Product.objects.filter(
        sku__in=["LAP-001", "KEY-001", "MOU-001"]
    ).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("orders", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(
            seed_products,
            reverse_seed
        ),
    ]