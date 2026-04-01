from flask import Flask, request, jsonify, render_template
from models import GradeManager

app = Flask(__name__)
manager = GradeManager()

# demo data
manager.add_student("عبدالله ليث")
manager.add_grade("عبدالله ليث", "رياضيات", 92)
manager.add_grade("عبدالله ليث", "علوم", 87)
manager.add_grade("عبدالله ليث", "لغة عربية", 78)



@app.route("/")
def index():
    return render_template("index.html")


@app.route("/students", methods=["GET", "POST"])
def students():
    if request.method == "GET":
        return jsonify({
            "students": manager.get_all(),
            "class_average": manager.get_class_average(),
            "total_students": len(manager.students),
            "total_grades": sum(len(s.grades) for s in manager.students.values())
        })
    data = request.get_json()
    name = (data.get("name") or "").strip()
    if not name:
        return jsonify({"error": "اسم الطالب مطلوب"}), 400
    try:
        manager.add_student(name)
        return jsonify({"success": True, "name": name})
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@app.route("/students/<path:n>", methods=["DELETE"])
def delete_student(n):
    try:
        manager.delete_student(n)
        return jsonify({"success": True})
    except ValueError as e:
        return jsonify({"error": str(e)}), 404


@app.route("/grades", methods=["POST"])
def add_grade():
    data = request.get_json()
    name    = (data.get("name")    or "").strip()
    subject = (data.get("subject") or "").strip()
    score   = data.get("score")
    if not name or not subject or score is None:
        return jsonify({"error": "أكمل جميع الحقول"}), 400
    try:
        score = float(score)
        if not (0 <= score <= 100):
            raise ValueError("الدرجة لازم تكون بين 0 و 100")
        manager.add_grade(name, subject, score)
        return jsonify({"success": True})
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@app.route("/grades/<path:n>/<int:idx>", methods=["DELETE"])
def delete_grade(n, idx):
    try:
        manager.remove_grade(n, idx)
        return jsonify({"success": True})
    except ValueError as e:
        return jsonify({"error": str(e)}), 404


if __name__ == "__main__":
    app.run(debug=True)
