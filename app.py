import os
from flask import Flask, render_template, request, redirect, url_for, flash
from utils.keyword_matching import rank_resumes

app = Flask(__name__)
app.secret_key = "your_secret_key"  # For flash messages

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# Check if the uploaded file is a valid PDF
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        job_description = request.form["job_description"].strip()
        resume_files = request.files.getlist("resume_folder")  # Get list of files uploaded

        if not job_description or not resume_files:
            flash("Please provide both job description and resume files.", "error")
            return redirect(url_for("home"))

        # Create a temporary folder to store uploaded files
        resume_folder = os.path.join(app.config['UPLOAD_FOLDER'], "resumes")
        os.makedirs(resume_folder, exist_ok=True)

        # Save only PDF files from the folder upload
        for resume_file in resume_files:
            if resume_file and allowed_file(resume_file.filename):
                filename = os.path.join(resume_folder, resume_file.filename)
                resume_file.save(filename)

        try:
            ranked_resumes = rank_resumes(resume_folder, job_description)
            return render_template("index.html", ranked_resumes=ranked_resumes)
        except Exception as e:
            flash(f"An error occurred: {str(e)}", "error")
            return redirect(url_for("home"))

    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
