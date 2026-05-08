from flask import Flask
from flask_cors import CORS

from routes.students import students_bp
from routes.courses import courses_bp
from routes.grades import grades_bp
from routes.auth import auth_bp

app = Flask(__name__)

CORS(app)

app.register_blueprint(students_bp)
app.register_blueprint(courses_bp)
app.register_blueprint(grades_bp)
app.register_blueprint(auth_bp)

@app.route("/")
def home():
    return {"message": "Backend funcionando"}

if __name__ == "__main__":
    app.run(debug=True)