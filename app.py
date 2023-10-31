from flask import Flask, request, render_template
import os
import vertexai
from vertexai import language_models

app = Flask(__name__)

# Define the upload folder and allowed extensions
app.config['UPLOAD_FOLDER'] = 'C:/Users/neosu/webapp1/temp'

# Update the allowed extensions
ALLOWED_EXTENSIONS = {'sql'}

# Set the GOOGLE_APPLICATION_CREDENTIALS environment variable.
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'C:/Users/neosu/webapp1/mlproj1-403203-c24f2a45ebd5.json'

# Initialize Vertex AI.
vertexai.init(project="mlproj1-403203", location="us-central1")

# Load the CodeChatModel model from Vertex AI.
chat_model = language_models.CodeChatModel.from_pretrained("codechat-bison")

# Function to correct SQL queries
def correct_sql_query(sql_query):
    chat = chat_model.start_chat()
    response = chat.send_message(sql_query)
    corrected_sql_query = response.text
    return corrected_sql_query

# Function to check allowed file extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Route to display the main page with both options
@app.route("/", methods=["GET", "POST"])
def handle_main_page():
    if request.method == "POST":
        # Check if SQL syntax was entered
        sql_syntax = request.form.get("sql_syntax")
        if sql_syntax:
            # Process SQL syntax if provided
            corrected_sql_query = correct_sql_query(sql_syntax)
            return corrected_sql_query

        # Check if an SQL file was uploaded
        if 'sql_file' in request.files:
            file = request.files["sql_file"]
            if file and allowed_file(file.filename):
                # Save the uploaded file to the UPLOAD_FOLDER
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
                file.save(file_path)
                # Read the SQL query from the uploaded file
                with open(file_path, "r") as f:
                    sql_query = f.read()
                # Correct the SQL query
                corrected_sql_query = correct_sql_query(sql_query)
                # Delete the temporary file
                os.remove(file_path)
                # Return the corrected SQL query as plain text
                return corrected_sql_query

    # Render the main page with the form for both options
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
