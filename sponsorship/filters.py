from django.contrib import admin
from django.contrib.admin.utils import reverse_field_path
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import smart_text

def filter_lookups_queryset(request, qs, lookup_kwarg=None):
    # Filter lookup queryset for all target_params in request.GET params, except for param of request initiator itself
    if lookup_kwarg:
        initial_attrs = dict([(param, val) for param, val in request.GET.iteritems()
                              if val and int(val) in range(100) and param != lookup_kwarg])
    else:
        initial_attrs = dict([(param, val) for param, val in request.GET.iteritems()
                              if val and int(val) in range(100) and param])

    return qs.filter(**initial_attrs)

class FilteredChoicesFieldListFilter(admin.FieldListFilter):
    def __init__(self, field, request, params, model, model_admin, field_path):
        self.lookup_kwarg = '%s__exact' % field_path
        self.lookup_kwarg_isnull = '%s__isnull' % field_path
        self.lookup_val = request.GET.get(self.lookup_kwarg)
        self.lookup_val_isnull = request.GET.get(self.lookup_kwarg_isnull)
        # Obey parent ModelAdmin queryset when deciding which options to show
        parent_model, reverse_path = reverse_field_path(model, field_path)
        if model == parent_model:
            queryset = model_admin.get_queryset(request)
        else:
            queryset = parent_model._default_manager.all()

        queryset = filter_lookups_queryset(request, queryset, lookup_kwarg=self.lookup_kwarg)

        self.lookup_choices = (queryset
                               .distinct()
                               .order_by(field.name)
                               .values_list(field.name, flat=True))

        super(FilteredChoicesFieldListFilter, self).__init__(
            field, request, params, model, model_admin, field_path)

    def expected_parameters(self):
        return [self.lookup_kwarg, self.lookup_kwarg_isnull]

    def choices(self, changelist):
        yield {
            'selected': self.lookup_val is None,
            'query_string': changelist.get_query_string(
                {}, [self.lookup_kwarg, self.lookup_kwarg_isnull]
            ),
            'display': _('All')
        }
        none_title = ''
        for lookup, title in self.field.flatchoices:
            if lookup is None:
                none_title = title
                continue
            if lookup in self.lookup_choices:
                yield {
                    'selected': smart_text(lookup) == self.lookup_val,
                    'query_string': changelist.get_query_string(
                        {self.lookup_kwarg: lookup}, [self.lookup_kwarg_isnull]
                    ),
                    'display': title,
                }
        if none_title:
            yield {
                'selected': bool(self.lookup_val_isnull),
                'query_string': changelist.get_query_string({
                    self.lookup_kwarg_isnull: 'True',
                }, [self.lookup_kwarg]),
                'display': none_title,
            }
admin.FieldListFilter.register(lambda f: bool(f.choices), FilteredChoicesFieldListFilter)


class FilteredAllValuesFieldListFilter(admin.FieldListFilter):
    def __init__(self, field, request, params, model, model_admin, field_path):
        self.lookup_kwarg = field_path
        self.lookup_kwarg_isnull = '%s__isnull' % field_path
        self.lookup_val = request.GET.get(self.lookup_kwarg)
        self.lookup_val_isnull = request.GET.get(self.lookup_kwarg_isnull)
        self.empty_value_display = model_admin.get_empty_value_display()
        parent_model, reverse_path = reverse_field_path(model, field_path)
        # Obey parent ModelAdmin queryset when deciding which options to show
        if model == parent_model:
            queryset = model_admin.get_queryset(request)
        else:
            queryset = parent_model._default_manager.all()

        queryset = filter_lookups_queryset(request, queryset, lookup_kwarg=self.lookup_kwarg)
        self.lookup_choices = (queryset
                               .distinct()
                               .order_by(field.name)
                               .values_list(field.name, flat=True))
        super(FilteredAllValuesFieldListFilter, self).__init__(
            field, request, params, model, model_admin, field_path)

    def expected_parameters(self):
        return [self.lookup_kwarg, self.lookup_kwarg_isnull]

    def choices(self, changelist):
        yield {
            'selected': self.lookup_val is None and self.lookup_val_isnull is None,
            'query_string': changelist.get_query_string({}, [self.lookup_kwarg, self.lookup_kwarg_isnull]),
            'display': _('All'),
        }
        include_none = False
        for val in self.lookup_choices:
            if val is None:
                include_none = True
                continue
            val = smart_text(val)
            yield {
                'selected': self.lookup_val == val,
                'query_string': changelist.get_query_string({
                    self.lookup_kwarg: val,
                }, [self.lookup_kwarg_isnull]),
                'display': val,
            }
        if include_none:
            yield {
                'selected': bool(self.lookup_val_isnull),
                'query_string': changelist.get_query_string({
                    self.lookup_kwarg_isnull: 'True',
                }, [self.lookup_kwarg]),
                'display': self.empty_value_display,
            }
admin.FieldListFilter.register(lambda f: True, FilteredAllValuesFieldListFilter)


class FilteredRelatedOnlyFieldListFilter(admin.RelatedFieldListFilter):
    def field_choices(self, field, request, model_admin):
        queryset = model_admin.get_queryset(request)
        lookup_kwarg = "%s__id__exact" % self.field_path
        queryset = filter_lookups_queryset(request, queryset, lookup_kwarg=lookup_kwarg)
        pk_qs = queryset.distinct().values_list('%s__pk' % self.field_path, flat=True)
        field_choices = field.get_choices(include_blank=False, limit_choices_to={'pk__in': pk_qs})
        return field_choices

    @property
    def include_empty_choice(self):
        """
        Return True if a "(None)" choice should be included, which filters
        out everything except empty relationships.
        """
        return self.field.null or (self.field.is_relation and self.field.many_to_many)\
            or (self.field_path == 'client' and self.field.name == 'client')