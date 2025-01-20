import hashlib
from flask import Flask, request,jsonify,session,redirect,url_for
import jwt
import os
token_id = {}    

app = Flask(__name__)
app.secret_key = os.urandom(42)
def generate_secret_key(*inputs):
    combined_input = ''.join(map(str, inputs))
    hashed_key = hashlib.sha256(combined_input.encode()).hexdigest()
    return hashed_key

@app.route('/Signup',methods = ['POST'])
def sign_up():
    user_key = f"USER{len(token_id)+1}"
    name = request.form.get("name")
    email = request.form.get("email")
    role = request.form.get("role")
    Password = request.form.get("Password") # if sab hona chahiye 
    SECRET_KEY = generate_secret_key(email, Password)
    payload = {
        "user_id": name,
        "email": email,
        "role": role,
    }
    if any(user['email'] == email for user in token_id.values()):
        return jsonify({"Message":"User Already registered"})
    token = jwt.encode(payload,SECRET_KEY,algorithm='HS256')
    token_id[user_key] = {
            "email": email,
            "token": token,
            "set_flag": False
        }
    return jsonify({"Message": f"Successfull Sign IN{token_id}"})



@app.route('/login', methods=['POST', 'GET'])
def log_in():
    if request.method == 'POST':
        email = request.form.get("email")
        Password = request.form.get("Password")
        SECRET_KEY = generate_secret_key(email, Password)

        if not email or not Password:
            return jsonify({"Error": "Please enter your login credentials."}), 400

        existing_user = next((user for user in token_id.values() if user['email'] == email), None)

        if existing_user:
            token = existing_user['token']
            decoded_token = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])

            if decoded_token.get("email") == email:
                session['email'] = email
                return redirect(url_for('response')), 200
            else:
                return jsonify({"Fail": "Invalid User"}), 401
        else:
            return jsonify({"Error": "Email not registered."}), 404

@app.route('/message', methods=['GET'])
def response():
    if 'email' in session:  # Check if user is logged in
        return f'Hello, {session["email"]}! You are logged in.'
    return 'You are not logged in!'
    
@app.route('/')
def home():
    return jsonify({"Welcome":"Login/Signup"})
    
if __name__ == '__main__':
    app.run(debug=True)
    


'''if 'username' in session:  # Check if user is logged in
        return f'Hello, {session["username"]}! You are logged in.'
    return 'You are not logged in!'''