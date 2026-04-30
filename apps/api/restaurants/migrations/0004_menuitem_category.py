# Generated manually for issue #4.

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("restaurants", "0003_remove_category_icon_url_category_icon_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="menuitem",
            name="category",
            field=models.CharField(blank=True, default="", max_length=100),
        ),
    ]
