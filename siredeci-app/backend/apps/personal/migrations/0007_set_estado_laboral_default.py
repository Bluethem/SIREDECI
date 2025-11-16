from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
        ('personal', '0006_create_view_personalmunicipal'),
    ]

    operations = [
        migrations.RunSQL(
            sql=(
                "ALTER TABLE \"personal_municipal\" ALTER COLUMN \"estado_laboral\" SET DEFAULT 'Activo';"
                "UPDATE \"personal_municipal\" SET \"estado_laboral\" = 'Activo' WHERE \"estado_laboral\" IS NULL;"
            ),
            reverse_sql=(
                "ALTER TABLE \"personal_municipal\" ALTER COLUMN \"estado_laboral\" DROP DEFAULT;"
            ),
        ),
    ]
