from graphql_jwt.shortcuts import get_user_by_token

class CookieToUser:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        
        try:
            user=get_user_by_token(request.COOKIES['JWT'], request)
            request.user=user
        except:
            pass


        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response