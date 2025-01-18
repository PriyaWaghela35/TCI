from functools import wraps
from flask import Flask, render_template,request,jsonify 
import requests
import threading
import time

app = Flask(__name__)


initial_route = " https://beta.tradefinder.in/api/servertime"
initial_response = {"message":"Route is working!"}
# try:
#     response= requests.get(initial_route)
#     if response.status_code == 200:
#         initial_response = response.json()
#     else:
#         initial_response = {"error":"failed to fetch data"}

# except Exception as e:
#     initial_response = {"error": str(e)}
# # 1 task
# @app.route('/dyn1',methods=['GET'])
# def get_dynamic_data():
#     return jsonify(initial_response)

# 2 task

def fetch_data_periodically(interval=5):
    global initial_response
    while True:
        try:
            response = requests.get(initial_route)
            if response.status_code == 200:
                initial_response = response.json()
            else:
                initial_response = {"error": "Failed to fetch data"}
        except Exception as e:
            initial_response = {"error":str(e)}
        time.sleep(interval)
threading.Thread(target=fetch_data_periodically,args=(3,),daemon=True).start()
@app.route('/dyn_new')
def get_dynamic_data():
    return jsonify(initial_response)
    

# 3 task
def log_request_type(func):
    def wrapper(*args,**kwargs):
        print(f"Request Type:{request.method}")
        return func(*args,**kwargs)
    return wrapper

@app.route("/example", methods=["GET","POST"])
@log_request_type
def example():
    if request.method == "GET":
        return "This is GET request"
    elif request.method == "POST":
        return "This is POST request"
    

@app.route('/')
def home():
    return "Welcome to TCI Backend"


if __name__ == '__main__':
    app.run(debug=True)