from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
        ('denuncias', '0013_set_seguimiento_fecha_hora_default'),
    ]

    operations = [
        migrations.RunSQL(
            sql=(
                'ALTER TABLE "seguimiento" ALTER COLUMN "es_visible" SET DEFAULT TRUE;'
                'UPDATE "seguimiento" SET "es_visible" = TRUE WHERE "es_visible" IS NULL;'
            ),
            reverse_sql=(
                'ALTER TABLE "seguimiento" ALTER COLUMN "es_visible" DROP DEFAULT;'
            ),
        ),
    ]
