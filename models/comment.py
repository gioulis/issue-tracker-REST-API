from db import db


class CommentModel(db.Model):
    __tablename__ = "comments"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), unique=False, nullable=False)
    body = db.Column(db.String(1000), unique=False, nullable=False)

    issue_id = db.Column(
        db.Integer, db.ForeignKey("issues.id"), unique=False, nullable=False
    )
    issue = db.relationship("IssueModel", back_populates="comments")
