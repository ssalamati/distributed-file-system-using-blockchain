import os
import json
import requests

from flask import Flask, request, send_file, make_response
from flask_cors import CORS

from file_handler import FileHandler

app = Flask(__name__)
CORS(app)

# This is a list of all the nodes in the network.
NODE_IPS = [
    # '192.168.56.11',
    # '192.168.56.12',
    # '192.168.56.13',
    # '192.168.56.14',
    # '192.168.56.15',
]

"""
The format of the following dict is like this:
{
    <file hash>: {<part number>: <part hash>, <part number>: <part hash>, chunk_count: <count of all the parts>}
}
"""
stored_parts = {}
with open("stored_parts.json") as file:
    data = json.load(file)
    stored_parts = data

def persist_stored_parts():
    with open("stored_parts.json", "w") as file:
        file.write(json.dumps(data))

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return "No file provided", 400

    file = request.files['file']
    if file.filename == '':
        return "No file selected", 400

    file.save(os.path.join(app.root_path + "/source", file.filename))

    file_handler = FileHandler(file.filename)
    file_handler.split_file()

    meta_data = file_handler.read_meta()
    upload_file_to_network(file_handler)
    return meta_data["file_hash"], 200


@app.route('/download/<file_hash>', methods=['GET'])
def download(file_hash):
    download_file_from_network(file_hash)
    return send_file('source/response'), 200


@app.route('/upload_chunk', methods=['POST'])
def upload_chunk():
    if 'file' not in request.files:
        return "No file provided", 400
    file = request.files['file']
    part_number = request.form.get('part_number')
    part_hash = request.form.get('part_hash')
    file_hash = request.form.get('file_hash')
    chunk_count = request.form.get('chunk_count')
    if stored_parts.get(file_hash):
        stored_parts[file_hash][part_number] = part_hash
    else:
        stored_parts[file_hash] = {part_number: part_hash, 'chunk_count': chunk_count}
    persist_stored_parts()

    file.save(os.path.join(app.root_path + "/parts", part_hash))
    return {'result': 'success'}


@app.route('/download_chunk', methods=['GET'])
def download_chunk():
    file_hash = request.form.get('file_hash')
    part_number = request.form.get('part_number')
    if not stored_parts.get(file_hash):
        return {'result': 'no-file'}
    if not stored_parts[file_hash][part_number]:
        return {'result': 'no-file'}
    part_hash = stored_parts[file_hash][part_number]
    file_data = open('parts/' + part_hash, 'rb').read()
    response = make_response(file_data)
    response.headers['Content-Disposition'] = f'attachment; filename={part_hash}'
    return response


@app.route('/get_chunk_count', methods=['GET'])
def get_chunk_count():
    file_hash = request.form.get('file_hash')
    if not stored_parts.get(file_hash):
        return {'result': 'no-file'}
    return {'chunk_count': stored_parts[file_hash]['chunk_count']}


def upload_file_to_network(file_handler: FileHandler):
    meta_data = file_handler.read_meta()
    parts = meta_data["parts"]
    file_hash = meta_data["file_hash"]
    chunk_count = meta_data["chunk_count"]

    for part_number, part_hash in parts.items():
        data = {'file_hash': file_hash, 'part_number': part_number, 'part_hash': part_hash, 'chunk_count': chunk_count}
        with open('parts/' + part_hash, 'rb') as file:
            file_data = file.read()
        for node_ip in NODE_IPS:
            response = requests.post(node_ip + '/upload_chunk', files={'file': file_data}, data=data)
        if stored_parts.get(file_hash):
            stored_parts[file_hash][part_number] = part_hash
        else:
            stored_parts[file_hash] = {part_number: part_hash, 'chunk_count': chunk_count}
        persist_stored_parts()


def download_file_from_network(file_hash: str):
    chunks_count = 0
    # In this part, this node will understand the number of chunks of this file
    if stored_parts.get(file_hash):
        chunks_count = stored_parts[file_hash]['chunk_count']
    else:
        for node_ip in NODE_IPS:
            data = {'file_hash': file_hash}
            response = requests.get(node_ip + '/get_chunk_count', data=data)
            if response.json()['result'] == 'no-file':
                continue
            chunks_count = response.json()['chunk_count']
            break

    # In this part, this node will gather all the chunks of the file
    for part_number in range(chunks_count):
        part_number = str(part_number)
        if stored_parts.get(file_hash) and stored_parts[file_hash][part_number]:
            continue
        data = {'file_hash': file_hash, 'part_number': part_number}
        for node_ip in NODE_IPS:
            response = requests.get(node_ip + '/download_chunk', data=data)
            if response.json()['result'] == 'no-file':
                continue
            part_hash = response.headers['Content-Disposition'].split('=')[1]
            with open('parts/' + part_hash, 'wb') as f:
                f.write(response.content)
            if stored_parts.get(file_hash):
                stored_parts[file_hash][part_number] = part_hash
            else:
                stored_parts[file_hash] = {part_number: part_hash, 'chunk_count': chunks_count}
            persist_stored_parts()
            break

    # In this part, this node will combine all the parts to send it back to the user
    chunk_count = stored_parts[file_hash]['chunk_count']
    file_path = 'response'
    parts = stored_parts[file_hash]
    with open('source/' + file_path, 'wb') as output_file:
        # Iterate over the chunks and write them to the output file
        for i in range(0, chunk_count):
            part_hash = parts[str(i)]
            chunk_file_path = 'parts/' + part_hash
            with open(chunk_file_path, 'rb') as chunk_file:
                output_file.write(chunk_file.read())


if __name__ == '__main__':
    app.run(debug=True)
