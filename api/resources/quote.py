from api import Resource, reqparse, db, auth
from api.models.author import AuthorModel
from api.models.quote import QuoteModel
from api.schemas.quote import quote_schema, quotes_schema


class QuoteResource(Resource):
    def get(self, author_id=None, quote_id=None):
        if author_id is None and quote_id is None:  # Если запрос приходит по url: /quotes
            quotes = QuoteModel.query.all()
            return [quote.to_dict() for quote in quotes]  # Возвращаем ВСЕ цитаты

        author = AuthorModel.query.get(author_id)
        if quote_id is None:  # Если запрос приходит по url: /authors/<int:author_id>/quotes
            quotes = author.quotes.all()
            return quotes_schema.dump(quotes), 200  # Возвращаем все цитаты автора

        quote = QuoteModel.query.get(quote_id)
        if quote is not None:
            return quote_schema.dump(quote), 200
        return {"Error": "Quote not found"}, 404

    @auth.login_required
    def post(self, author_id):
        parser = reqparse.RequestParser()
        parser.add_argument("text", required=True)
        quote_data = parser.parse_args()
        # TODO: раскомментируйте строку ниже, чтобы посмотреть quote_data
        #   print(f"{quote_data=}")
        author = AuthorModel.query.get(author_id)
        if author:
            quote = QuoteModel(author, quote_data["text"])
            db.session.add(quote)
            db.session.commit()
            return quote.to_dict(), 201
        return {"Error": f"Author id={author_id} not found"}, 404



    def put(self, quote_id):
        parser = reqparse.RequestParser()
        parser.add_argument("author")
        parser.add_argument("text")
        new_data = parser.parse_args()

        quote = QuoteModel.query.get(quote_id)
        quote.author = new_data["author"]
        quote.text = new_data["text"]
        db.session.commit()
        return quote.to_dict(), 200

    def delete(self, quote_id):
        raise NotImplemented("Метод не реализован")
