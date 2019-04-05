from flask import Flask, jsonify, url_for, render_template
from thermo import read_sensor
import thermo

app = Flask(__name__, static_url_path='')
# sensor1 = temp.init_sensor_software(24)
# sensor2 = temp.init_sensor_software(12)
# sensor3 = temp.init_sensor_software(21)


@app.route('/')
def index():
    return render_template('index.html')


# @app.route('/raw_temp')
# def raw_temp():
#     raw = temp.read_raw_temp(sensor1)
#     return jsonify(raw)


# @app.route('/HLT')
# def hlt():
#     raw = temp.read_raw_temp(sensor1)
#     return jsonify(raw)
#
#
# @app.route('/MLT')
# def mlt():
#     raw = temp.read_raw_temp(sensor2)
#     return jsonify(raw)
#
#
# @app.route('/BK')
# def bk():
#     raw = temp.read_raw_temp(sensor3)
#     return jsonify(raw)


@app.route('/temp')
def thermo():
    all_temps = read_sensor()
    hlt = all_temps[0][1]
    mlt = all_temps[1][1]
    bk = all_temps[2][1]
    return jsonify({'hlt': "{0:4.1f}".format(hlt), 'mlt': "{0:4.1f}".format(mlt), 'bk': "{0:4.1f}".format(bk)})



if __name__ == '__main__':
    app.run(debug=True, port=80, host='0.0.0.0')
