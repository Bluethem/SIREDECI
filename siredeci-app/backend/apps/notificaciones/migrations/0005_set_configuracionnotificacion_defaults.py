from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
        ('notificaciones', '0004_alter_configuracionnotificacion_table'),
    ]

    operations = [
        migrations.RunSQL(
            sql=(
                "ALTER TABLE \"configuracionnotificacion\" ALTER COLUMN \"horario_preferido\" SET DEFAULT '';"
                "UPDATE \"configuracionnotificacion\" SET \"horario_preferido\" = '' WHERE \"horario_preferido\" IS NULL;"
            ),
            reverse_sql=(
                'ALTER TABLE "configuracionnotificacion" ALTER COLUMN "horario_preferido" DROP DEFAULT;'
            ),
        ),
    ]
