from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
        ('denuncias', '0008_set_denuncia_defaults'),
    ]

    operations = [
        migrations.RunSQL(
            sql=(
                'ALTER TABLE "denuncia" ALTER COLUMN "fecha_actualizacion" SET DEFAULT CURRENT_TIMESTAMP;'
                'UPDATE "denuncia" SET "fecha_actualizacion" = CURRENT_TIMESTAMP WHERE "fecha_actualizacion" IS NULL;'
            ),
            reverse_sql=(
                'ALTER TABLE "denuncia" ALTER COLUMN "fecha_actualizacion" DROP DEFAULT;'
            ),
        ),
    ]
