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
            user = User.objects.get(username=username)
        else:
            user = request.user

        try:
            show_count = int(request.GET.get("show_count", 10))
        except ValueError:
            show_count = 10

        panels = get_user_panels(user, request, show_count=show_count)
        panels = [panel for panel in panels if panel.is_visible()]

        data = []

        for panel in panels:

            object_list = panel.object_list()

            context = {
                "object_list": object_list,
            }

            html = render_to_string(panel.template_name, context=context, request=request)

            url = panel.more_url()

            if url:
                url = request.build_absolute_uri(url)

            serialized = {
                "html": html,
                "title": panel.title,
                "more_url": url,
                "count": len(panel.get_queryset()),
            }
            data.append(serialized)
        return Response(data)
