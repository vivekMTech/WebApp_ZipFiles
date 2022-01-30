from flask import Flask, render_template, flash, send_from_directory
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileRequired
from wtforms import FileField
from zipfile import ZipFile
import shutil
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ec9439cfc6c796ae2029594d'


class upload_zip(FlaskForm):
    file = FileField(label="Select file : ",
                     validators=[FileAllowed(['zip']), FileRequired()])


def extract_zip(file_name, dir_name):
    shutil.rmtree('extracted_files')
    with ZipFile(file_name, "r") as zip_ref:
        zip_ref.extractall(dir_name)


@app.route("/", methods=['GET', 'POST'])
@app.route('/upload', methods=['GET', 'POST'])
def uploadRoute():
    lst = []
    form = upload_zip()
    if form.validate_on_submit():
        zip_file = form.file.data
        extract_zip(zip_file, 'extracted_files')
        for files in os.listdir("extracted_files"):
            lst.append(files)
        return render_template("shownZipFiles.html", files=lst)
    else:
        flash("Please, Select only zip file.", category='danger')
    return render_template("uploadZip.html", form=form)


@app.route("/shown")
def showRoute():
    return render_template("shownZipFiles.html")


@app.route('/<path:filename>', methods=['GET', 'POST'])
def download_file(filename):
    return send_from_directory('extracted_files', filename)


if __name__ == '__main__':
    app.run(debug=True)
