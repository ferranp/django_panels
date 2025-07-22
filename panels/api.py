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

            url = panel.more_url()

            if url:
                url = request.build_absolute_uri(url)

            items = []
            for obj in object_list:
                if hasattr(obj, "get_absolute_url"):
                    url = request.build_absolute_uri(obj.get_absolute_url())
                elif hasattr(obj, "absolute_url"):
                    url = request.build_absolute_uri(obj.absolute_url)
                else:
                    url = None

                item = {
                    "name": str(obj),
                    "id": obj.pk,
                    "absolute_url": url,
                }
                items.append(item)

            serialized = {
                "html": html,
                "title": panel.title,
                "more_url": url,
                "count": len(panel.get_queryset()),
                "items": items,
            }
            data.append(serialized)
        return Response(data)
