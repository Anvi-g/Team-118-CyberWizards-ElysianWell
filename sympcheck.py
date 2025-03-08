from app import db, Symptom, app

# Ensure we are inside the Flask app context
with app.app_context():
    symptoms = Symptom.query.all()
    if not symptoms:
        print("🔴 No symptoms found in the database!")
    else:
        print("🟢 Symptoms in Database:")
        for symptom in symptoms:
            print(f"'{symptom.name}' | Tip: {symptom.tip}")
