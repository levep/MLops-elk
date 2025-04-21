from configs import input_config, preprocessing_config, model_config
from src.appLogger import AppLogger
from src.input_manager import InputManager
from src.model_manager import ModelManager
from src.preprocessingManager import PreprocessingManager
from flask import Flask, request, jsonify
import pandas as pd

app = Flask(__name__)
inputManager = InputManager(input_config)
preprocessing = PreprocessingManager(preprocessing_config)
modelManager = ModelManager(model_config)
appLogger = AppLogger()
inputs_params = ['Pclass', 'Sex', 'Age', 'SibSp', 'Parch', 'Fare', 'Cabin', 'Embarked']

@app.route('/predict', methods=['GET'])
def getPredict():
    request_body = request.get_json()
    appLogger.getLogger().info(f"getPredict invoke with {request_body}")
    missing_keys = [key for key in inputs_params if key not in request_body.keys()]

    if len(missing_keys) > 0:
        response = {'error': 'Bad Request', 'message': f'Missing required parameter/s:{missing_keys}'}
        return jsonify(response, 400)

    dataset = pd.DataFrame([[request_body['Pclass'],
                            request_body['Sex'],
                            request_body['Age'],
                            request_body['SibSp'],
                            request_body['Parch'],
                            request_body['Fare'],
                            request_body['Cabin'],
                            request_body['Embarked']]], columns=inputs_params)

    process_dataset = preprocessing.processData(dataset)
    result = modelManager.predict(process_dataset)
    appLogger.getLogger().info(f"getPredict result with {result}")
    return jsonify({"predict_result":int(result[0])}, 200)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9999)


    # dataset = inputManager.getData()
    # process_dataset = preprocessing.processData(dataset)
    # result = modelManager.predict(process_dataset)
    # print(process_dataset.columns)
    # print(result)

    # output
