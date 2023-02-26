# Generated by Django 4.1.7 on 2023-02-25 09:11

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('hunter', '0002_alter_product_website'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='website',
            name='date',
        ),
        migrations.RemoveField(
            model_name='website',
            name='html',
        ),
        migrations.AddField(
            model_name='product',
            name='date_created',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='product',
            name='date_updated',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='website',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product', to='hunter.website'),
        ),
        migrations.CreateModel(
            name='TagData',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name_tag', models.TextField()),
                ('price_tag', models.TextField()),
                ('availability_tag', models.TextField()),
                ('url_tag', models.TextField()),
                ('related_website', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='tagData', to='hunter.website')),
            ],
        ),
        migrations.AddField(
            model_name='website',
            name='related_tag_data',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='website', to='hunter.tagdata'),
        ),
    ]
