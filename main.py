import datetime
import json

from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5001)


@app.route('/')
def index():
  #Get homework details
  ls = []
  with open("hw.txt", "rt") as f:
    for x in f:
      ls.append(list(x.rstrip('\n').split("||")))

  f.close()
  ls.reverse()

  #Get general announcement details
  ls_ga = []
  with open("ga.txt", "rt") as f:
    for x in f:
      ls_ga.append(list(x.rstrip('\n').split("||")))
  f.close()
  ls_ga.reverse()

  #print(ls)
  return render_template('index.html', result=ls, result_ga=ls_ga)
  #return render_template('index.html')


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
    with open("data.txt", "r") as file:
      data_list = json.load(file)
    for item in data_list:
      if item["name"] == name and item["password"] == password:
        #return redirect(url_for('post'))
        return render_template('post.html', name=name)
    return render_template('login.html', name=name, password=password)
  else:
    return render_template('login.html', name=name, password=password)


@app.route('/result', methods=['POST'])
def result():
  if request.method == 'POST':
    result = request.form
    #print(result)
    x = datetime.datetime.now()
    if result["type"] == "HW":
      with open("hw.txt", "at") as f:
        f.write(
            x.strftime("%d %b %y %I:%M %p") + "||" + result["subject"] + "||" +
            result["date"] + "||" + result["desc"] + "||" + result["name"] +
            "\n")
      f.close()
      return render_template("post.html", result=result)
    else:
      with open("ga.txt", "at") as f:
        f.write(
            x.strftime("%d %b %y %I:%M %p") + "||" + result["title"] + "||" +
            result["desc"] + "||" + result["name"] + "\n")
      f.close()
      return render_template("post.html", name=result["name"])


@app.route('/back')
def back():
  return redirect(url_for('index'))

'''
@app.route('/post', methods=['GET'])
def post():
  return render_template("post.html")
'''


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
      with open("data.txt", "r") as file:
        data_list = json.load(file)
      data_list.append(data)
      json_string = json.dumps(data_list)
      with open("data.txt", "w") as file:
        file.truncate(0)
      with open("data.txt", "a") as file:
        file.write(json_string + "\n")
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
