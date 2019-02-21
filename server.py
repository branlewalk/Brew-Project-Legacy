from flask import Flask, jsonify, url_for
import temp

app = Flask(__name__, static_url_path='')
sensor1 = temp.init_sensor_software(24)
sensor2 = temp.init_sensor_software(12)
sensor3 = temp.init_sensor_software(21)


@app.route('/')
def static_file(path):
    return app.send_static_file(path)


# @app.route('/raw_temp')
# def raw_temp():
#     raw = temp.read_raw_temp(sensor1)
#     return jsonify(raw)


@app.route('/HLT')
def hlt():
    raw = temp.read_raw_temp(sensor1)
    return jsonify(raw)


@app.route('/MLT')
def mlt():
    raw = temp.read_raw_temp(sensor2)
    return jsonify(raw)


@app.route('/BK')
def bk():
    raw = temp.read_raw_temp(sensor3)
    return jsonify(raw)


@app.route('/temp')
def thermo():
    return temp.read_temp(sensor1)


if __name__ == '__main__':
    app.run(debug=True, port=80, host='0.0.0.0')
