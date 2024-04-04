from flask import Flask
from src import resume_generator

app = Flask(__name__, static_url_path="", static_folder="public")

@app.route("/resume/generate", methods=['POST'])
def create_resume():
    return resume_generator.create_resume_()

if __name__ == '__main__':
    resume_generator.create_resume_()
    app.run(host='0.0.0.0', port=80, debug=True)