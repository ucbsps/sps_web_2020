"""
Django Middleware for rewriting / urls.
"""

BASE_DIR = b'/~carterturn/sps'

def sub_middleware(get_response):
    """Django Middleware for rewriting urls."""

    def middleware(request):
        """Replaces href="/ with href="DIR/."""

        response = get_response(request)

        response.content = response.content.replace(b'href="/',
                                                    b'href="' + BASE_DIR + b'/')
        response.content = response.content.replace(b'src="/',
                                                    b'src="' + BASE_DIR + b'/')

        return response

    return middleware
