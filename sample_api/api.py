from flask import Flask, request
from pprint import pprint
from json import loads, dumps
import urbandict


app = Flask(__name__)

@app.route('/', methods=["GET", "POST"])
def index() :
        
    try :
        data = loads(request.get_json())
        args = data.get('args')
    except :
        return dumps({"result":"something broke"})

    pprint(data)

    try :
        action = args[3]
    except :
        return dumps({"result":"Invalid JSON arguments"})

    if action == ':!define':
        term = " ".join(args[4:])
        res = urbandict.define(term)
        defi = res[0].get('def').strip()
        return dumps({'result' : defi})

    return dumps({"result":"noop"})

if __name__ == '__main__' :
    app.debug = True
    app.run(port=5000, host="0.0.0.0")

