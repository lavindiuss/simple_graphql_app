#!/usr/bin/env python3
from flask import Flask, request, jsonify
from flask_graphql import GraphQLView
from extensions import bcrypt, auth, jwt
from .queries import auth_required_schema, schema
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token, get_jwt_identity,
    jwt_required
)
import os
from .models import User, session


app = Flask(__name__)
app.config['SECRET_KEY'] = "testest"
app.config['JWT_SECRET_KEY'] = "testtest"

bcrypt.init_app(app)
auth.init_app(app)
jwt.init_app(app)