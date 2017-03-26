from django.contrib import admin
from . import models
from .filters import FilteredChoicesFieldListFilter

from import_export import resources
from import_export.admin import ImportExportModelAdmin
from import_export.widgets import ForeignKeyWidget
from import_export import fields
from django.contrib.admin.filters import AllValuesFieldListFilter

class FamilyResource(resources.ModelResource):

    class Meta:
        model = models.Family
        skip_unchanged = True
        report_skipped = False

        widgets = {
            'created_date': {'format': '%m/%d/%y'},
            'last_updated': {'format': '%m/%d/%y'}
        }

        fields = ('id', 'parent_name', 'household_type', 'family_members', 'father_occupation', 'mother_occupation',
                  'household_income', 'have_maid', 'home_type', 'construction_type', 'parent_education',
                  'parent_abroad', 'father_alive', 'mother_alive', 'total_children', 'children_in_program',
                  'created_date', 'last_updated')

        export_order = fields

class ChildResource(resources.ModelResource):

    family = fields.Field(
        column_name='family',
        attribute='family',
        widget=ForeignKeyWidget(models.Family, 'parent_name')
    )

    class Meta:
        model = models.Child
        skip_unchanged = True
        report_skipped = False

        widgets = {
            'birth_date': {'format': '%m/%d/%y'},
            'created_date': {'format': '%m/%d/%y'},
            'last_updated': {'format': '%m/%d/%y'}
        }

        fields = ('id', 'child_id', 'first_name', 'last_name', 'birth_date', 'age', 'grade_level', 'town', 'education',
                  'health_status', 'daily_meals', 'has_photo', 'family', 'created_date', 'last_updated')

        export_order = fields

class ChildAdmin(ImportExportModelAdmin):
    resource_class = ChildResource
    search_fields = ('child_id',)
    list_display = [f.name for f in models.Child._meta.fields]
    list_filter = (('town', AllValuesFieldListFilter),
                   ('has_photo', FilteredChoicesFieldListFilter),
                   ('health_status', FilteredChoicesFieldListFilter),
                   ('education', FilteredChoicesFieldListFilter),
                   ('grade_level', FilteredChoicesFieldListFilter),
                   'daily_meals',
                   'age',
                   )
admin.site.register(models.Child, ChildAdmin)

class ChildInline(admin.StackedInline):
    model = models.Child
    extra = 0

class FamilyAdmin(ImportExportModelAdmin):
    resource_class = FamilyResource
    list_display = [f.name for f in models.Family._meta.fields]
    inlines = [ChildInline, ]
    list_filter = (('household_type', FilteredChoicesFieldListFilter),
                   'family_members',
                   ('father_occupation', FilteredChoicesFieldListFilter),
                   ('mother_occupation', FilteredChoicesFieldListFilter),
                   'household_income',
                   ('have_maid', FilteredChoicesFieldListFilter),
                   ('home_type', FilteredChoicesFieldListFilter),
                   ('construction_type', FilteredChoicesFieldListFilter),
                   ('parent_education', FilteredChoicesFieldListFilter),
                   ('father_alive', FilteredChoicesFieldListFilter),
                   ('mother_alive', FilteredChoicesFieldListFilter),
                   ('total_children', AllValuesFieldListFilter),
                   ('children_in_program', AllValuesFieldListFilter))
admin.site.register(models.Family, FamilyAdmin)


