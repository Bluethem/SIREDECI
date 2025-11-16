# Generated migration to fix categoria foreign key column name

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('categorias', '0003_alter_arearesponsable_table'),
    ]

    operations = [
        # Drop the incorrectly named column and recreate with correct name
        migrations.RunSQL(
            """
            ALTER TABLE categoria DROP COLUMN IF EXISTS id_area_responsable_id;
            ALTER TABLE categoria ADD COLUMN id_area_responsable INTEGER NOT NULL;
            ALTER TABLE categoria ADD CONSTRAINT fk_categoria_area FOREIGN KEY (id_area_responsable) REFERENCES arearesponsable(id_area_responsable);
            CREATE INDEX idx_categoria_area ON categoria(id_area_responsable);
            """,
            reverse_sql="""
            ALTER TABLE categoria DROP COLUMN IF EXISTS id_area_responsable;
            ALTER TABLE categoria ADD COLUMN id_area_responsable_id INTEGER NOT NULL;
            ALTER TABLE categoria ADD CONSTRAINT fk_categoria_area FOREIGN KEY (id_area_responsable_id) REFERENCES arearesponsable(id_area_responsable);
            CREATE INDEX idx_categoria_area ON categoria(id_area_responsable_id);
            """
        ),
    ]
