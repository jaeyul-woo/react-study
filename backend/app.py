from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import config

app = Flask(__name__)
app.config.from_object(config)

db = SQLAlchemy(app)

# 예제 모델 정의
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)

    def to_dict(self):
        return {"id": self.id, "username": self.username, "email": self.email}

# 테이블 생성
@app.before_first_request
def create_tables():
    db.create_all()

# CREATE
@app.route("/users", methods=["POST"])
def create_user():
    data = request.get_json()
    new_user = User(username=data["username"], email=data["email"])
    db.session.add(new_user)
    db.session.commit()
    return jsonify(new_user.to_dict()), 201

# READ
@app.route("/users", methods=["GET"])
def get_users():
    users = User.query.all()
    return jsonify([user.to_dict() for user in users])

# UPDATE
@app.route("/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    data = request.get_json()
    user = User.query.get_or_404(user_id)
    user.username = data.get("username", user.username)
    user.email = data.get("email", user.email)
    db.session.commit()
    return jsonify(user.to_dict())

# DELETE
@app.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User deleted"})

if __name__ == "__main__":
    app.run(debug=True)

