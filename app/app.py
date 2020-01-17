from flask_cors import CORS
from flask import Flask
from flask_restful import Api
from controllers.spliter import Splitter
from utils import ROOT_DIR

app = Flask(__name__)

# The following line is just a workround for the error: cross-origin read blocking (corb) 
# blocked cross-origin response with mime type application/json
CORS(app)

#Creation of REST API 
api = Api(app)

# Resource Routing
api.add_resource(Splitter, '/splitter')

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=80)