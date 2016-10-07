from flask import Flask, request, jsonify
from flasgger import Swagger, swag_from
from nameko.standalone.rpc import ClusterRpcProxy

app = Flask(__name__)
Swagger(app)
CONFIG = {'AMQP_URI': "#AMQP#"}


@app.route('/best_price/<int:item_id>', methods=['POST'])
@swag_from('api_files/best_price.yml')
def compute():
    item_id = request.json.get('item_id')

    # msg = "Please wait the calculation, you'll receive an email with results"
    # subject = "API Notification"
    #
    # with ClusterRpcProxy(CONFIG) as rpc:
    #     # asynchronously spawning and email notification
    #     rpc.mail.send.async(email, subject, msg)
    #     # asynchronously spawning the compute task
    #     result = rpc.compute.compute.async(operation, value, other, email)
    #     return msg, 200
    return jsonify({'item_id': item_id, 'best_price', 15})

if __name__ == '__main__':
    app.run(debug=True)
