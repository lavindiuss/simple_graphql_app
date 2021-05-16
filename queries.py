import graphene
from .mutations import *
from .models import *
from .schema import *


class Query(graphene.ObjectType):
    # find single note
    findNote = graphene.Field(Note, id=graphene.Int())
    # get all notes by user
    user_notes = graphene.List(Note)

    def resolve_user_notes(root, info):
        # find user with uid from token
        uid = info.context['uid']
        user = session.query(UserModel).filter_by(email=uid).first()
        return user.notes

    def resolve_findNote(root, info, id):
        return session.query(NotesModel).filter_by(id=id).first()


class PreAuthQuery(graphene.ObjectType):
    all_users = graphene.List(User)

    def resolve_all_users(root, info):
        return session.query(UserModel).all()



auth_required_schema = graphene.Schema(query=Query, mutation=PostAuthMutation)
schema = graphene.Schema(query=PreAuthQuery, mutation=PreAuthMutation)