from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
        ('denuncias', '0007_alter_denuncia_id_categoria_and_more'),
    ]

    operations = [
        migrations.RunSQL(
            sql=(
                'ALTER TABLE "denuncia" ALTER COLUMN "fecha_registro" SET DEFAULT CURRENT_TIMESTAMP;'
                'UPDATE "denuncia" SET "fecha_registro" = CURRENT_TIMESTAMP WHERE "fecha_registro" IS NULL;'
            ),
            reverse_sql=(
                'ALTER TABLE "denuncia" ALTER COLUMN "fecha_registro" DROP DEFAULT;'
            ),
        ),
    ]
