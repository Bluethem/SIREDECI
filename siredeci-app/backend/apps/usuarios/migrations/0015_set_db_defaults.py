from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0014_remove_usuario_groups_remove_usuario_is_superuser_and_more'),
    ]

    operations = [
        migrations.RunSQL(
            sql=(
                'ALTER TABLE "usuario" ALTER COLUMN "fecha_creacion" SET DEFAULT CURRENT_TIMESTAMP;'
                'ALTER TABLE "usuario" ALTER COLUMN "intentos_login" SET DEFAULT 0;'
                'ALTER TABLE "usuario" ALTER COLUMN "requiere_mfa" SET DEFAULT FALSE;'
                "ALTER TABLE \"usuario\" ALTER COLUMN \"estado_cuenta\" SET DEFAULT 'Activo';"
            ),
            reverse_sql=(
                'ALTER TABLE "usuario" ALTER COLUMN "fecha_creacion" DROP DEFAULT;'
                'ALTER TABLE "usuario" ALTER COLUMN "intentos_login" DROP DEFAULT;'
                'ALTER TABLE "usuario" ALTER COLUMN "requiere_mfa" DROP DEFAULT;'
                'ALTER TABLE "usuario" ALTER COLUMN "estado_cuenta" DROP DEFAULT;'
            ),
        ),
    ]
