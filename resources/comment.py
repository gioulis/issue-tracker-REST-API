from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError

from db import db
from models import CommentModel
from schemas import CommentSchema

blp = Blueprint("Comments", "comments", description="Operations on comments")


@blp.route("/comment/<string:comment_id>")
class Comment(MethodView):
    @blp.response(200, CommentSchema)
    def get(self, comment_id):
        comment = CommentModel.query.get_or_404(comment_id)
        return comment

    def delete(self, comment_id):
        comment = CommentModel.query.get_or_404(comment_id)
        db.session.delete(comment)
        db.session.commit()
        return {"message": "Comment deleted."}


@blp.route("/comment")
class CommentList(MethodView):
    @blp.response(200, CommentSchema(many=True))
    def get(self):
        return CommentModel.query.all()

    @blp.arguments(CommentSchema)
    @blp.response(201, CommentSchema)
    def post(self, comment_data):
        comment = CommentModel(**comment_data)

        try:
            db.session.add(comment)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the comment.")

        return comment
