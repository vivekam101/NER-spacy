import re
import time
from flask import Flask, request, jsonify
from flask_cors import CORS
import spacy


application = Flask(__name__)
cors = CORS(application)

@application.route('/api/predict', methods=['POST'])
def contract_predict():
    try:
        start_time = time.time()
        input_dict = request.get_json()
        print("input_dict", input_dict)
        doc = nlp(input_dict['text'].replace("\f", ""))

        # remove multiple lines and spaces
        arg = input_dict['text']
        arg = re.sub(r'\t+', ' ', arg)
        arg = re.sub(r'\n+', '\n', arg)

        attributes = []
        for entity in doc.ents:
            if entity.label_ in ["PERSON", "ORG", "GPE", "PRODUCT", "DATE", "TIME", "MONEY", "LAW"]:
                attributes.append({'name': entity.label_, 'value': entity.text})

        print("total time taken", time.time() - start_time)
        result = {
            'attributes': attributes,
            'preprocessed_text': arg
        }
    except Exception as e:
        result = {
            'status': 'error',
            'code': e,
        }
    return jsonify(result)


if __name__ == '__main__':
    nlp = spacy.load('en_core_web_sm')
    application.run(debug=True, threaded=True, host='0.0.0.0', port=7005)
