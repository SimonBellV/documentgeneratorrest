from . import api_blueprint as api
from .services.document_worker import DocumentWorker, DocumentWorkerException
import json
from flask import jsonify, request, send_file
from genshi.template.eval import UndefinedError


""""@api.route('/v1.01/document/', methods=['POST'])
def document_v1():
    if request.files['file']:
        document = request.files['file']
        ext = request.form['extension']
        data = json.loads(request.form['data'])
        return send_file(BytesIO(document.read()), attachment_filename=document.filename, as_attachment=True)"""


@api.route('/v1.02/document/', methods=['GET'])
def document_v2():
    try:
        if request.files.get('template') and request.files.get('data') and request.form.get('extension'):
            data = json.load(request.files['data'])
            worker = DocumentWorker(request.files['template'], request.form['extension'], data)
            document, filename = worker.render_template()
            return send_file(document, attachment_filename=filename, as_attachment=True)
        else:
            return jsonify({'message': 'Incorrect request params!'}), 400
    except DocumentWorkerException as e:
        return jsonify({'message': e.args[0]}), 400
    except UndefinedError:
        return jsonify({'message': 'Not enough JSON params!'}), 400
    except (json.decoder.JSONDecodeError, UnicodeDecodeError):
        return jsonify({'message': 'Incorrect JSON file data!'}), 400
