from flask import Flask, jsonify, request
from connection import collection
import base64

app = Flask(__name__)

# Define API endpoint to fetch data
@app.route('/api/data', methods=['GET'])
def get_data():
    response_dict = {}
    if request.method == 'GET':
        userName = request.args.get('userName')
        if userName:
            data = list(collection.find({"userName":userName}, {"_id":0}))
            if isinstance(data[0]['profilePicture'], bytes):
                data[0]['profilePicture'] = base64.b64encode(data[0]['profilePicture']).decode('utf-8')
            else:
                data[0]['profilePicture'] = data[0]['profilePicture']
            return jsonify({"data":data[0], "status":200}), 200
        else:
            return {"message":"user name is missing, Please check.", "status":404}, 404

if __name__ == '__main__':
    app.run(debug=True)
