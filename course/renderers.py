from rest_framework import renderers


class PlainTextRenderer(renderers.BaseRenderer):
    media_type = 'text/plain'
    format = 'text'

    def render(self, data, media_type=None, renderer_context=None):
        return str(renderers.JSONRenderer().render(data, media_type, renderer_context)).encode(self.charset)
