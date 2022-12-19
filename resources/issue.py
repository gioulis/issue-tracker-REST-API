from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from db import db
from models import IssueModel
from schemas import IssueSchema, IssueUpdateSchema


blp = Blueprint("Issues", "issues", description="Operations on issues")


@blp.route("/issue/<string:issue_id>")
class Issue(MethodView):
    @blp.response(200, IssueSchema)
    def get(self, issue_id):
        issue = IssueModel.query.get_or_404(issue_id)
        return issue

    def delete(self, issue_id):
        issue = IssueModel.query.get_or_404(issue_id)
        db.session.delete(issue)
        db.session.commit()
        return {"message": "Issue deleted"}, 200

    @blp.arguments(IssueUpdateSchema)
    @blp.response(200, IssueSchema)
    def put(self, issue_data, issue_id):
        issue = IssueModel.query.get(issue_id)

        if issue:
            issue.title = issue_data["title"]
            issue.status = issue_data["status"]
            issue.body = issue_data["body"]
        else:
            issue = IssueModel(id=issue_id, **issue_data)

        db.session.add(issue)
        db.session.commit()

        return issue


@blp.route("/issue")
class IssueList(MethodView):
    @blp.response(200, IssueSchema(many=True))
    def get(self):
        query_args = request.args
        if "status" in query_args.keys():
            return IssueModel.query.filter_by(status=query_args["status"])
        return IssueModel.query.all()

    @blp.arguments(IssueSchema)
    @blp.response(201, IssueSchema)
    def post(self, issue_data):
        issue = IssueModel(**issue_data)
        try:
            db.session.add(issue)
            db.session.commit()
        except IntegrityError:
            abort(
                400,
                message="A issue with that title already exists.",
            )
        except SQLAlchemyError:
            abort(500, message="An error occurred creating the issue.")

        return issue
