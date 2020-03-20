from flask import Flask, request
import json

fd = open('raw.json', 'r')
rawdata = json.load(fd)
# print(rawdata)

app = Flask(__name__)

@app.route('/estar')
def estar():
    mac = request.args.get('mac')
    print('==mac==',mac)
    return rawdata


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
