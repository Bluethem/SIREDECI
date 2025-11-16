from django.db import migrations

SQL = r'''
DO $$ BEGIN
    -- UsuarioRol.id_usuario
    IF EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name='usuariorol' AND column_name='id_usuario_id'
    ) THEN
        EXECUTE 'ALTER TABLE "usuariorol" RENAME COLUMN "id_usuario_id" TO "id_usuario"';
    END IF;

    -- UsuarioRol.id_rol
    IF EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name='usuariorol' AND column_name='id_rol_id'
    ) THEN
        EXECUTE 'ALTER TABLE "usuariorol" RENAME COLUMN "id_rol_id" TO "id_rol"';
    END IF;

    -- RolPermiso.id_rol
    IF EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name='rolpermiso' AND column_name='id_rol_id'
    ) THEN
        EXECUTE 'ALTER TABLE "rolpermiso" RENAME COLUMN "id_rol_id" TO "id_rol"';
    END IF;

    -- RolPermiso.id_permiso
    IF EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name='rolpermiso' AND column_name='id_permiso_id'
    ) THEN
        EXECUTE 'ALTER TABLE "rolpermiso" RENAME COLUMN "id_permiso_id" TO "id_permiso"';
    END IF;
END $$;
'''

REVERSE_SQL = r'''
DO $$ BEGIN
    -- UsuarioRol.id_usuario
    IF EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name='usuariorol' AND column_name='id_usuario'
    ) THEN
        EXECUTE 'ALTER TABLE "usuariorol" RENAME COLUMN "id_usuario" TO "id_usuario_id"';
    END IF;

    -- UsuarioRol.id_rol
    IF EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name='usuariorol' AND column_name='id_rol'
    ) THEN
        EXECUTE 'ALTER TABLE "usuariorol" RENAME COLUMN "id_rol" TO "id_rol_id"';
    END IF;

    -- RolPermiso.id_rol
    IF EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name='rolpermiso' AND column_name='id_rol'
    ) THEN
        EXECUTE 'ALTER TABLE "rolpermiso" RENAME COLUMN "id_rol" TO "id_rol_id"';
    END IF;

    -- RolPermiso.id_permiso
    IF EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name='rolpermiso' AND column_name='id_permiso'
    ) THEN
        EXECUTE 'ALTER TABLE "rolpermiso" RENAME COLUMN "id_permiso" TO "id_permiso_id"';
    END IF;
END $$;
'''

class Migration(migrations.Migration):
    dependencies = [
        ('usuarios', '0016_alter_rolpermiso_id_permiso_alter_rolpermiso_id_rol_and_more'),
    ]

    operations = [
        migrations.RunSQL(sql=SQL, reverse_sql=REVERSE_SQL),
    ]
