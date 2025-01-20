import hashlib
from flask import Flask, request,jsonify
import jwt
token_id = {}    
# existing_user = next((user for user in token_id.values() if user['email'] == email), None)

app = Flask(__name__)

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



@app.route('/login', methods=['POST'])
def log_in():
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
            existing_user['set_flag'] = True
            return jsonify({"Accepted": "Welcome user"}), 200
        else:
            return jsonify({"Fail": "Invalid User"}), 401
    else:
        return jsonify({"Error": "Email not registered."}), 404


@app.route('/message', methods=['GET'])
def response():
    flagged_user = next((user for user in token_id.values() if user['set_flag']), None)
    
    if flagged_user:
        return jsonify({"response": "xyz"}), 200
    else:
        return jsonify({"message": "No flagged user found."}), 404
    
@app.route('/logout', methods=['GET'])
def log_out():
    flagged_user = next((user for user in token_id.values() if user['set_flag']), None)
    
    if flagged_user:
        flagged_user['set_flag'] = False
        return jsonify({"response": "Log-out succesful"}), 200
    else:
        return jsonify({"message": "No flagged user found."}), 404
    
@app.route('/')
def home():
    return jsonify({"Welcome":"Login/Signup"})
    
if __name__ == '__main__':
    app.run(debug=True)
    