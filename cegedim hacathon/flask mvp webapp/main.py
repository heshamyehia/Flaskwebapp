import codecs
import csv
import pandas as pd
from flask import Flask, jsonify, request, render_template

app = Flask(__name__)

# Paths for CSV files
VOLUNTEER_CSV_PATH = "D:\cegedim hacathon\Voulonteer basic .csv"
HOSPITAL_CSV_PATH = "D:\cegedim hacathon\hospital basic.csv"

# Read initial data from CSV files
def read_csv_data(csv_path):
    data = []
    try:
        with open(csv_path, mode="r", newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                data.append(row)
    except FileNotFoundError:
        # If the CSV file doesn't exist yet, create an empty file
        with open(csv_path, mode="w", newline='') as file:
            pass
    return data

volunteers = read_csv_data(VOLUNTEER_CSV_PATH)
hospitals = read_csv_data(HOSPITAL_CSV_PATH)

#@app.route('/')
#def index():
#    return render_template('index.html',content="Testing")

@app.route('/api/register/volunteer', methods=['POST','GET'])
def register_volunteer():
    data = request.json   # Assuming data is sent as JSON in the request body
    name = data.get('name')
    email = data.get('email')
    age = data.get('age')
    password = data.get('password')
    bloodtype = data.get('bloodtype')
    # You can add more fields as needed

    if not name or not email:
        return jsonify({"error": "Name and email are required fields"}), 400

    # Save the volunteer data to the CSV file
    with open(VOLUNTEER_CSV_PATH, mode="a", newline='') as file:
        writer = csv.DictWriter(file, fieldnames=["name", "email","age","password","bloodtype"])
        writer.writerow({"name": name, "email": email,"age": age, "password": password,"bloodtype": bloodtype})

    return jsonify({"message": "Volunteer registration successful!"}), 201

@app.route('/api/register/hospital', methods=['POST'])
def register_hospital():
    data = request.json  # Assuming data is sent as JSON in the request body
    name = data.get('name')
    location = data.get('location')
    # You can add more fields as needed

    if not name or not location:
        return jsonify({"error": "Name and location are required fields"}), 400

    # Save the hospital data to the CSV file
    with open(HOSPITAL_CSV_PATH, mode="a", newline='') as file:
        writer = csv.DictWriter(file, fieldnames=["name", "location"])
        writer.writerow({"name": name, "location": location})

    return jsonify({"message": "Hospital registration successful!"}), 201


@app.route("/api/hospitals", methods=["GET"])
def get_hospitals():
    # Read hospital data from the CSV file
    hospitals = pd.read_csv(HOSPITAL_CSV_PATH)
    return jsonify(hospitals.to_dict('record'))


if __name__ == '__main__':
    app.run(debug=True)

