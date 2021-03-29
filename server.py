
import pika
import json
from flask import Flask, jsonify, render_template
#import database
from brew_session import BrewSession

# from routes import recipe_blueprint, malt_ingred_blueprint, hops_ingred_blueprint, yeast_ingred_blueprint, \
#                    other_ingred_blueprint, malt_blueprint, hops_blueprint, yeast_blueprint, other_blueprint, \
#                    style_blueprint, image_blueprint, session_blueprint, temps_blueprint, step_blueprint, \
#                    session_step_blueprint

# Initializing Flask and the database (SQLAlchemy and Marshmallow)
brew_session = BrewSession()
on_off = False
app = Flask(__name__, static_url_path='')
app.url_map.strict_slashes = False
#flask_cors.CORS(app)
#database.create_app(app)

# Connection to Rabbit
parameters = pika.URLParameters('amqp://guest:guest@192.168.1.49:5672/%2F')
connection = pika.BlockingConnection(parameters)
channel = connection.channel()
channel.exchange_declare(exchange='temps', exchange_type='fanout')
channel.queue_delete(queue='current_temps')
channel.queue_declare(queue='current_temps', arguments={'x-message-ttl': 1000})
channel.queue_bind(queue='current_temps', exchange='temps')
connection.close()

# Register Routes
# app.register_blueprint(recipe_blueprint, url_prefix='/recipe')
# app.register_blueprint(malt_ingred_blueprint, url_prefix='/malt_ingred')
# app.register_blueprint(hops_ingred_blueprint, url_prefix='/hops_ingred')
# app.register_blueprint(yeast_ingred_blueprint, url_prefix='/yeast_ingred')
# app.register_blueprint(other_ingred_blueprint, url_prefix='/other_ingred')
# app.register_blueprint(malt_blueprint, url_prefix='/malt')
# app.register_blueprint(hops_blueprint, url_prefix='/hops')
# app.register_blueprint(yeast_blueprint, url_prefix='/yeast')
# app.register_blueprint(other_blueprint, url_prefix='/other')
# app.register_blueprint(style_blueprint, url_prefix='/style')
# app.register_blueprint(image_blueprint, url_prefix='/image')
# app.register_blueprint(session_blueprint, url_prefix='/session')
# app.register_blueprint(temps_blueprint, url_prefix='/temps')
# app.register_blueprint(step_blueprint, url_prefix='/step')
# app.register_blueprint(session_step_blueprint, url_prefix='/session_step')


# Template Routes
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/recipes')
def recipes():
    return render_template('recipes.html')


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
    tconnection = pika.BlockingConnection(parameters)
    tchannel = tconnection.channel()
    tchannel.exchange_declare(exchange='temps', exchange_type='fanout')
    tchannel.basic_publish(exchange='temps', routing_key='', body=json.dumps(on_off),
                           properties=pika.BasicProperties(headers={'type': 'command'}))
    tconnection.close()


# Receiving temperatures from Rabbit
@app.route('/temp')
def thermo():
    ctconnection = pika.BlockingConnection(parameters)
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
