import urllib
from datetime import date

from dateutil.relativedelta import relativedelta
from django.contrib import messages
from django.db import models
from django.shortcuts import redirect, reverse
from django.utils.functional import cached_property
from django.utils.translation import ugettext_lazy as _
from django.views.generic import CreateView, DetailView, TemplateView, UpdateView
from django_filters.views import FilterView


class BasePanel(object):
    template_name = "panels/panel.html"

    model = None
    ordering = None
    exclude_params = None

    more_params = None
    base_more_url = None

    params = {}
    exclude_params = {}

    title = None

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

    def get_queryset(self):
        qs = self.model.objects.filter(**self.params)
        if self.exclude_params:
            qs = qs.exclude(**self.exclude_params)
        if self.ordering:
            qs = qs.order_by(*self.ordering)
        return qs

    def is_visible(self):
        return self.get_queryset().exists()

    @property
    def more(self):
        return bool(self.more_url)

    def more_url(self):
        mparams = self.more_params
        if mparams is None:
            mparams = self.params
        return "%s?%s" % (self.base_more_url, urllib.parse.urlencode(mparams))


class PanelsView(TemplateView):
    template_name = "panels/panels_dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        panels = self.get_panels()

        context["panels"] = [panel for panel in panels if panel.is_visible()]

        return context

    def get_panels(self):
        return []
