from app import create_app
from flask import render_template
import os

app = create_app()

print("Current Directory:", os.getcwd())
print("Template Folder:", app.template_folder)

@app.route("/")
def home():
    return "<h1>CVPilot Working</h1>"

if __name__ == "__main__":
    app.run(debug=True)