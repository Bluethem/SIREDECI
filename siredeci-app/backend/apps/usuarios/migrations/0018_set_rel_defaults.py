from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
        ('usuarios', '0017_fix_fk_column_names'),
    ]

    operations = [
        migrations.RunSQL(
            sql=(
                # UsuarioRol defaults and backfill
                'ALTER TABLE "usuariorol" ALTER COLUMN "fecha_asignacion" SET DEFAULT CURRENT_TIMESTAMP;'
                'UPDATE "usuariorol" SET "fecha_asignacion" = CURRENT_TIMESTAMP WHERE "fecha_asignacion" IS NULL;'
                'ALTER TABLE "usuariorol" ALTER COLUMN "es_activo" SET DEFAULT TRUE;'
                'UPDATE "usuariorol" SET "es_activo" = TRUE WHERE "es_activo" IS NULL;'
                # RolPermiso defaults and backfill
                'ALTER TABLE "rolpermiso" ALTER COLUMN "fecha_asignacion" SET DEFAULT CURRENT_TIMESTAMP;'
                'UPDATE "rolpermiso" SET "fecha_asignacion" = CURRENT_TIMESTAMP WHERE "fecha_asignacion" IS NULL;'
            ),
            reverse_sql=(
                'ALTER TABLE "usuariorol" ALTER COLUMN "fecha_asignacion" DROP DEFAULT;'
                'ALTER TABLE "usuariorol" ALTER COLUMN "es_activo" DROP DEFAULT;'
                'ALTER TABLE "rolpermiso" ALTER COLUMN "fecha_asignacion" DROP DEFAULT;'
            ),
        ),
    ]
