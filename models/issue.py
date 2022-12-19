from db import db


class IssueModel(db.Model):
    __tablename__ = "issues"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), unique=True, nullable=False)
    status = db.Column(db.String(10), default="unresolved", nullable=False)
    body = db.Column(db.String(1000), nullable=False)

    comments = db.relationship("CommentModel", back_populates="issue", lazy="dynamic", cascade="all, delete")
