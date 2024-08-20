from flask import Flask, redirect, render_template, url_for, request, jsonify
import json
import os

app = Flask(__name__)

@app.route("/", methods=['GET'])
def Home():
    return render_template("Home.html")

@app.route("/", methods=['POST'])
def HomeFormu():
    action = request.form.get("action")
    if action == "Login":
        return redirect(url_for("Login"))
    elif action == "Create New User":
        return redirect(url_for("New"))
    return redirect(url_for("Home"))

@app.route("/Login", methods=['GET'])
def Login():
    return render_template("Login.html")

@app.route("/Login", methods=['POST'])
def LoginFormAndData():
    json_path = os.path.join(app.static_folder, 'Data.json')
    
    try:
        with open(json_path, "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        return "Json yoxdu", 500
    except json.JSONDecodeError:
        return "JSON load edile bilmir", 500

    name = request.form.get("Name", "").strip()
    surname = request.form.get("Surname", "").strip()
    
    found = False
    for student in data.get("students", []):
        if name == student.get("Name") and surname == student.get("Surname"):
            found = True    
            break
    
    if found:
        return redirect(url_for("HelloUser", name = name))
    else:
        return redirect(url_for("Login"))


@app.route("/New")
def New():
    return render_template("New.html")

@app.route("/New", methods = ["POST", "GET"])
def NewFormAndSaveData():
    json_path = os.path.join(app.static_folder, 'Data.json')
    with open(json_path, "r") as f:
        loaded_data = json.load(f)
    name = request.form.get("Name", "").strip()
    surname = request.form.get("Surname", "").strip()
    new_user={
        "Name": name,
        "Surname": surname
    }
    loaded_data["students"].append(new_user)
    with open(json_path,"w") as f:
       json.dump(loaded_data, f, indent=4) 
    return redirect(url_for("Successfully"))
        



@app.route("/Successfully")
def Successfully():
    return render_template("scfly.html")


@app.route("/hello-user/<name>")
def HelloUser(name):
    return render_template("hello-user.html" , username = name)



if __name__ == "__main__":
    app.run(debug=True)
