from flask import Flask, request

app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload_file():
    uploaded_file = request.files['file']
    if uploaded_file.filename != '':
        uploaded_file.save(uploaded_file.filename)
        # Process the uploaded file here
        return 'File uploaded successfully.'
    else:
        return 'No file selected.'

if __name__ == '__main__':
    app.run(debug=True)