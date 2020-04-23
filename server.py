import json
import pika
from flask import Flask, jsonify, render_template
import flask_cors
from brew_session import BrewSession
import database
from routes import recipe_blueprint, malt_ingred_blueprint

# Initializing Flask and the database (SQLAlchemy and Marshmallow)
brew_session = BrewSession()
on_off = False

app = Flask(__name__, static_url_path='')
app.url_map.strict_slashes = False
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

# Register Routes
app.register_blueprint(recipe_blueprint, url_prefix='/recipe')
app.register_blueprint(malt_ingred_blueprint, url_prefix='/malt_ingred')

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


@app.route('/malt/<malt_id>', methods=['GET'])
def get_malt(malt_id):
    return database.MaltSchema().jsonify(database.Malt.query.get(malt_id))

# Hops Routes (Read/Read All Only)
@app.route('/hops', methods=['GET'])
def get_hops():
    return jsonify(database.HopsSchema(many=True).dump(database.Hops.query.all()))


@app.route('/hops/<hops_id>', methods=['GET'])
def get_hop(hops_id):
    return database.HopsSchema().jsonify(database.Hops.query.get(hops_id))

# Yeast Routes (Read/Read All Only)
@app.route('/yeast', methods=['GET'])
def get_yeasts():
    return jsonify(database.YeastSchema(many=True).dump(database.Yeast.query.all()))


@app.route('/yeast/<yeast_id>', methods=['GET'])
def get_yeast(yeast_id):
    return database.YeastSchema().jsonify(database.Yeast.query.get(yeast_id))


# Style Routes (Read/Read All Only)
@app.route('/style', methods=['GET'])
def get_styles():
    return jsonify(database.StyleSchema(many=True).dump(database.Style.query.all()))


@app.route('/yeast/<style_id>', methods=['GET'])
def get_style(style_id):
    return database.StyleSchema().jsonify(database.Style.query.get(style_id))


# Old Routes
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


# Send On/Off message through Rabbit to Persistor
def send_toggle():
    tconnection = pika.BlockingConnection(pika.ConnectionParameters('rabbit', 5672, '/'))
    tchannel = tconnection.channel()
    tchannel.exchange_declare(exchange='temps', exchange_type='fanout')
    tchannel.basic_publish(exchange='temps', routing_key='', body=json.dumps(on_off),
                           properties=pika.BasicProperties(headers={'type': 'command'}))
    tconnection.close()

# Receiving temperatures from Rabbit
@app.route('/temp')
def thermo():
    ctconnection = pika.BlockingConnection(pika.ConnectionParameters('rabbit', 5672, '/'))
    ctchannel = ctconnection.channel()
    for method_frame, properties, body in ctchannel.consume('current_temps'):
        print(body)
        message_type = properties.headers.get('type')
        if message_type != 'command':
            ctconnection.close()
            temp_list = json.loads(body)
            hlt = float(temp_list[0])
            mlt = float(temp_list[1])
            bk = float(temp_list[2])
            temps = {'hlt': hlt, 'mlt': mlt, 'bk': bk}
            print('Temperatures: {}'.format(temps))
            brew_session.set_temp(temps)
            return jsonify(temps)


if __name__ == '__main__':
    app.run(debug=True, port=80, host='0.0.0.0')
