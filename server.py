from flask import Flask, jsonify, request
from flask.views import MethodView
from models import Session, Advertisement, User
from sqlalchemy.exc import IntegrityError, DisconnectionError
from shema import CreatAdv, UpdateAdv, CreatUser, UpdateUser
from pydantic import ValidationError
from flask_bcrypt import Bcrypt

app = Flask('my_server')
bcrypt = Bcrypt(app)

def hash_password(password: str) -> str:
    password_bytes = password.encode()
    password_hashed_bytes = bcrypt.generate_password_hash(password_bytes)
    password_hashed = password_hashed_bytes.decode()
    return password_hashed


def check_password(password: str, hashed_password: str) -> bool:
    password = password.encode()
    hashed_password = hashed_password.encode()
    return bcrypt.check_password_hash(hashed_password, password)


class HttpError(Exception):

    def __init__(self, status_code, message):
        self.status_code = status_code
        self.massage = message

@app.errorhandler(HttpError)
def error_handler(error: HttpError):
    response = jsonify({'error': error.massage})
    response.status_code = error.status_code
    return response


def validate(schema_cls: type[CreatAdv] | type[UpdateAdv] | type[CreatUser] | type[UpdateUser], json_data):
    try:
        return schema_cls(**json_data).dict(exclude_unset=True)
    except ValidationError as err:
        errors = err.errors()
        for error in errors:
            error.pop('ctx', None)
        raise HttpError(400, errors)


@app.before_request
def before_request():
    session = Session()
    request.session = session


@app.after_request
def after_request(http_response):
    request.session.close()
    return http_response

def add_user(user):
    request.session.add(user)
    try:
        request.session.commit()
    except IntegrityError as er:
        raise HttpError(409, 'user already exist')


def get_user_by_id(user_id) -> User:
    user = request.session.get(User, user_id)
    if user is None:
        raise HttpError(404, 'user not found')
    return user

class UserView(MethodView):
    def get(self, user_id: int):
        user = get_user_by_id(user_id)
        return jsonify(user.dict)

    def post(self):
        json_data = validate(CreatUser, request.json)
        user = User(name=json_data['name'], password=hash_password(json_data['password']), email=json_data['email'])
        add_user(user)
        return jsonify(user.dict)


    def patch(self, user_id: int):
        json_data = validate(UpdateUser, request.json)
        user = get_user_by_id(user_id)
        for field, value in json_data.items():
            setattr(user, field, value)
            add_user(user)
        return user.dict


    def delete(self, user_id: int):
        user = get_user_by_id(user_id)
        request.session.delete(user)
        request.session.commit()
        return jsonify({'status': 'deleted'})


def add_adv(adv):
    request.session.add(adv)
    try:
        request.session.commit()
    except IntegrityError as er:
        raise HttpError(409, 'The creator is not registered')

def get_adv_by_id(adv_id) -> Advertisement:
    adv = request.session.get(Advertisement, adv_id)
    if adv is None:
        raise HttpError(404, 'Advertisement not found')
    return adv

def val_creator_adv(json_data, adv):
    if int(json_data['creator']) != adv.creator:
        raise HttpError(403, 'You are not the creator of the adv ')
    return adv


class AdvView(MethodView):
    def get(self, adv_id: int):
        adv = get_adv_by_id(adv_id)
        return jsonify(adv.dict)

    def post(self):
        json_data = validate(CreatAdv, request.json)
        adv = Advertisement(heading=json_data['heading'], description=json_data['description'], creator=json_data['creator'])
        add_adv(adv)
        return jsonify(adv.dict)

    def patch(self, adv_id: int):
        json_data = validate(UpdateAdv, request.json)
        adv = get_adv_by_id(adv_id)
        val_creator_adv(json_data, adv)
        for field, value in json_data.items():
            setattr(adv, field, value)
            add_adv(adv)
        return adv.dict

    def delete(self, adv_id: int):
        json_data = validate(UpdateAdv, request.json)
        adv = get_adv_by_id(adv_id)
        val_creator_adv(json_data, adv)
        request.session.delete(adv)
        request.session.commit()
        return jsonify({'status': 'deleted'})

adv_view = AdvView.as_view('adv')
user_view = UserView.as_view('user')

app.add_url_rule('/adv/<int:adv_id>', view_func=adv_view, methods=['GET', 'PATCH', 'DELETE'])
app.add_url_rule('/adv', view_func=adv_view, methods=['POST'])

app.add_url_rule('/user/<int:user_id>', view_func=user_view, methods=['GET', 'PATCH', 'DELETE'])
app.add_url_rule('/user', view_func=user_view, methods=['POST'])


app.run()