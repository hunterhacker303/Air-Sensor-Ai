from flask import Flask, render_template,jsonify

app = Flask(__name__)

Job = [
    {
        'id': 1,
        'title': 'Data Analyst',
        'location': 'Bengaluru, India',
        'salary': 'Rs 10,00,000'
    },
    {
        'id': 2,
        'title': 'Data Scientist',
        'location': 'Delhi, India',
        'salary': 'Rs 10,00,000'
    },
    {
        'id': 3,
        'title': 'Machine Learning Engineer',
        'location': 'Mumbai, India',
        'salary': 'Rs 10,00,000'
    },
    {
        'id': 4,
        'title': 'Backend Developer',
        'location': 'Indore, India',
        'salary': 'Rs 10,00,000'
    }
]

@app.route("/")
def home():
    return render_template("ai.html", jobs=Job,project_name="Air Sensor Ai")
@app.route("/api/jobs")
def jobs():
    return jsonify(Job)
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)