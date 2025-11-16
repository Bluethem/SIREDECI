from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
        ('denuncias', '0012_alter_seguimiento_id_denuncia_and_more'),
    ]

    operations = [
        migrations.RunSQL(
            sql=(
                'ALTER TABLE "seguimiento" ALTER COLUMN "fecha_hora" SET DEFAULT CURRENT_TIMESTAMP;'
                'UPDATE "seguimiento" SET "fecha_hora" = CURRENT_TIMESTAMP WHERE "fecha_hora" IS NULL;'
            ),
            reverse_sql=(
                'ALTER TABLE "seguimiento" ALTER COLUMN "fecha_hora" DROP DEFAULT;'
            ),
        ),
    ]
