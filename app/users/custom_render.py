from rest_framework.renderers import JSONRenderer


class CustomJsonRender(JSONRenderer):

    def render(self, data, accepted_media_type=None, renderer_context=None):

        if renderer_context:
            response = renderer_context['response']
            msg = "OK"
            code = response.status_code
            if isinstance(data, dict):
                msg = data.pop('msg', msg)
                code = data.pop('code', code)
                data = data.pop('data', data)
            if code != 200 and data:
                msg = data.pop('detail', 'failed')
            response.status_code = 200
            res = {
                'status': code,
                'message': msg,
                'info': data,
            }
            return super().render(res, accepted_media_type, renderer_context)
        else:
            return super().render(data, accepted_media_type, renderer_context)
