from django.db import migrations

def add_initial_data(apps, schema_editor):
    Site = apps.get_model('sites', 'Site')
    SocialApp = apps.get_model('socialaccount', 'SocialApp')
    # Update Site
    Site.objects.update_or_create(
        id=3,
        defaults={'domain': 'bb4-django.onrender.com', 'name': 'bb4-django.onrender.com'}
    )
    # Add Google SocialApp
    google_app, created = SocialApp.objects.get_or_create(
        provider='google',
        name='Google',
        client_id=os.getenv('GOOGLE_CLIENT_ID', 'your-client-id'),
        secret=os.getenv('GOOGLE_CLIENT_SECRET', 'your-secret'),
    )
    if created:
        google_app.sites.add(Site.objects.get(id=3))

class Migration(migrations.Migration):
    dependencies = [('socialaccount', '0001_initial'), ('sites', '0002_alter_domain_unique')]
    operations = [migrations.RunPython(add_initial_data)]