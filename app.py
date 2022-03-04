from flask import Flask
from flask import render_template
from flask import Response, request, jsonify, abort
from flask_restful import fields, marshal_with, marshal
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc
import random
import string

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///players.db'
db = SQLAlchemy(app)

class PlayerModel(db.Model):
    player_id = db.Column(db.String, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    xp = db.Column(db.Integer, nullable=False)
    gold = db.Column(db.Integer, nullable=False)

resource_fields = {
    'player_id':fields.String,
    'username':fields.String,
    'xp':fields.Integer,
    'gold':fields.Integer
}


@app.route("/api/v1/player/", methods=['POST', 'GET'])
def create_player():
    if request.method == 'POST':
        username = request.form.get('username')

        # get username and generate player id randomly to add to players list
        numbers = ''.join(random.choice(string.digits) for i in range(3))
        letters = ''.join(random.choice(string.ascii_lowercase) for i in range(3))
        player_id = numbers + letters
        new_player = PlayerModel(player_id=player_id, username=username, xp=9999, gold=0)
        db.session.add(new_player)
        db.session.commit()

        return {'username': username, 'player_id': player_id}, 200

    return render_template('create.html')


@app.route("/api/player/<player_id>/", methods=['GET'])
@marshal_with(resource_fields)
def view_player(player_id=None):
    result = PlayerModel.query.filter_by(player_id=player_id).first()

    if result:
        return result

    abort(400, {'error_message': "The player you are looking for does not exist, please try a differen one"})


@app.route("/api/player/update/<player_id>/", methods=['POST', 'PUT', 'GET'])
def update_player(player_id=None):
    result = PlayerModel.query.filter_by(player_id=player_id).first()
    if result:
        if request.method == 'POST':
            username = request.form.get('username')
            xp = request.form.get('xp')
            gold = request.form.get('gold')

            if username:
                result.username = username
            if xp:
                result.xp = xp
            if gold:
                result.gold = gold

            db.session.commit()
            return marshal(result, resource_fields), 200

        return render_template('update.html', player_id=player_id)

    abort(400, {'error_message': "The player you are trying to update for does not exist, please try a differen one"})


@app.route("/api/leaderboards/", methods=['POST','GET'])
def leader_boards():
    if request.method == 'POST':
        sortby = request.form.get('sortby')
        size = int(request.form.get('size'))

        if sortby != "gold" and sortby != "xp":
            abort(400, {'error_message': "You can only sort by gold or xp, please try again"})

        if size < 0:
            size = 0
        elif size > PlayerModel.query.count():
            size = PlayerModel.query.count()

        # sort players by sortby
        if sortby == "gold":
            results = PlayerModel.query.order_by(PlayerModel.gold.desc()).limit(size)
        else:
            results = PlayerModel.query.order_by(PlayerModel.xp.desc()).limit(size)

        res = []
        for result in results:
            res.append(marshal(result, resource_fields))

        return jsonify(res), 200

    return render_template('top.html')


if __name__ == '__main__':
    app.run(debug = True)
