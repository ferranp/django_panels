import re

from django.contrib.auth import get_user_model
from django.template.loader import render_to_string
from rest_framework import viewsets
from rest_framework.response import Response

from .register import get_user_panels


class PanelViewSet(viewsets.ViewSet):
    def list(self, request, format=None):
        data = {}

        username = request.GET.get("user")
        if username:
            User = get_user_model()
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                user = None
        else:
            user = request.user

        try:
            show_count = int(request.GET.get("show_count", 10))
        except ValueError:
            show_count = 10

        if user:
            panels = get_user_panels(user, request, show_count=show_count)
        else:
            panels = []

        if request.GET.get("all"):
            # First the ones wioth data, after the rest
            panels.sort(key=lambda x: not x.has_data())
        else:
            panels = [panel for panel in panels if panel.has_data()]

        data = []

        for panel in panels:

            object_list = panel.object_list()

            context = {
                "object_list": object_list,
            }

            html = render_to_string(
                panel.template_name, context=context, request=request
            )
            # converty to abslure url
            absolutize = (
                lambda m: ' href="' + request.build_absolute_uri(m.group(1)) + '"'
            )
            html = re.sub(r' href="([^"]+)"', absolutize, html)

            more_url = panel.more_url()

            if more_url:
                more_url = request.build_absolute_uri(more_url)

            items = []
            for obj in object_list:
                url = panel.get_object_url(obj)
                if url:
                    url = request.build_absolute_uri(url)
                name = panel.get_object_name(obj)
                obj_id = panel.get_object_id(obj)

                item = {
                    "name": name,
                    "id": obj_id,
                    "absolute_url": url,
                }
                items.append(item)

            panel_name = "{}.{}".format(panel.__class__.__module__, panel.__class__.__name__)

            serialized = {
                "name": panel_name,
                "title": panel.title,
                "html": html,
                "more_url": more_url,
                "count": len(panel.get_queryset()),
                "items": items,
            }
            data.append(serialized)
        return Response(data)
