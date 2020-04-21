import json
import pika
from flask import Flask, jsonify, render_template, request
import flask_cors
from brew_session import BrewSession, Recipe
import database

# Initializing Flask and the database (SQLAlchemy and Marchmallow)
brew_session = BrewSession()
on_off = False
app = Flask(__name__, static_url_path='')
flask_cors.CORS(app)
database.create_app(app)

# Connection to Rabbit
connection = pika.BlockingConnection(pika.ConnectionParameters('rabbit', 5672, '/'))
channel = connection.channel()
channel.exchange_declare(exchange='temps', exchange_type='fanout')
channel.queue_delete(queue='current_temps')
channel.queue_declare(queue='current_temps', arguments={'x-message-ttl': 1000})
channel.queue_bind(queue='current_temps', exchange='temps')
connection.close()

# Template Routes
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/recipes')
def recipes():
    return render_template('recipes.html')


# CRUD Routes for accessing JSON Data from database
# Malt Routes (Read/Read All Only)
@app.route('/malt', methods=['GET'])
def get_malts():
    return jsonify(database.MaltSchema(many=True).dump(database.Malt.query.all()))


@app.route('/malt/<id>', methods=['GET'])
def get_malt(id):
    return database.MaltSchema().jsonify(database.Malt.query.get(id))

# Hops Routes (Read/Read All Only)
@app.route('/hops', methods=['GET'])
def get_hops():
    return jsonify(database.HopsSchema(many=True).dump(database.Hops.query.all()))


@app.route('/hops/<id>', methods=['GET'])
def get_hop(id):
    return database.YeastSchema().jsonify(database.Yeast.query.get(id))

# Yeast Routes (Read/Read All Only)
@app.route('/yeast', methods=['GET'])
def get_yeasts():
    return jsonify(database.YeastSchema(many=True).dump(database.Yeast.query.all()))


@app.route('/yeast/<id>', methods=['GET'])
def get_yeast(id):
    return database.HopsSchema().jsonify(database.Hops.query.get(id))

# Recipe Routes (Create, Read/Read All, Update, Delete)
@app.route('/recipe', methods=['POST'])
def add_recipe():
    print('Request: {}'.format(request))
    recipe_name = request.json['recipe_name']

    recipe_method = request.json['recipe_method']
    recipe_srm = request.json['recipe_srm']
    recipe_batch_size = request.json['recipe_batch_size']
    recipe_rating = request.json['recipe_rating']
    recipe_description = request.json['recipe_description']
    style_id = request.json['style_id']
    image_id = request.json['image_id']

    recipe = database.Recipe(recipe_name, recipe_method, recipe_srm, recipe_batch_size, recipe_rating,
                             recipe_description, style_id, image_id)

    database.db.session.add(recipe)
    database.db.session.commit()

    return database.RecipeSchema().jsonify(recipe)


@app.route('/recipe', methods=['GET'])
def get_recipes():
    return jsonify(database.RecipeSchema(many=True).dump(database.Recipe.query.all()))


@app.route('/recipe/<id>', methods=['GET'])
def get_recipe(id):
    return database.RecipeSchema().jsonify(database.Recipe.query.get(id))


@app.route('recipe/<id>', methods=['PUT'])
def update_recipe(id):
    pass


@app.route('recipe/<id>', methods=['DELETE'])
def delete_recipe(id):
    pass


# Recipe Routes (Create, Read/Read All, Update, Delete)
@app.route('/recipe', methods=['POST'])
def add_recipe():
    print('Request: {}'.format(request))
    recipe_name = request.json['recipe_name']

    recipe_method = request.json['recipe_method']
    recipe_srm = request.json['recipe_srm']
    recipe_batch_size = request.json['recipe_batch_size']
    recipe_rating = request.json['recipe_rating']
    recipe_description = request.json['recipe_description']
    style_id = request.json['style_id']
    image_id = request.json['image_id']

    recipe = database.Recipe(recipe_name, recipe_method, recipe_srm, recipe_batch_size, recipe_rating,
                             recipe_description, style_id, image_id)

    database.db.session.add(recipe)
    database.db.session.commit()

    return database.RecipeSchema().jsonify(recipe)


@app.route('/recipe', methods=['GET'])
def get_recipes():
    return jsonify(database.RecipeSchema(many=True).dump(database.Recipe.query.all()))


@app.route('/recipe/<id>', methods=['GET'])
def get_recipe(id):
    return database.RecipeSchema().jsonify(database.Recipe.query.get(id))


@app.route('recipe/<id>', methods=['PUT'])
def update_recipe(id):
    pass


@app.route('recipe/<id>', methods=['DELETE'])
def delete_recipe(id):
    pass

@app.route('/session')
def session():
    return jsonify(brew_session.prompt())


@app.route('/timer')
def timer():
    brew_session.timer()
    return 'Ok'


@app.route('/session', methods=['POST'])
def toggle():
    brew_session.toggle_step()
    return session()


def send_toggle():
    tconnection = pika.BlockingConnection(pika.ConnectionParameters('rabbit', 5672, '/'))
    tchannel = tconnection.channel()
    tchannel.exchange_declare(exchange='temps', exchange_type='fanout')
    tchannel.basic_publish(exchange='temps', routing_key='', body=json.dumps(on_off),
                           properties=pika.BasicProperties(headers={'type': 'command'}))
    tconnection.close()


@app.route('/temp')
def thermo():
    print("Calling thermo")
    ctconnection = pika.BlockingConnection(pika.ConnectionParameters('rabbit', 5672, '/'))
    ctchannel = ctconnection.channel()
    for method_frame, properties, body in ctchannel.consume('current_temps'):
        print(body)
        message_type = properties.headers.get('type')
        if message_type != 'command':
            ctconnection.close()
            # all_temps = read_sensor()
            temp_list = json.loads(body)
            hlt = float(temp_list[0])
            mlt = float(temp_list[1])
            bk = float(temp_list[2])
            temps = {'hlt': hlt, 'mlt': mlt, 'bk': bk}
            print(temps)
            brew_session.set_temp(temps)
            return jsonify(temps)


if __name__ == '__main__':
    app.run(debug=True, port=80, host='0.0.0.0')
