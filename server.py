from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_security import *
from flask_mail import Mail
from flask_jsonpify import jsonify 

from flask_json import FlaskJSON, JsonError, json_response, as_json
from flask_restful import reqparse, abort, Api, Resource





# Security, SQLAlchemyUserDatastore, UserMixin, RoleMixin, login_required, current_user

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from datetime import datetime

# Create app

app = Flask(__name__,static_url_path='/static')
app.config.from_pyfile('settings/config.py')

# Create API 
api = Api(app)
FlaskJSON(app)

# Create database connection object
db = SQLAlchemy(app)

# Database Mirgration set up 
migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

mail = Mail(app)

# Define models
roles_users = db.Table('roles_users',
        db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
        db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))

posts_users = db.Table('comments_users', 
		db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
		db.Column('post_id', db.Integer(), db.ForeignKey('post.id'))
	)

users_friends = db.Table('users_friends',
		db.Column('user1_id', db.Integer(), db.ForeignKey('user.id')),
		db.Column('friend_id', db.Integer(), db.ForeignKey('friend.id'))
	)


class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Role', secondary=roles_users,backref=db.backref('users', lazy='dynamic'))


class Friend(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer())
	requested_at = db.Column(db.DateTime())
	confirmed = db.Column(db.Boolean())
	confirmed_at = db.Column(db.DateTime()) 
	friend = db.relationship('User', secondary=users_friends,backref=db.backref('friends', lazy='dynamic'))

class Post(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	text = db.Column(db.Text())
	timeStamp = db.Column(db.DateTime())
	user = db.relationship('User', secondary=posts_users,backref=db.backref('post', lazy='dynamic'))



# db.session.add(new_user)
# db.session.commit()


# Setup Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)


@app.route('/')
def index():
	return render_template('index.html')

@app.route('/homepage')
@login_required
def home():
	# comments = Post.query.filter(Post.user_id==current_user.id)

	comments = Post.query.filter(User.id == current_user.id).join(Post.user)
	friends = Friend.query.filter(User.id == current_user.id).join(Friend.friend)[0]

	return render_template('home.html', comments=comments, friends=friends)

@app.route('/add_friend', methods=["POST", "GET"])
@login_required
def addFriend():
	if request.method == "POST":
		email = request.form['email']
		requested_user = User.query.filter(User.email==email).one()

		friend_request = Friend(
				user_id = requested_user.id,
				requested_at = datetime.now(),
				confirmed = False
			)
		friend_request.friend.append(current_user)
		db.session.add(friend_request)
		db.session.commit()

		return redirect(url_for("home"))
	return render_template('add_friend.html')

@app.route('/comment', methods=["POST", "GET"])
@login_required
def save_comments():
	if request.method == "POST":
		comment = request.form['comment']
		
		new_comment = Post(
				text = comment,
				timeStamp = datetime.now()
			)

		new_comment.user.append(current_user)

		db.session.add(new_comment)
		db.session.commit()

		return redirect(url_for("home"))

	return redirect(url_for("home"))



@app.route('/feed')
@login_required
def feed():
	return render_template('feed.html')



COMMENTS = [
	{'id':1, 'comment':'This is cool!!'},
	{'id':2, 'comment':'This is really cool!!'},
	{'id':3, 'comment':'This is actually very cool!!'}
]


def abort_if_comment_doesnt_exist(comment_id):
	if any(x['id'] == int(comment_id )for x in COMMENTS) == False:
		abort(404, message="Comment {} doesn't exist".format(comment_id))

parser = reqparse.RequestParser()
parser.add_argument('comment')

# Shows a single comment item and lets you delete a comment
class Comment(Resource):
	def get(self, comment_id):
		abort_if_comment_doesnt_exist(comment_id)
		comment = next((l for l in COMMENTS if l['id'] == int(comment_id)))
		return comment

	def delete(self, comment_id):
		abort_if_comment_doesnt_exist(comment_id)
		comment = next((l for l in COMMENTS if l['id'] == comment_id))
		del comment
		return '', 204

	def put(self, comment_id):
		args = parser.parse_args()
		new_comment = {'comment':args['comment']}
		comment = next((l for l in COMMENTS if l['id'] == comment_id))
		comment = new_comment 
		return task, 201

# Comment List
# shows a list of all comments, and lets you POST to add new comments
class CommentList(Resource):
	def get(self):
		return jsonify(COMMENTS)

	def post(self):
		args = parser.parse_args()
		comment_id = COMMENTS[-1]['id'] + 1 
		COMMENTS.append({'id':comment_id, 'comment':args['comment']})
		index = (len(COMMENTS)-1)
		return jsonify(COMMENTS[index], 201)

##
## Setting up the Api resource routing
##

api.add_resource(CommentList, '/comments')
api.add_resource(Comment, '/comments/<comment_id>')



if __name__ == '__main__':
    # manager.run()
    app.run()