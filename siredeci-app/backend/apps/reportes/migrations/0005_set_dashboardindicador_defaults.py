from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
        ('reportes', '0004_alter_dashboardindicador_id_dashboard_and_more'),
    ]

    operations = [
        migrations.RunSQL(
            sql=(
                'ALTER TABLE "dashboardindicador" ALTER COLUMN "fecha_asignacion" SET DEFAULT CURRENT_TIMESTAMP;'
                'UPDATE "dashboardindicador" SET "fecha_asignacion" = CURRENT_TIMESTAMP WHERE "fecha_asignacion" IS NULL;'
            ),
            reverse_sql=(
                'ALTER TABLE "dashboardindicador" ALTER COLUMN "fecha_asignacion" DROP DEFAULT;'
            ),
        ),
    ]
