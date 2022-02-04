from flask import Flask, render_template, flash, send_file  # import flask and their classes
from flask_wtf import FlaskForm  # flask form for uploading zip files
from flask_wtf.file import FileAllowed, FileRequired  # allowed files
from wtforms import FileField  # file field for uploading files
import zipfile  # extract zip files
import shutil  # removing files from pwd
from werkzeug.utils import secure_filename  # get file name
import os

app = Flask(__name__)  # initialize flask app
app.config['SECRET_KEY'] = 'ec9439cfc6c796ae2029594d'  # secret key for authentication
global extracted_path, dir_count  # extracted files path & current dir count
dir_count = 0  # init directory count=0


class upload_zip(FlaskForm):  # class for fileField form
    file = FileField(label="Select file : ",
                     validators=[FileAllowed(['zip', 'rar']), FileRequired()])  # validators only allow zip files


def extract_zip(zip_file, filename):  # extract zip method
    global dir_count
    dir_count += 1  # increment directory cont
    child_dir_path = os.path.join("extracted_files", filename + str(dir_count))  # prepare path for sub folder
    try:
        shutil.rmtree(child_dir_path)  # removing files from sub-folder
    except OSError as error:
        os.makedirs(child_dir_path)  # If folder was not their then it created.

        try:
            with zipfile.ZipFile(zip_file, "r") as zip_ref:  # process of extract files:
                zip_ref.extractall(child_dir_path)  # extractall() method for extracting files
        except zipfile.BadZipfile:
            flash("Please, Your ZIP or RAR files is Corrupted.", category='danger')
        except zipfile.LargeZipFile:
            flash("Please, Your ZIP or RAR files is Large.", category='danger')

    return child_dir_path


@app.route("/", methods=['GET', 'POST'])  # index route
@app.route('/upload', methods=['GET', 'POST'])  # upload route
def upload_route():  # method for uploading zip file
    global extracted_path
    form = upload_zip()  # initialize form object
    if form.validate_on_submit():  # if data is valid then process further
        zip_file = form.file.data  # get file in zip_file var
        filename = secure_filename(form.file.data.filename)  # get filename
        extracted_path = extract_zip(zip_file, filename)  # extract zip file
        return render_template("shownZipFiles.html", files=os.listdir(extracted_path))
    else:
        # if file are not validate then print flash message
        flash("Please, Select only ZIP or RAR files.", category='danger')
    return render_template("uploadZip.html", form=form)  # call "uploadZip.html" with form


@app.route("/<filename>", methods=['GET', 'POST'])  # route for downloading file
def download_file(filename):  # method for download file
    global extracted_path
    file_path = extracted_path + "/" + filename  # file path, where file is located
    return send_file(file_path, as_attachment=True)  # send_file() send content to client pc.


if __name__ == '__main__':  # init main
    app.run(debug=True)  # run app in debug mode
