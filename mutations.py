import graphene
from extensions import bcrypt
from .schema import User, UserModel, session, Note, NotesModel

class createUser(graphene.Mutation):
    class Arguments:
        first_name = graphene.String()
        last_name = graphene.String()
        email = graphene.String()
        password = graphene.String()
    ok = graphene.Boolean()
    user = graphene.Field(User)

    def mutate(root, info, first_name, last_name, email, password):
        new_user = UserModel(
            first_name = first_name,
            last_name = last_name,
            email = email,
            password = str(
                bcrypt.generate_password_hash(password),
                'utf-8'
            )
        )
        session.add(new_user)
        session.commit()
        ok = True
        return createUser(ok=ok, user=new_user)


class addNote(graphene.Mutation):
    class Arguments:
        title = graphene.String()
        body = graphene.String()
    ok = graphene.Boolean()
    note = graphene.Field(Note)

    def mutate(root, info, title, body):
        uid = info.context['uid']
        # find user based on token payload
        user = session.query(UserModel).filter_by(email=uid).first()
        new_note = NotesModel(
            title=title,
            body=body,
            user=user
        )
        session.add(new_note)
        session.commit()
        ok = True
        return addNote(ok=ok, note=new_note)


# delete note
class deleteNote(graphene.Mutation):
    class Arguments:
        id = graphene.Int()
    ok = graphene.Boolean()
    note = graphene.Field(Note)

    def mutate(root, info, id):
        note = session.query(NotesModel).filter_by(id=id).first()
        session.delete(note)
        ok = True
        note = note
        session.commit()
        return deleteNote(ok=ok, note=note)


# update existing note
class updateNote(graphene.Mutation):
    class Arguments:
        note_id = graphene.Int()
        title = graphene.String()
        body = graphene.String()
    ok = graphene.Boolean()
    note = graphene.Field(Note)

    def mutate(root, info, note_id, title: Optional[str]=None, body: Optional[str]=None):
        # find note object
        note = session.query(NotesModel).filter_by(id=note_id).first()
        if not title:
            note.body = body
        elif not body:
            note.title = title
        else:
            note.title = title
            note.body = body
        session.commit()
        ok = True
        note = note
        return updateNote(ok=ok, note=note)


class PostAuthMutation(graphene.ObjectType):
    addNote = addNote.Field()
    updateNote = updateNote.Field()
    deleteNote = deleteNote.Field()


class PreAuthMutation(graphene.ObjectType):
    create_user = createUser.Field()
