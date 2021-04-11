from functools import wraps

import flask
import werkzeug
import werkzeug.wrappers


def response(*, mimetype: str = None, template_file: str = None):
    def response_inner(f):
        print("Wrapping in response {}".format(f.__name__), flush=True)

        @wraps(f)
        def view_method(*args, **kwargs):
            resource_val = f(*args, **kwargs)
            if isinstance(resource_val, werkzeug.wrappers.Response):
                return resource_val

            if isinstance(resource_val, flask.Response):
                return resource_val

            if isinstance(resource_val, dict):
                model = dict(resource_val)
            else:
                model = dict()

            if template_file and not isinstance(resource_val, dict):
                raise Exception(
                    "Invalid return type {}, we expected a dict as the return value.".format(type(resource_val))
                )

            if template_file:
                resource_val = flask.render_template(template_file, **resource_val)

            resp = flask.make_response(resource_val)
            resp.model = model
            if mimetype:
                resp.mimetype = mimetype

            return resp
        return view_method
    return response_inner








