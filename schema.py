from .models import (
    User as UserModel, Note as NotesModel,
    session
)
from graphene_sqlalchemy import (
    SQLAlchemyConnectionField,
    SQLAlchemyObjectType
)
from typing import Optional


# types
class User(SQLAlchemyObjectType):
    class Meta:
        model = UserModel


class Notes(SQLAlchemyObjectType):
    class Meta:
        model = NotesModel

