# Generated migration to add password_hash field to Usuario table

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0006_recreate_rolpermiso'),
    ]

    operations = [
        # Add password_hash field to match scriptDDL
        migrations.AddField(
            model_name='usuario',
            name='password_hash',
            field=models.CharField(
                max_length=255,
                verbose_name='Hash de Contraseña'
            ),
        ),
        # Copy existing password to password_hash field
        migrations.RunSQL(
            "UPDATE usuario SET password_hash = password WHERE password IS NOT NULL;",
            reverse_sql="UPDATE usuario SET password = password_hash WHERE password_hash IS NOT NULL;"
        ),
    ]
