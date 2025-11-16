from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
        ('ciudadanos', '0004_alter_ciudadano_id_usuario_and_more'),
    ]

    operations = [
        migrations.RunSQL(
            sql=(
                'ALTER TABLE "ciudadano" ALTER COLUMN "fecha_registro" SET DEFAULT CURRENT_TIMESTAMP;'
                'UPDATE "ciudadano" SET "fecha_registro" = CURRENT_TIMESTAMP WHERE "fecha_registro" IS NULL;'
                'ALTER TABLE "ciudadano" ALTER COLUMN "es_anonimo" SET DEFAULT FALSE;'
                'UPDATE "ciudadano" SET "es_anonimo" = FALSE WHERE "es_anonimo" IS NULL;'
                "ALTER TABLE \"ciudadano\" ALTER COLUMN \"estado_cuenta\" SET DEFAULT 'Activo';"
                "UPDATE \"ciudadano\" SET \"estado_cuenta\" = 'Activo' WHERE \"estado_cuenta\" IS NULL;"
            ),
            reverse_sql=(
                'ALTER TABLE "ciudadano" ALTER COLUMN "fecha_registro" DROP DEFAULT;'
                'ALTER TABLE "ciudadano" ALTER COLUMN "es_anonimo" DROP DEFAULT;'
                'ALTER TABLE "ciudadano" ALTER COLUMN "estado_cuenta" DROP DEFAULT;'
            ),
        ),
    ]
