from django.db import migrations

def update_site(apps, schema_editor):
    Site = apps.get_model('sites', 'Site')
    Site.objects.update_or_create(
        id=1,
        defaults={
            'domain': 'myjobs-backend-b2y5.onrender.com',
            'name': 'myjobs'
        }
    )

class Migration(migrations.Migration):
    dependencies = [
        ('accounts', '0003_alter_user_industry_alter_user_years_of_experience'),  # ← fixed
        ('sites', '0002_alter_domain_unique'),
    ]
    operations = [
        migrations.RunPython(update_site, migrations.RunPython.noop),
    ]