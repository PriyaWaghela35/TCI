from flask import Flask, jsonify, request # type: ignore
import mysql.connector # type: ignore
from mysql.connector import errorcode # type: ignore

app = Flask(__name__)

# Establish connection without specifying the database to create it if it doesn't exist
con = mysql.connector.connect(
    host='127.0.0.1',
    user='root',
    password='Apjb@1389'
)

# Create the database if it doesn't exist
def create_database_if_not_exists():
    cursor = con.cursor()
    try:
        cursor.execute("CREATE DATABASE IF NOT EXISTS TestDB;")
        con.commit()
        print("Database created or already exists.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()

# Call the function to ensure the database exists
create_database_if_not_exists()

# Now connect to the specific database
con = mysql.connector.connect(
    host='127.0.0.1',
    user='root',
    password='Apjb@1389',
    database='TestDB'
)

@app.route('/getTable', methods=['GET'])
def get_Table():
    cur = con.cursor()
    cur.execute("SHOW TABLES;")
    tables = cur.fetchall()
    cur.close()
    table_names = [table[0] for table in tables]
    return jsonify({"Table": table_names})

@app.route("/create", methods=["POST"])
def create_tables():
    query = """CREATE table IF NOT EXISTS employee (
                empid INT primary key,
                name varchar(100) not null,
                email_id varchar(100),
                job_role varchar(100)
                );"""
    cur = con.cursor()
    cur.execute(query)
    con.commit()
    cur.close()
    return jsonify({"Message": "Table created successfully"})

@app.route("/update", methods=["POST"])
def update_tables():
    empid = request.form.get("empid")  # Employee ID
    column = request.form.get("column")  # Column to update
    value = request.form.get("value")  # New value for the column
    
    if not (empid and column and value):
        return jsonify({"Error": "Please provide 'empid', 'column', and 'value'"}), 400

    try:
        query = f"UPDATE employee SET {column} = %s WHERE empid = %s;"
        cur = con.cursor()
        cur.execute(query, (value, empid))
        con.commit()
        cur.close()
        return jsonify({"Message": "Table updated successfully"})
    except Exception as e:
        return jsonify({"Error": str(e)}), 500

@app.route("/delete", methods=["POST"])
def delete_tables():
    empid = request.form.get("empid")  # Employee ID
    if not empid:
        return jsonify({"Error": "Please provide 'empid'"}), 400
    
    query = f"DELETE FROM employee WHERE empid = %s;"
    cur = con.cursor()
    cur.execute(query, (empid,))
    con.commit()
    cur.close()
    return jsonify({"Message": "Value is deleted successfully"})

@app.route("/read", methods=['POST'])
def read_table():
    table_name = request.form.get("table")  # Get the table name from query parameters
    
    if not table_name:
        return jsonify({"Error": "Please provide a table name in the query parameter 'table'"}), 400
    
    try:
        cur = con.cursor()
        query = f"SELECT * FROM {table_name};"
        cur.execute(query)
        result = cur.fetchall()
        cur.close()
        
        # Optional: Dynamically fetch column names
        column_names = [desc[0] for desc in cur.description]
        result_with_columns = [dict(zip(column_names, row)) for row in result]
        
        return jsonify(result_with_columns)
    except Exception as e:
        return jsonify({"Error": str(e)}), 500

@app.route("/alter", methods=["GET"])
def alter_tables():
    query = "ALTER TABLE employee ADD COLUMN contact BIGINT;"
    cur = con.cursor()
    cur.execute(query)
    con.commit()
    cur.close()
    return jsonify({"Message": "Table altered successfully"})

@app.route("/insert", methods=["GET"])
def insert_tables():
    query = """
    INSERT INTO employee (empid, name, email_id, job_role)
    VALUES
    (2001, 'Priya Wagehla', 'priyawaghela35@gmail.com', 'Engineer'),
    (2002, 'Priya Sharma', 'priyasharma@gmail.com', 'HR'),
    (2003, 'Tiya Wagehla', 'tiyawaghela35@gmail.com', 'CA');
    """
    cur = con.cursor()
    cur.execute(query)
    con.commit()
    cur.close()
    return jsonify({"Message": "Values inserted in table successfully"})

@app.route("/drop", methods=["GET"])
def drop_tables():
    query1 = """DROP TABLE IF EXISTS employee"""
    cur = con.cursor()
    cur.execute(query1)
    con.commit()
    cur.close()
    return jsonify({"Message": "Table is deleted successfully"})

@app.route('/')
def home():
    return "Welcome to my Database!!!!"

if __name__ == "__main__":
    app.run(debug=True, port=2000)
