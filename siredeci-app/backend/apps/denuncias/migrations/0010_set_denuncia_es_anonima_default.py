from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
        ('denuncias', '0009_set_denuncia_fecha_actualizacion_default'),
    ]

    operations = [
        migrations.RunSQL(
            sql=(
                'ALTER TABLE "denuncia" ALTER COLUMN "es_anonima" SET DEFAULT FALSE;'
                'UPDATE "denuncia" SET "es_anonima" = FALSE WHERE "es_anonima" IS NULL;'
            ),
            reverse_sql=(
                'ALTER TABLE "denuncia" ALTER COLUMN "es_anonima" DROP DEFAULT;'
            ),
        ),
    ]
