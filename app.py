#!/usr/bin/env python3
from settings import *

@app.route('/')
def index():
    return "Go to /graphql"


@app.route('/login', methods=['POST'])
def login():
    # fetch login credentials
    data = request.get_json(force=True)
    # find user
    user = session.query(User).filter_by(email=data['email']).first()
    if not user:
        return {
            "ok":True,
            "message": "User with email not found"
        }, 404
        
    if bcrypt.check_password_hash(user.password, data['password']):
        token = create_access_token(identity=data['email'])
        return jsonify(access_token=token)
    return {
        "ok":True,
        "message": "Incorrect password"
    }, 401


def graphql():
    view = GraphQLView.as_view(
        'graphql',
        schema=auth_required_schema,
        graphiql=True,
        get_context=lambda: {
            'session': session,
            'request':request,
            'uid': get_jwt_identity()
        }
    )
    return jwt_required(view)


app.add_url_rule(
    '/graphql',
    view_func=graphql()
)

app.add_url_rule(
    '/graphq',
    view_func=GraphQLView.as_view(
        'graphq',
        schema=schema,
        graphiql=True
    )
)