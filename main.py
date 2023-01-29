import random
from flask_bootstrap import Bootstrap
from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)

##Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
Bootstrap(app)
postman_auth_token = 'postman://auth/callback?code=916c59e50b782ae59c4bfa00efd006fd4c797eea1e6c31c5e7ababcec28b4e07'
##Cafe TABLE Configuration

class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)

    def to_dict(self):
            # Method 2. Altenatively use Dictionary Comprehension to do the same thing.
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}


@app.route("/all", methods=["GET"])
def get_all():
    # cafes_list = []
    cafes = db.session.query(Cafe).all()
    # for cafe in cafes:
    #     individual_cafe = {
    #
    #         "map_url": cafe.map_url,
    #         "img_url": cafe.img_url,
    #         "location": cafe.location,
    #         "seats": cafe.seats,
    #         "has_toilet": cafe.has_toilet,
    #         "has_wifi": cafe.has_wifi,
    #         "has_sockets": cafe.has_sockets,
    #         "can_take_calls": cafe.can_take_calls,
    #         "coffee_price": cafe.coffee_price,
    #         "name": cafe.name,
    #     }
    #     cafes_list.append(individual_cafe)
    return jsonify(cafe=[cafe.to_dict() for cafe in cafes])

@app.route("/search")
def get_cafe_at_location():
    query_location = request.args.get("loc")
    cafe = db.session.query(Cafe).filter_by(location=query_location).first()
    cafes_list = []
    if cafe:

        individual_cafe = {

            "map_url": cafe.map_url,
            "img_url": cafe.img_url,
            "location": cafe.location,
            "seats": cafe.seats,
            "has_toilet": cafe.has_toilet,
            "has_wifi": cafe.has_wifi,
            "has_sockets": cafe.has_sockets,
            "can_take_calls": cafe.can_take_calls,
            "coffee_price": cafe.coffee_price,
            "name": cafe.name,
        }
        cafes_list.append(individual_cafe)
        return jsonify(cafes_list)
    else:
        return jsonify(error={"Not Found": "Sorry, we don't have a cafe at that location."})


@app.route("/")
def home():
    return render_template("index.html")


@app.route('/random', methods=["GET", "POST"])
def random_cafe():
    cafes = db.session.query(Cafe).all()
    random_choice = random.choice(cafes)
    return jsonify(cafe={
        # id=random_cafe.id,
        "name": random_choice.name,
        "map_url": random_choice.map_url,
        "img_url": random_choice.img_url,
        "location": random_choice.location,
        "amenities":
            {
                "has_sockets": random_choice.has_sockets,
                "has_toilet": random_choice.has_toilet,
                "has_wifi": random_choice.has_wifi,
                "can_take_calls": random_choice.can_take_calls,
                "seats": random_choice.seats,
                "coffee_price": random_choice.coffee_price,
            }
    })
    # return jsonify(cafe=random_choice.to_dict())
    # all_cafes = Cafe.query.order_by(Cafe.id).all()
    # cafe_list = []
    # for cafe in all_cafes:
    #     cafe_list.append(cafe)
    # random_choice = random.choice(cafe_list)
    # return render_template('index.html', random_cafe=random_choice)
#
#
# ## HTTP GET - Read Record
#
# ## HTTP POST - Create Record
#
# ## HTTP PUT/PATCH - Update Record
#
# ## HTTP DELETE - Delete Record
#


@app.route("/add", methods=["POST"])
def post_new_cafe():
    new_cafe = Cafe(
        name=request.form.get("name"),
        map_url=request.form.get("map_url"),
        img_url=request.form.get("img_url"),
        location=request.form.get("loc"),
        has_sockets=bool(request.form.get("sockets")),
        has_toilet=bool(request.form.get("toilet")),
        has_wifi=bool(request.form.get("wifi")),
        can_take_calls=bool(request.form.get("calls")),
        seats=request.form.get("seats"),
        coffee_price=request.form.get("coffee_price"),
    )
    db.session.add(new_cafe)
    db.session.commit()
    return jsonify(response={"success": "Successfully added the new cafe."})


@app.route("/update-price/<int:cafe_id>", methods=["PATCH"])
def patch_new_price(cafe_id):
    new_price = request.args.get("new_price")
    cafe = db.session.query(Cafe).get(cafe_id)
    if cafe:
        cafe.coffee_price = new_price
        db.session.commit()
        ## Just add the code after the jsonify method. 200 = Ok
        return jsonify(response={"success": "Successfully updated the price."}), 200
    else:
        #404 = Resource not found
        return jsonify(error={"Not Found": "Sorry a cafe with that id was not found in the database."}), 404


@app.route("/report-closed/<int:cafe_id>", methods=["DELETE"])
def delete_cafe(cafe_id):
    api_key = request.args.get("api-key")
    if api_key == "TopSecretAPIKey":
        cafe = db.session.query(Cafe).get(cafe_id)
        if cafe:
            db.session.delete(cafe)
            db.session.commit()
            return jsonify(response={"success": "Successfully deleted the cafe from the database."}), 200
        else:
            return jsonify(error={"Not Found": "Sorry a cafe with that id was not found in the database."}), 404
    else:
        return jsonify(error={"Forbidden": "Sorry, that's not allowed. Make sure you have the correct api_key."}), 403




if __name__ == '__main__':
    app.run(debug=True)
