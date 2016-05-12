from flask import Flask, request, send_file, Response
from pprint import pprint
from pprint import pformat
from pymongo import MongoClient
from bson.json_util import loads, dumps
from bson import ObjectId

con = MongoClient()
col = con.socket

app = Flask(__name__)

@app.route('/')
def index() :
    return send_file('index.html')

@app.route('/logs')
def logs() :
    return Response(dumps(col.log.find().limit(10).sort('time', -1), encoding="UTF-8"), status=200, mimetype="application/json")

@app.route('/delete', methods=["GET"])
def drule() :
    try :
        ruleid = ObjectId(request.args.get('ruleid'))
        col.rules.remove({'_id':ruleid})
    except :
        return dumps({'error':True})
    return dumps({'success':True})

@app.route('/rules', methods=["GET","POST"])
def rules() :

    if request.method == 'POST' :
        try :
            data = request.get_json()
            rule = data.get('rules')
            pattern = str(rule.get('pattern'))
            match = rule.get('match')
            typeof = rule.get('type')
            valof = rule.get('val')
            action = rule.get('action')+"\r\n"
            title = rule.get('title')
            res = {
                "title" : title,
                "condition" : {
                    pattern:match
                },
                # There can only be one exec, it returns 'result' to the action
                "exec" : {
                    "type" : typeof,
                    "value" : valof,
                },
                "actions" : [
                    action
                ]
            }
            col.rules.insert(res)
            return dumps(res)
        except :
            return dumps({'error':True})
    return Response(dumps(col.rules.find(), encoding="UTF-8"), status=200, mimetype="application/json")

@app.route('/api', methods=["GET","POST"])
def api() :
    return ''


if __name__ == '__main__' :
    app.debug = True
    app.run(host="0.0.0.0", port=5000)
