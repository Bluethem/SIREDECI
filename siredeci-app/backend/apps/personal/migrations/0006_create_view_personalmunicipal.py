from django.db import migrations

CREATE_VIEW_SQL = r'''
CREATE OR REPLACE VIEW personalmunicipal AS
SELECT 
  id_personal,
  codigo_personal,
  dni,
  nombre,
  apellido,
  email,
  cargo,
  fecha_ingreso,
  estado_laboral,
  especialidad,
  id_area_responsable_id AS id_area_responsable,
  id_usuario_id AS id_usuario
FROM personal_municipal;
'''

DROP_VIEW_SQL = "DROP VIEW IF EXISTS personalmunicipal;"

class Migration(migrations.Migration):
    dependencies = [
        ('personal', '0005_alter_personaltelefono_table'),
    ]

    operations = [
        migrations.RunSQL(sql=CREATE_VIEW_SQL, reverse_sql=DROP_VIEW_SQL),
    ]
