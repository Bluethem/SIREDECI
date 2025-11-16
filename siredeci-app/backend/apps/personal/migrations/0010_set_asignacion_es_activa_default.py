from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
        ('personal', '0009_alter_asignacion_id_denuncia_and_more'),
    ]

    operations = [
        migrations.RunSQL(
            sql=(
                'ALTER TABLE "asignacion" ALTER COLUMN "es_activa" SET DEFAULT TRUE;'
                'UPDATE "asignacion" SET "es_activa" = TRUE WHERE "es_activa" IS NULL;'
            ),
            reverse_sql=(
                'ALTER TABLE "asignacion" ALTER COLUMN "es_activa" DROP DEFAULT;'
            ),
        ),
    ]
