from django.apps import apps
from django.utils.module_loading import autodiscover_modules

_PANEL_REGISTRY = {}


def register(func=None, name=None):

    def inner_register(func):
        global _PANEL_REGISTRY

        assert callable(func)

        if not name:
            regname = "%s.%s" % (func.__module__, func.__name__)

        _PANEL_REGISTRY[regname] = func

    if func is None:
        return inner_register

    return inner_register(func)


def get_user_panels(user, request, **kwargs):

    panels = []

    for PanelCls in _PANEL_REGISTRY.values():

        panel = PanelCls(user, request, **kwargs)
        if panel.has_permission():
            panels.append(panel)

    return panels


def autodiscover():
    autodiscover_modules("panels")
