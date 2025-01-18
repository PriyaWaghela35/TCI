from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)
MONGO_URI = "mongodb://localhost:27017"  # Replace with your MongoDB URI
DATABASE_NAME = "test_db"                # Replace with your database name
COLLECTION_NAME = "test_collection"

@app.route("/")
def home():
    # mongo.db.inventory.insert_one({"name":"Priya","email":"priyawagehal35@gmail.com","contact":987654321})
    return " HELLO WORLD!!"

@app.route("/create", methods=["POST"])
def create_document():
    name = request.form.get("name")
    email = request.form.get("email")
    contact = request.form.get("contact")
    if not name or not email or not contact:
        return jsonify({"Error": "All fields (name, email, contact) are required"}), 400
    try:
        contact = int(contact)
    except ValueError:
        return jsonify({"Error": "Invalid 'contact' value. Must be an integer"}), 400
    new_document = {
        "name": name,
        "email": email,
        "contact": contact
    }
    try:
        result = mongo.db.inventory.insert_one(new_document)
        return jsonify({"message": "Document created", "_id": str(result.inserted_id)}), 201
    except Exception as e:
        return jsonify({"Error": f"An error occurred: {str(e)}"}), 500

@app.route("/read", methods=["GET"])
def read_documents():
    documents = mongo.db.inventory.find()
    output = []
    for doc in documents:
        doc["_id"] = str(doc["_id"])  
        output.append(doc)
    return jsonify(output)

@app.route('/delete',methods=['POST'])
def delete_document():
    doc_id = request.form.get("id")
    if not doc_id:
        return jsonify ({"message":"ID is required"}),400
    try:
        delete_result=mongo.db.inventory.delete_one({'_id': ObjectId(doc_id)})
        if delete_result.deleted_count>0:
            return jsonify({"Message":"Document deleted"})
        else:
            return jsonify({"Message":"Document not found"}),404
    except Exception as e:
        return jsonify({"error":str(e)}),500


@app.route("/update", methods=["POST"])
def update_document():
    _id = request.form.get("id")
    if not _id:
        return jsonify({"Error": "'id' is required"}), 404

    if not ObjectId.is_valid(_id):
        return jsonify({"Error": "Invalid ObjectId"}), 400

    object_id = ObjectId(_id)

    name = request.form.get("name")
    email = request.form.get("email")
    contact = request.form.get("contact")

    update_data = {}
    if name:
        update_data["name"] = name
    if email:
        update_data["email"] = email
    if contact:
        try:
            contact = int(contact)  
            update_data["contact"] = contact
        except ValueError:
            return jsonify({"Error": "Invalid 'contact' value. Must be an integer."}), 400

    if not update_data:
        return jsonify({"Error": "No fields provided to update"}), 400

    try:
        update_result = mongo.db.inventory.update_one(
            {'_id': object_id},
            {'$set': update_data}
        )
        if update_result.matched_count > 0:
            return jsonify({"message": "Document updated successfully"})
        else:
            return jsonify({"message": "Document not found"}), 404
    except Exception as e:
        return jsonify({"Error": str(e)}), 500
if __name__ == '__main__':
    app.run(debug=True)