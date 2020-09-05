import uuid
import bcrypt
import datetime

from flask import request
from flask_restplus import Namespace, Resource, fields

from model import db
from model.user import User
from model.session import Session

api = Namespace('user', description='User Management')

user_signup_model = api.model('UserSignup', {
    'id': fields.String(required=True),
    'password': fields.String(required=True)
})

@api.route('/signup')
class UserSignup(Resource):
    @api.expect(user_signup_model)
    @api.doc(responses={
        200: 'Success',
        400: 'Validation Error'
    })
    def post(self):
        """ User Sign up """

        # Validation
        if not request.is_json:
            return {"result": -1, "msg": "Missing JSON in request"}, 400

        id = request.json.get('id', None)
        password = request.json.get('password', None)
        if not id:
            return {"result": -1, "msg": "Missing id parameter"}, 400
        if not password:
            return {"result": -1, "msg": "Missing password parameter"}, 400

        user = User.query.filter_by(id=id).first()
        # id duplicate check
        # if user signouted, can make sign-up again
        re_signup_flag = False
        if user:
            if not user.signout_dt:
                return {"result": -1, "msg": "ID alreay exists"}, 400
            elif user.signout_dt:
                re_signup_flag = True

        # encrypt password using bcrypt
        password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        if re_signup_flag:
            user.password = password.decode('utf-8', 'ignore')
            user.signout_dt = None
            user.last_logout_dt = None
            user.create_dt = datetime.datetime.now()
        else:
            new_user = User(
                id=id, 
                password=password.decode('utf-8', 'ignore')
            )
            db.session.add(new_user)
        db.session.commit()

        return {"result": 0, "msg": "Signup Success"}

@api.route('/login')
class UserLogin(Resource):
    @api.expect(user_signup_model)
    @api.doc(responses={
        200: 'Success',
        400: 'Validation Error',
    })
    def put(self):
        """ User Log in """ 

        # Validation
        if not request.is_json:
            return {"result": -1, "msg": "Missing JSON in request"}, 400

        id = request.json.get('id', None)
        password = request.json.get('password', None)
        if not id:
            return {"result": -1, "msg": "Missing id parameter"}, 400
        if not password:
            return {"result": -1, "msg": "Missing password parameter"}, 400

        user = User.query.filter_by(id=id).first()
        if not user or user.signout_dt:
            return {"result": -1, "msg": "User not found"}, 400
        
        if not bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')): 
            return {"result": -1, "msg": "Bad password"}, 400

        # Make session info
        session_id = str(uuid.uuid4()).replace('-', '')[:20]
        client_ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr) # get Client IP
        session = Session(
            session_id=session_id,
            id=id,
            client_ip=client_ip
        )
        db.session.add(session)
        db.session.commit()

        return {"result": 0, "session": session_id}, 200

@api.route('/logout')
class UserLogout(Resource):
    @api.expect(api.model('logout', {'session': fields.String(required=True)}))
    @api.doc(responses={
        200: 'Success',
        400: 'Validation Error'
    })
    def delete(self):
        """ User Log out """

        # Validation
        if not request.is_json:
            return {"result": -1, "msg": "Missing JSON in request"}, 400

        session_id = request.json.get('session', None)
        if not session_id:
            return {"result": -1, "msg": "Missing session parameter"}, 400

        session = Session.query.filter_by(session_id=session_id).first()
        if not session:
            return {"result": -1, "msg": "Cannot find session"}, 400
        if session.logout_dt:
            return {"result": -1, "msg": "Already Logout"}, 400
        
        # Logout
        now = datetime.datetime.now()
        user = User.query.filter_by(id=session.id).first()
        user.last_logout_dt = now
        session.logout_dt = now
        db.session.commit()

        return {"result": 0, "msg": "[{}] Logout".format(session.id)}

@api.route('/signout')
class Signout(Resource):
    @api.expect(api.model('logout', {'session': fields.String(required=True)}))
    @api.doc(responses={
        200: 'Success',
        400: 'Validation Error'
    })
    def delete(self):
        """ User Sign out """

        # Validation
        if not request.is_json:
            return {"result": -1, "msg": "Missing JSON in request"}, 400

        session_id = request.json.get('session', None)
        if not session_id:
            return {"result": -1, "msg": "Missing session parameter"}, 400

        session = Session.query.filter_by(session_id=session_id).first()
        if not session:
            return {"result": -1, "msg": "Cannot find session"}, 400
        
        # Signout
        # User Info Change
        user = User.query.filter_by(id=session.id).first()
        now = datetime.datetime.now()
        user.signout_dt = now
        user.last_logout_dt = now
        # Session data Remove
        sessions = Session.query.filter_by(id=user.id).all()
        for sess in sessions:
            db.session.delete(sess)
        db.session.commit()

        return {"result": 0, "msg": "[{}] Signout".format(user.id)}
        
@api.route('/user/<string:id>')
class UserInfo(Resource):
    @api.doc(responses={
        200: 'Success',
        400: 'Validation Error'
    })
    def get(self, id):
        """ Get Selected User Infomations about session """

        # Valition
        if not id:
            return {"result": -1, "msg": "Missing id parameter"}, 400
        
        # if user signed out, dont show info
        user = User.query.filter_by(id=id).first()
        if not user or (user and user.signout_dt):
            return {"result": -1, "msg": "Cannot find User [{}]".format(id)}, 400

        sessions = Session.query.filter_by(id=id).all()

        # make response msg
        res = {
            "result": 0,
            "user_info": user.to_dictionary(),
            "session_info": [sess.to_dictionary() for sess in sessions]
        }

        return res, 200
