from marshmallow import Schema, fields


class PlainIssueSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True)
    status = fields.Str()
    body = fields.Str(required=True)


class PlainCommentSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str()
    body = fields.Str()


class CommentSchema(PlainCommentSchema):
    issue_id = fields.Int(required=True, load_only=True)
    issue = fields.Nested(PlainIssueSchema(), dump_only=True)


class IssueUpdateSchema(Schema):
    title = fields.Str()
    status = fields.Str()
    body = fields.Str()


class IssueSchema(PlainIssueSchema):
    comments = fields.List(fields.Nested(PlainCommentSchema()), dump_only=True)
