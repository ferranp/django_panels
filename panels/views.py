import urllib

from django.views.generic import TemplateView

from .register import get_user_panels


class BasePanel(object):
    template_name = "panels/panel.html"

    model = None
    ordering = None
    exclude_params = None

    more_params = None
    base_more_url = None

    params = {}
    exclude_params = {}
    show_count = 10
    title = None

    def __init__(self, user, request, **kwargs):

        self.user = user
        self.request = request
        for k, v in kwargs.items():
            setattr(self, k, v)

    permission_required = None

    def has_permission(self):

        if self.permission_required is None:
            return True

        if isinstance(self.permission_required, str):
            perms = (self.permission_required,)
        else:
            perms = self.permission_required

        return self.user.has_perms(perms)

    def get_params(self):
        return self.params

    def get_queryset(self):
        qs = self.model.objects.filter(**self.get_params())
        if self.exclude_params:
            qs = qs.exclude(**self.exclude_params)
        if self.ordering:
            qs = qs.order_by(*self.ordering)
        return qs

    def object_list(self):
        return self.get_queryset()[:self.show_count]

    def has_data(self):
        return self.get_queryset().exists()

    @property
    def more(self):
        return bool(self.more_url())

    def more_url(self):
        if not self.base_more_url:
            return None

        mparams = self.more_params
        if mparams is None:
            mparams = self.get_params()

        return "%s?%s" % (self.base_more_url, urllib.parse.urlencode(mparams))


class PanelsView(TemplateView):
    template_name = "panels/panels_dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        panels = get_user_panels(self.request.user, self.request)

        if self.request.GET.get("all"):
            # First the ones width data, after the rest
            panels.sort(key=lambda x: not x.has_data())
            context["panels"] = panels
        else:
            context["panels"] = [panel for panel in panels if panel.has_data()]

        return context

    def get_panels(self):
        return []
