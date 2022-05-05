from api import api, app
from api.resources.quote import QuoteResource
from api.resources.author import AuthorResource
from api.resources.user import UserResource
from api.resources.token import TokenResource
from config import Config

api.add_resource(QuoteResource,
                 '/authors/<int:author_id>/quotes/<int:quote_id>',
                 '/authors/<int:author_id>/quotes',
                 '/quotes'
                 )  # <-- requests
api.add_resource(AuthorResource,
                 '/authors/<int:author_id>',
                 '/authors')  # <-- requests
api.add_resource(UserResource,
                 '/users/<int:user_id>',
                 '/users')  # <-- requests
api.add_resource(TokenResource, '/auth/token')

if __name__ == '__main__':
    app.run(debug=Config.DEBUG, port=Config.PORT)
