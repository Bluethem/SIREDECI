from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
        ('denuncias', '0010_set_denuncia_es_anonima_default'),
    ]

    operations = [
        migrations.RunSQL(
            sql=(
                'ALTER TABLE "denuncia" ALTER COLUMN "requiere_validacion" SET DEFAULT TRUE;'
                'UPDATE "denuncia" SET "requiere_validacion" = TRUE WHERE "requiere_validacion" IS NULL;'
            ),
            reverse_sql=(
                'ALTER TABLE "denuncia" ALTER COLUMN "requiere_validacion" DROP DEFAULT;'
            ),
        ),
    ]
