from __future__ import unicode_literals

from django.db import models
from decimal import Decimal

class Family(models.Model):
    YES_NO_CHOICES = (
        (0, "No"),
        (1, "YES")
    )

    HOUSEHOLD_TYPE_CHOICES = (
        (1, "Mother and Father"),
        (2, "Mother"),
        (3, "Mother and Stepfather"),
        (4, "Father"),
        (5, "Other"),
        (6, "Unknown")
    )

    HOME_TYPE_CHOICES = (
        (1, "Own"),
        (2, "Rent"),
        (3, "Other")
    )

    CONSTRUCTION_TYPE_CHOICES = (
        (1, "Concrete"),
        (2, "Earth"),
        (3, "Wooden, 2 Room"),
        (4, "Wooden, 1 Room")
    )

    PARENT_EDUCATION_CHOICES = (
        (1, "Neither"),
        (2, "Only"),
        (3, "Didn't"),
        (4, "At least")
    )

    PARENT_ABROAD_CHOICES = (
        (1, "None"),
        (2, "Yes, Other"),
        (3, "Yes, Father"),
        (4, "Yes, Mother")
    )

    OCCUPATION_CHOICES = (
        (1, "Farmer"),
        (2, "Owner"),
        (3, "Worker"),
        (4, "Trades"),
        (5, "Other"),
        (6, "Unknown")
    )

    parent_name = models.CharField(max_length=128, unique=True)
    household_type = models.IntegerField(choices=HOUSEHOLD_TYPE_CHOICES, blank=True, null=True)
    family_members = models.IntegerField(blank=True, null=True)
    father_occupation = models.IntegerField(choices=OCCUPATION_CHOICES, blank=True, null=True)
    mother_occupation = models.IntegerField(choices=OCCUPATION_CHOICES, blank=True, null=True)
    household_income = models.DecimalField(max_digits=6,decimal_places=2,default=Decimal('0.00'), blank=True, null=True)
    have_maid = models.IntegerField(choices=YES_NO_CHOICES, blank=True, null=True, default=0)
    home_type = models.IntegerField(choices=HOME_TYPE_CHOICES, blank=True, null=True, default=2)
    construction_type = models.IntegerField(choices=CONSTRUCTION_TYPE_CHOICES, blank=True, null=True)
    parent_education = models.IntegerField(choices=PARENT_EDUCATION_CHOICES, blank=True, null=True, default=1)
    parent_abroad = models.IntegerField(choices=PARENT_ABROAD_CHOICES, blank=True, null=True, default=1)
    father_alive = models.IntegerField(choices=YES_NO_CHOICES, blank=True, null=True, default=1)
    mother_alive = models.IntegerField(choices=YES_NO_CHOICES, blank=True, null=True, default=1)
    total_children = models.IntegerField(blank=True, null=True)
    children_in_program = models.IntegerField(blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "families"

    def __unicode__(self):
        return self.parent_name

class Child(models.Model):
    YES_NO_CHOICES = (
        (0, "No"),
        (1, "YES")
    )

    HEALTH_CHOICES = (
        (1, "Home"),
        (2, "Often"),
        (3, "Constantly"),
        (4, "Drug")
    )

    EDUCATION_CHOICES = (
        (0, "None"),
        (1, "Some"),
        (2, "All")
    )

    TOWN_CHOICES = (
        ("BL", "Bas-Limbe"),
        ("BN", "Bazilan"),
        ("CB", "Chouchou Bay"),
        ("PM", "Port Margot"),
        ("RT", "Robert")
    )

    GRADE_LEVEL_CHOICES = (
        (0, "Preschool"),
        (1, "First"),
        (2, "Second"),
        (3, "Third"),
        (4, "Fourth"),
        (5, "Fifth"),
        (6, "Sixth")
    )

    child_id = models.CharField(max_length=16, unique=True)
    first_name = models.CharField(max_length=128, blank=True, null=True)
    last_name = models.CharField(max_length=128, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    grade_level = models.IntegerField(choices=GRADE_LEVEL_CHOICES, blank=True, null=True)
    town = models.CharField(choices=TOWN_CHOICES, max_length=16, blank=True, null=True)
    family = models.ForeignKey(Family, blank=True, null=True)
    education = models.IntegerField(choices=EDUCATION_CHOICES, blank=True, null=True, default=1)
    health_status = models.IntegerField(choices=HEALTH_CHOICES, blank=True, null=True, default=3)
    daily_meals = models.IntegerField(blank=True, null=True)
    has_photo = models.IntegerField(choices=YES_NO_CHOICES, blank=True, null=True, default=0)
    created_date = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "children"
        ordering = ('last_name', 'first_name')

    def __unicode__(self):
        return self.child_id