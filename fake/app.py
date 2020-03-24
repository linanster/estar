#coding:utf8
from flask import Flask, request
import json

fd = open('raw.json', 'r')
rawdata = json.load(fd)
# print(rawdata)
fd.close()

app = Flask(__name__)

@app.route('/estar')
def estar():
    mac = request.args.get('mac')
    print('==mac==',mac)
    fd = open('raw.json', 'r')
    rawdata = json.load(fd)
    # print(rawdata)
    fd.close()
    return rawdata


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
