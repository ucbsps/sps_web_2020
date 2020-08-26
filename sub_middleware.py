"""
Django Middleware for rewriting / urls.
"""

import os
import sys

def sub_middleware(get_response):
    """Django Middleware for rewriting urls."""

    print(os.getcwd(), file=sys.stderr)
    BASE_DIR = ('/~' + '/'.join(os.getcwd().split('/')[-2:])).encode()

    def middleware(request):
        """Replaces href="/ with href="DIR/."""

        print(BASE_DIR, file=sys.stderr)

        response = get_response(request)

        response.content = response.content.replace(b'href="/',
                                                    b'href="' + BASE_DIR + b'/')
        response.content = response.content.replace(b'src="/',
                                                    b'src="' + BASE_DIR + b'/')

        return response

    return middleware
