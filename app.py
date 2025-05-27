from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    schedule = []
    error = ""
    if request.method == "POST":
        daily_hours = request.form.get("daily_hours", "").strip()
        subjects_text = request.form.get("subjects", "").strip()
        if not daily_hours or not subjects_text:
            error = "Please enter valid daily study hours and at least one subject with hours."
        else:
            try:
                daily_hours = float(daily_hours)
                subjects = []
                for line in subjects_text.splitlines():
                    if "," not in line:
                        raise ValueError(
                            f"Invalid format in line: '{line}'. Use Subject,Hours."
                        )
                    subject, hours = line.split(",", 1)
                    subjects.append((subject.strip(), float(hours.strip())))
                total_hours = sum(hours for subject, hours in subjects)
                schedule = [
                    (subject, round(hours / total_hours * daily_hours, 2))
                    for subject, hours in subjects
                ]
            except ValueError as e:
                error = f"Error: {e}"
    return render_template("index.html", schedule=schedule, error=error)


if __name__ == "__main__":
    app.run(debug=True)
