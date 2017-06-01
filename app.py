#!/usr/bin/env python

import urllib
import json
import os

from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))

    res = makeWebhookResult(req)

    res = json.dumps(res, indent=4)
    print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

def makeWebhookResult(req):
    if req.get("result").get("action") != "order":
        return {}
    result = req.get("result")
    parameters = result.get("parameters")
    type = parameters.get("type")
    size = parameters.get("size")
    crust = parameters.get("crust")
    sauce = parameters.get("sauce")

    cost = {'capricciosa':10, 'margherita':15, 'pepperoni':20, 'marinara':25}

    speech = "Wonderful! Great!! Order is" + type + "," + size + "," + sauce + "," + crust + "." + "It will be delivered to you within 30 minutes!" + "Price is $" + str(cost[type]) + "."

    print("Response:")
    print(speech)

    return {
        "speech": speech,
        "displayText": speech,
        #"data": {},
        # "contextOut": [],
        "source": "agent"
    }


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    #print "Starting app on port %d" % port

    app.run(debug=True, port=port, host='0.0.0.0')
