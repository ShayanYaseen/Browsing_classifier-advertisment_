# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.


class Order(models.Model):
    id = models.DecimalField(max_digits=5, decimal_places=2, primary_key=True)
    url = models.CharField(max_length=50)
    title = models.CharField(max_length=50)
    visit_count = models.DecimalField(max_digits=5, decimal_places=2)
    typed_count = models.DecimalField(max_digits=5, decimal_places=2)
    last_visit_time = models.DecimalField(max_digits=5, decimal_places=2)
