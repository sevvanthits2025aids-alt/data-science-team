from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
from werkzeug.security import check_password_hash, generate_password_hash

from main import (
    choose_advice,
    clean_input,
    ensure_users_file,
    get_analytics_data,
    get_metrics,
    get_risk_level,
    load_data,
    load_history_records,
    load_users,
    predict_disease,
    save_history,
    save_user,
    update_password,
)

from vaccine import get_vaccine_info, list_available_vaccines
from disease_analyzer import create_analyzer
from medical_dataset import get_severity_accuracy_data, get_statistics

app = Flask(__name__, static_folder="static", template_folder="templates")
app.secret_key = "replace-with-a-secure-random-key"

# Initialize enhanced disease analyzer
disease_analyzer = create_analyzer()

try:
    data_frame = load_data()
except FileNotFoundError as error:
    data_frame = None
    print(f"[startup] {error}")

ensure_users_file()


def authenticated():
    return "username" in session


@app.route("/")
def index():
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip().lower()
        password = request.form.get("password", "").strip()

        users = load_users()
        if username in users and check_password_hash(users[username], password):
            session["username"] = username
            return redirect(url_for("dashboard"))

        flash("Invalid username or password.")

    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username", "").strip().lower()
        password = request.form.get("password", "").strip()
        confirm_password = request.form.get("confirm_password", "").strip()

        if not username or not password:
            flash("Username and password are required.")
        elif password != confirm_password:
            flash("Passwords do not match.")
        else:
            users = load_users()
            if username in users:
                flash("Username already exists.")
            else:
                save_user(username, generate_password_hash(password))
                flash("Account created successfully. Please log in.")
                return redirect(url_for("login"))

    return render_template("register.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route("/dashboard")
def dashboard():
    if not authenticated():
        return redirect(url_for("login"))

    metrics = get_metrics(session["username"])
    return render_template(
        "dashboard.html",
        page_title="Dashboard",
        section_title="Overview",
        current_page="dashboard",
        username=session["username"],
        total_predictions=metrics["total_predictions"],
        recent_disease=metrics["recent_disease"],
        health_status=metrics["health_status"],
    )


@app.route("/chat")
def chat():
    if not authenticated():
        return redirect(url_for("login"))

    return render_template(
        "chat.html",
        page_title="Chatbot",
        section_title="Live assistant",
        current_page="chat",
        username=session["username"],
    )


@app.route("/prediction")
def prediction():
    if not authenticated():
        return redirect(url_for("login"))

    return render_template(
        "prediction.html",
        page_title="Disease Prediction",
        section_title="Symptom analysis",
        current_page="prediction",
        username=session["username"],
    )


@app.route("/history")
def history():
    if not authenticated():
        return redirect(url_for("login"))

    records = list(reversed(load_history_records(session["username"])))
    return render_template(
        "history.html",
        page_title="History",
        section_title="Saved sessions",
        current_page="history",
        username=session["username"],
        records=records,
    )


@app.route("/analytics")
def analytics():
    if not authenticated():
        return redirect(url_for("login"))

    history_items = load_history_records(session["username"])
    analytics_data = get_analytics_data(history_items)

    return render_template(
        "analytics.html",
        page_title="Analytics",
        section_title="Health trends",
        current_page="analytics",
        username=session["username"],
        disease_labels=analytics_data["disease_labels"],
        disease_values=analytics_data["disease_values"],
        risk_labels=analytics_data["risk_labels"],
        risk_values=analytics_data["risk_values"],
        trend_labels=analytics_data["trend_labels"],
        trend_values=analytics_data["trend_values"],
    )


@app.route("/vaccine")
def vaccine():
    if not authenticated():
        return redirect(url_for("login"))

    # Get all diseases from the vaccine database for the dropdown
    from vaccine import VACCINE_DATABASE
    all_diseases = sorted(VACCINE_DATABASE.keys())
    disease_list = [disease.title() for disease in all_diseases]
    
    return render_template(
        "vaccine.html",
        page_title="Vaccine Info",
        section_title="Immunization lookup",
        current_page="vaccine",
        username=session["username"],
        disease_list=disease_list,
    )


@app.route("/profile", methods=["GET", "POST"])
def profile():
    if not authenticated():
        return redirect(url_for("login"))

    if request.method == "POST":
        current_password = request.form.get("current_password", "").strip()
        new_password = request.form.get("new_password", "").strip()
        confirm_password = request.form.get("confirm_password", "").strip()

        users = load_users()
        stored_hash = users.get(session["username"])

        if not stored_hash or not check_password_hash(stored_hash, current_password):
            flash("Your current password is incorrect.")
        elif new_password != confirm_password:
            flash("New passwords do not match.")
        else:
            update_password(session["username"], generate_password_hash(new_password))
            flash("Password updated successfully.")
            return redirect(url_for("profile"))

    metrics = get_metrics(session["username"])
    return render_template(
        "profile.html",
        page_title="Profile Settings",
        section_title="Account security",
        current_page="profile",
        username=session["username"],
        total_predictions=metrics["total_predictions"],
    )


@app.route("/predict", methods=["POST"])
def predict():
    if not authenticated():
        return jsonify({"error": "Authentication required."}), 401

    payload = request.get_json(silent=True) or {}
    user_text = payload.get("text", "").strip()
    if not user_text:
        return jsonify({"error": "Please enter your symptoms."}), 400

    # Clean and normalize symptoms
    symptoms = clean_input(user_text)
    
    # Check if symptoms are sufficient
    if not symptoms or len(symptoms) < 2:
        return jsonify({
            "error": "Cannot determine disease with given symptoms",
            "message": "Please provide at least 2 symptoms for accurate analysis.",
            "input_symptoms": symptoms,
        }), 400

    # Use enhanced analyzer for predictions
    predictions, confidence_note = disease_analyzer.analyze_symptoms(symptoms)
    
    if not predictions:
        return jsonify({
            "error": "Cannot determine disease with given symptoms",
            "message": confidence_note or "Symptoms are too non-specific to predict any disease.",
            "input_symptoms": symptoms,
        }), 400
    
    # Format enhanced results with medical reasoning
    results = []
    for prediction in predictions:
        # Save only the top prediction to history
        if prediction["rank"] == 1:
            save_history(
                session["username"],
                symptoms,
                prediction["disease"],
                prediction["confidence"],
                "High" if prediction["confidence"] >= 75 else ("Medium" if prediction["confidence"] >= 50 else "Low")
            )
        
        results.append({
            "rank": prediction["rank"],
            "disease": prediction["disease"],
            "category": prediction["category"],
            "confidence": prediction["confidence"],
            "risk_level": "High" if prediction["confidence"] >= 75 else ("Medium" if prediction["confidence"] >= 50 else "Low"),
            "severity": prediction["severity"],
            "matched_symptoms": prediction["matched_symptoms"],
            "unmatched_primary_symptoms": prediction["unmatched_primary"][:3],  # Show top 3
            "medical_reasoning": prediction["medical_reasoning"],
            "recommendations": prediction["recommendations"],
        })
    
    # Get urgency level
    urgency = disease_analyzer.suggest_medical_attention(predictions)
    
    return jsonify({
        "predictions": results,
        "input_symptoms": symptoms,
        "total_matches": len(results),
        "confidence_note": confidence_note,
        "urgency_level": urgency,
        "status": "enhanced_analysis_complete"
    })


@app.route("/vaccine-info", methods=["POST"])
def vaccine_info():
    if not authenticated():
        return jsonify({"error": "Authentication required."}), 401

    payload = request.get_json(silent=True) or {}
    disease = payload.get("disease", "").strip()
    if not disease:
        return jsonify({"error": "Please provide a disease name."}), 400

    vaccine_data = get_vaccine_info(disease)
    return jsonify(vaccine_data)


@app.route("/severity-accuracy-chart")
def severity_accuracy_chart():
    """Get severity vs accuracy data for visualization."""
    if not authenticated():
        return redirect(url_for("login"))
    
    severity_data = get_severity_accuracy_data()
    stats = get_statistics()
    
    # Format data for chart
    chart_data = []
    for severity_level, diseases in severity_data.items():
        if diseases:
            avg_accuracy = sum(d["accuracy"] for d in diseases) / len(diseases)
            chart_data.append({
                "severity": severity_level,
                "accuracy": round(avg_accuracy, 1),
                "disease_count": len(diseases),
                "diseases": [d["disease"] for d in diseases]
            })
    
    return render_template(
        "analytics.html",
        page_title="Disease Severity vs Accuracy Analytics",
        section_title="Prediction accuracy by disease severity",
        current_page="analytics",
        username=session["username"],
        chart_data=chart_data,
        statistics=stats,
        disease_labels=[d["severity"] for d in chart_data],
        disease_values=[d["accuracy"] for d in chart_data],
        risk_labels=None,
        risk_values=None,
        trend_labels=None,
        trend_values=None,
    )


@app.route("/dataset-stats")
def dataset_stats():
    """Get dataset statistics."""
    if not authenticated():
        return jsonify({"error": "Authentication required."}), 401
    
    stats = get_statistics()
    severity_data = get_severity_accuracy_data()
    
    # Build detailed response
    disease_details = []
    for disease_name, data in severity_data.items():
        if data:
            accuracies = [d["accuracy"] for d in data]
            disease_details.append({
                "severity": disease_name,
                "diseases": [d["disease"] for d in data],
                "average_accuracy": round(sum(accuracies) / len(accuracies), 1),
                "count": len(data)
            })
    
    return jsonify({
        "statistics": stats,
        "severity_breakdown": disease_details,
        "status": "success"
    })


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
