import hashlib
from flask import Flask, request,jsonify
import jwt
token_id = {}
email_id = token_id.keys()
app = Flask(__name__)

def generate_secret_key(*inputs):
    combined_input = ''.join(map(str, inputs))
    hashed_key = hashlib.sha256(combined_input.encode()).hexdigest()
    return hashed_key

@app.route('/Signup',methods = ['POST'])
def sign_up():
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
    token = jwt.encode(payload,SECRET_KEY,algorithm='HS256')
    token_id[email] = token
    return jsonify({"Message": "Successfull Sign IN"})



@app.route('/login', methods=['POST'])
def log_in():
    email = request.form.get("email")
    Password = request.form.get("Password")
    SECRET_KEY = generate_secret_key(email, Password)

    # Ensure both email and password are provided
    if not email or not Password:
        return jsonify({"Error": "Please enter your login credentials."})

    # Check if the email is valid
    if email in token_id:
        token = token_id[email]
        token_1 = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])

        # Check if the decoded token matches the email
        if email == token_1.get("email"):
            return jsonify({"Accepted": "Welcome user"})
        else:
            return jsonify({"Fail": "Invalid User"})
    
    # If email is not found
    return jsonify({"Fail": "Invalid User"})
    
if __name__ == '__main__':
    app.run(debug=True,ssl_context='adhoc',port=5001)
    