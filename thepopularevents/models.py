from django.contrib.gis.db import models
from django.contrib.postgres.operations import CreateExtension
from django.db import migrations

class Migration(migrations.Migration):

    operations = [
        CreateExtension('postgis'),
    ]


class model1(models.Model):
    geom = models.GeometryField(srid=4326,blank=True,null=True)
    name = models.TextField(null=True)

