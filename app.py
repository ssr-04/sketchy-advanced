from crypt import methods
from tabnanny import check
from time import sleep
from unittest import result
from flask import Flask, render_template, request, redirect,jsonify,session
from werkzeug.utils import secure_filename
from helper import apology, file_check, popup, qr_code
from controlnet import render,set_key
import os
import random
from firebase_helper import create_user,upload_sketch,get_active_users,upload_result,get_urls,check_login
from session_helper import login_required

app = Flask(__name__)
app.secret_key = 'I_am_unpredictable_lv_3000'

app.config["SESSION_TYPE"] = "filesystem"
app.config['SESSION_PARMANENT'] = False

@app.after_request
def after_request(response):
  """Ensure responses aren't cached"""
  response.headers["Cache-Control"] = "no-cache,no-store,must-revalidate"
  response.headers["Expires"] = 0
  response.headers["Pragma"] = "no-cache"
  return response

@app.route("/login", methods=["POST","GET"])
def login():
    if request.method == "POST":
        user = request.form.get("username")
        password = request.form.get("password")

        if not check_login(user,password):
            return apology("Invalid username and password")
        else:
            session['admin'] = "ssr_labs_admin"

            return redirect("/generate")
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.route("/")
@login_required
def index():
    return render_template("home.html")


@app.route("/set_api",methods=["POST","GET"])
@login_required
def api_key():
    if request.method == "POST":
        key = request.form.get("key")
        c_key = set_key(key)
        return render_template("api_key.html",check=1,key=c_key)
    else:
        return render_template("api_key.html",check=0)


@app.route("/generate",methods=["POST","GET"])
@login_required
def generate():
    if request.method == "POST":
        name = request.form.get("name")
        department = request.form.get("department")
        uni_num = str(random.randint(100,1000))
        
        uni_id = name + "-" + department + "-" +uni_num
        c_host = str(request.host)
        uni_url = c_host+ "/input/" + uni_id
        create_user(uni_id)
        session['temp_user'] = uni_id
        
        qr_code(uni_url)
        return render_template("qr_input.html",url=uni_url,user=uni_id)

    return render_template("generate.html")


@app.route("/input/<unique_id>")
def input(unique_id):
    s = unique_id
    db = get_active_users()
    if s in db:
        session['temp_user'] = s
        if db[s]['status']==0:
            return render_template("input.html",check=0)
        elif db[s]['status']==1:
            return apology("Sketch uploaded..(might be processing)")
        else:
            return redirect('/result')
    else:
        return apology("Generation request not created")


@app.route("/magic",methods=["POST"])
def upload():
    if request.method == "POST":
        if 'file' not in request.files:
            return apology(msg="Illegal Post detected 🤨",code=420)
        file = request.files['file']

        if file.filename == '':
            return popup("Invalid","Choose file before submitting")

        if file and file_check(file.filename):
            filename = secure_filename(file.filename)
            filename = "sketch" + '.' + filename.split('.')[-1]
            session['sketch_name'] = filename
            prompt = request.form.get("prompt")
            model = int(request.form.get("modelSelect"))
            path = "./"+filename
            file.save(path)
            upload_sketch(session['temp_user'],path,filename)

            print("started")
            url = render(path,model,prompt=prompt)
            print("done")
            upload_result(url,session['temp_user'])
            return redirect("result")
        return apology("Something went wrong")


@app.route("/result")
def result():
    user = session['temp_user'].split('-')
    user = user[0] + " " + user[1]
    r_urls = get_urls()
    if (r_urls['result'] and r_urls['sketch']):
        sketch_url = r_urls['sketch_url']
        result_url = r_urls['result_url']
        return render_template("result.html",check=1, result = result_url, sketch = sketch_url ,user=user)
    else:
        return apology("Something went wrong")

"""@app.route("/loading")
def test():
    return render_template("result.html")

@app.route("/test")
def test1():
    return render_template("qr_input.html",user="Sachin-it-990")"""


if (__name__ == "__main__"):
    print("started")
    app.run(host="0.0.0.0", port = 9090, debug= True)