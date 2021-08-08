class UserVerificationMiddleWare(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_template_response(self, request, response):
        current_user = request.user
        if hasattr(response, 'data') and not request.user.is_anonymous:
            response.data['user_verification'] = str(current_user.user_verification)
        return response
