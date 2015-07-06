# -*- coding: utf-8 -*-
from django.db import models


class CompanyRecord(models.Model):
    name = models.TextField(verbose_name=u'Компания', unique=True, null=False)


class BuildingRecord(models.Model):
    name = models.TextField(verbose_name=u'Объект', unique=True)
    company = models.ForeignKey(CompanyRecord, verbose_name=u'Компания')


class BuildingFieldRecord(models.Model):
    field = models.TextField(verbose_name=u'Название поля', null=False)
    value = models.TextField(verbose_name=u'Значение поля', null=True)
    building = models.ForeignKey(BuildingRecord, verbose_name=u'Дом', null=False, related_name='building_field')

    class Meta:
        unique_together = ("building", "field")


class FlatRecord(models.Model):
    building = models.ForeignKey(BuildingRecord, verbose_name=u'Дом', null=True)


class FlatFieldRecord(models.Model):
    field = models.TextField(verbose_name=u'Название поля', null=False)
    value = models.TextField(verbose_name=u'Значение поля', null=True)
    flat = models.ForeignKey(FlatRecord, verbose_name=u'Квартира', null=False, related_name='flat_field')

    # class Meta:
       #  unique_together = ("flat", "field")

