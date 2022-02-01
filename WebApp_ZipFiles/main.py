from flask import Flask, render_template, flash, send_file  # import flask and their classes
from flask_wtf import FlaskForm  # flask form for uploading zip files
from flask_wtf.file import FileAllowed, FileRequired  # allowed files
from wtforms import FileField  # file field for uploading files
from zipfile import ZipFile  # extract zip files
import shutil  # removing files from pwd
import os

app = Flask(__name__)  # initialize flask app
app.config['SECRET_KEY'] = 'ec9439cfc6c796ae2029594d'  # secret key for authentication


class upload_zip(FlaskForm):  # class for fileField form
    file = FileField(label="Select file : ",
                     validators=[FileAllowed(['zip']), FileRequired()])  # validators only allow zip files


def extract_zip(file_name, dir_name):  # extract zip method
    shutil.rmtree('extracted_files')  # removing files from folder
    with ZipFile(file_name, "r") as zip_ref:  # process of extract files
        zip_ref.extractall(dir_name)  # extractall() method for extracting files


@app.route("/", methods=['GET', 'POST'])  # index route
@app.route('/upload', methods=['GET', 'POST'])  # upload route
def uploadRoute():  # method for uploading zip file
    form = upload_zip()  # initialize form object
    if form.validate_on_submit():  # if data is valid then process further
        zip_file = form.file.data  # get file in zip_file var
        extract_zip(zip_file, 'extracted_files')  # extract zip file
        return render_template("shownZipFiles.html", files=os.listdir("extracted_files"))  # call "shownZipFiles.html" and send file lst
    else:
        flash("Please, Select only zip file.", category='danger')  # if file are not validate then print flash message
    return render_template("uploadZip.html", form=form)  # call "uploadZip.html" with form


@app.route("/<filename>", methods=['GET', 'POST'])  # route for downloading file
def download_file(filename):  # method for download file
    file_path = "extracted_files/" + filename  # file path, where file is located
    return send_file(file_path, as_attachment=True)  # send_file() send content to client pc.


if __name__ == '__main__':  # init main
    app.run(debug=True)  # run app in debug mode
