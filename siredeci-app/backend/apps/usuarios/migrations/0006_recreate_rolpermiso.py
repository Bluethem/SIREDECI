# Generated migration to recreate rolpermiso table with correct structure

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0005_alter_logauditoria_resultado'),
    ]

    operations = [
        # Drop the incorrectly structured table
        migrations.RunSQL(
            "DROP TABLE IF EXISTS rolpermiso CASCADE;",
            reverse_sql="DROP TABLE IF EXISTS rolpermiso CASCADE;"
        ),
        
        # Recreate the table with correct structure matching scriptDDL
        migrations.RunSQL(
            """
            CREATE TABLE rolpermiso (
                id_rol INTEGER NOT NULL,
                id_permiso INTEGER NOT NULL,
                fecha_asignacion TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                
                CONSTRAINT pk_rol_permiso PRIMARY KEY (id_rol, id_permiso),
                CONSTRAINT fk_rol_permiso_rol FOREIGN KEY (id_rol) REFERENCES rol(id_rol) ON DELETE CASCADE,
                CONSTRAINT fk_rol_permiso_permiso FOREIGN KEY (id_permiso) REFERENCES permiso(id_permiso) ON DELETE CASCADE
            );
            
            CREATE INDEX idx_rol_permiso_rol ON rolpermiso(id_rol);
            CREATE INDEX idx_rol_permiso_permiso ON rolpermiso(id_permiso);
            """,
            reverse_sql="DROP TABLE IF EXISTS rolpermiso CASCADE;"
        ),
    ]
