import os
import json
from flask import Flask, request, render_template, jsonify
import vertexai
from vertexai import language_models

class Config:
    GOOGLE_APPLICATION_CREDENTIALS = 'C:/Users/neosu/webapp3/mlproj1-403203-c24f2a45ebd5.json'
    PROJECT_ID = "mlproj1-403203"
    LOCATION = "us-central1"
    ALLOWED_EXTENSIONS = {'txt', 'json'}
    UPLOAD_FOLDER = "C:/Users/neosu/webapp3/temp"

class VertexAIAnalyzer:
    def __init__(self, project_id, location):
        vertexai.init(project=project_id, location=location)
        self.chat_model = language_models.CodeChatModel.from_pretrained("codechat-bison")

    def analyze_error_logs(self, error_logs):
        try:
            error_logs = [error_log.strip() for error_log in error_logs]
            chat = self.chat_model.start_chat()
            for error_log in error_logs:
                chat.send_message(error_log)
            analysis_results = chat.get_analysis_results()
        except Exception as e:
            analysis_results = {"error": str(e)}
        return analysis_results

app = Flask(__name__)

analyzer = VertexAIAnalyzer(Config.PROJECT_ID, Config.LOCATION)

@app.route("/", methods=["GET", "POST"])
def handle_main_page():
    if request.method == "GET":
        return render_template("index.html")

    file = request.files.get("logFile")
    if file and '.' in file.filename and file.filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS:
        file_path = os.path.join(Config.UPLOAD_FOLDER, file.filename)
        file.save(file_path)

        if file.filename.rsplit('.', 1)[1].lower() == 'json':
            with open(file_path, "r") as f:
                data = json.load(f)
                error_logs = data if isinstance(data, list) else data.get("logs", []) if isinstance(data, dict) else []
        else:
            with open(file_path, "r") as f:
                error_logs = f.readlines()

        os.remove(file_path)
        analysis_results = analyzer.analyze_error_logs(error_logs)
        return jsonify(analysis_results)

    return render_template("index.html", error="Please upload a valid log file (.txt or .json).")

if __name__ == "__main__":
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = Config.GOOGLE_APPLICATION_CREDENTIALS
    app.run(debug=True)
