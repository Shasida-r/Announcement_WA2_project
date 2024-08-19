import datetime
import json
import os
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)

# Set the base directory to the location of this script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

@app.route('/')
def index():
    # Get homework details
    hw_file_path = os.path.join(BASE_DIR, 'hw.txt')
    ls = []
    with open(hw_file_path, "rt") as f:
        for x in f:
            ls.append(list(x.rstrip('\n').split("||")))
    ls.reverse()

    # Get general announcement details
    ga_file_path = os.path.join(BASE_DIR, 'ga.txt')
    ls_ga = []
    with open(ga_file_path, "rt") as f:
        for x in f:
            ls_ga.append(list(x.rstrip('\n').split("||")))
    ls_ga.reverse()

    return render_template('index.html', result=ls, result_ga=ls_ga)

@app.route('/login_button')
def login_button():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    name = None
    password = None
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']
        data_file_path = os.path.join(BASE_DIR, 'data.txt')
        with open(data_file_path, "r") as file:
            data_list = json.load(file)
        for item in data_list:
            if item["name"] == name and item["password"] == password:
                return render_template('post.html', name=name)
        return render_template('login.html', name=name, password=password)
    else:
        return render_template('login.html', name=name, password=password)

@app.route('/result', methods=['POST'])
def result():
    if request.method == 'POST':
        result = request.form
        x = datetime.datetime.now()
        if result["type"] == "HW":
            hw_file_path = os.path.join(BASE_DIR, 'hw.txt')
            with open(hw_file_path, "at") as f:
                f.write(
                    x.strftime("%d %b %y %I:%M %p") + "||" + result["subject"] + "||" +
                    result["date"] + "||" + result["desc"] + "||" + result["name"] + "\n")
            return render_template("post.html", result=result)
        else:
            ga_file_path = os.path.join(BASE_DIR, 'ga.txt')
            with open(ga_file_path, "at") as f:
                f.write(
                    x.strftime("%d %b %y %I:%M %p") + "||" + result["title"] + "||" +
                    result["desc"] + "||" + result["name"] + "\n")
            return render_template("post.html", name=result["name"])

@app.route('/back')
def back():
    return redirect(url_for('index'))

@app.route('/create_account', methods=['GET', 'POST'])
def create_account():
    name = None
    email = None
    dropdown = None
    password = None
    c_password = None
    admin_code = None
    data_list = []
    data = {}
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        dropdown = request.form['dropdown']
        password = request.form['password']
        c_password = request.form['c_password']
        admin_code = request.form['admin_code']
        if password == c_password and admin_code == "ASRJC":
            data = {
                "name": name,
                "email": email,
                "class": dropdown,
                "password": password
            }
            data_file_path = os.path.join(BASE_DIR, 'data.txt')
            with open(data_file_path, "r") as file:
                data_list = json.load(file)
            data_list.append(data)
            json_string = json.dumps(data_list)
            with open(data_file_path, "w") as file:
                file.write(json_string)
            return redirect(url_for('index'))
        else:
            return render_template('create_account.html',
                                   name=name,
                                   email=email,
                                   dropdown=dropdown,
                                   password=password,
                                   c_password=c_password,
                                   admin_code=admin_code)
    else:
        return render_template('create_account.html',
                               name=name,
                               email=email,
                               dropdown=dropdown,
                               password=password,
                               c_password=c_password,
                               admin_code=admin_code)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
