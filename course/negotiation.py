from rest_framework.renderers import JSONRenderer
from rest_framework.negotiation import DefaultContentNegotiation


class JSONDefaultRendererContentNegotiation(DefaultContentNegotiation):
    """http://www.django-rest-framework.org/api-guide/content-negotiation/#example"""
    def select_renderer(self, request, renderers, format_suffix):
        """Given a request and a list of renderers, return a two-tuple of:
        (renderer, media type)

        If format not in querystring then use JSON as the default renderer,
        otherwise defer to the select_renderer of the DefaultContentNegotiation.

        """
        if 'format' not in request.GET:
            return (JSONRenderer(), JSONRenderer.media_type)
        return super().select_renderer(request, renderers, format_suffix)
