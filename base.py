from flask import Flask, request, render_template
import pandas as pd
import pickle

app = Flask(__name__)

# Load the pre-trained model
model = pickle.load(open("logmodel.pkl", "rb"))

def predictinpdata(input_df):
    # Perform prediction
    prediction = model.predict(input_df)[0]
    
    # Return a human-readable result
    if prediction == 1:
        return "YOU WILL GET PLACED"
    else:
        return "YOU WILL NOT GET PLACED"

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/reglink", methods=["POST"])
def getinputdata():
    try:
        # Extract form data and convert them to appropriate types with validation
        CGPA = float(request.form["CGPA"])
        if not (0 <= CGPA <= 10):
            return render_template("display.html", data="Error: CGPA must be between 0 and 10")

        Internships = int(request.form["Internships"])
        if Internships not in [0, 1, 2]:
            return render_template("display.html", data="Error: Invalid Internships value")

        Projects = int(request.form["Projects"])
        if Projects not in [1, 2, 3]:
            return render_template("display.html", data="Error: Invalid Projects value")

        WorkshopsCertifications = int(request.form["Workshops/Certifications"])
        if WorkshopsCertifications not in [0, 1, 2]:
            return render_template("display.html", data="Error: Invalid Workshops/Certifications value")

        AptitudeTestScore = float(request.form["AptitudeTestScore"])
        if not (0 <= AptitudeTestScore <= 100):
            return render_template("display.html", data="Error: Aptitude Test Score must be between 0 and 100")

        SoftSkillsRating = float(request.form["SoftSkillsRating"])
        if not (1 <= SoftSkillsRating <= 5):
            return render_template("display.html", data="Error: Soft Skills Rating must be between 1 and 5")

        SSC_Marks = float(request.form["SSC_Marks"])
        if not (0 <= SSC_Marks <= 100):
            return render_template("display.html", data="Error: SSC Marks must be between 0 and 100")

        HSC_Marks = float(request.form["HSC_Marks"])
        if not (0 <= HSC_Marks <= 100):
            return render_template("display.html", data="Error: HSC Marks must be between 0 and 100")

        # Convert 'Yes'/'No' to 1/0
        ExtracurricularActivities = 1 if request.form["ExtracurricularActivities"] == 'Yes' else 0
        PlacementTraining = 1 if request.form["PlacementTraining"] == 'Yes' else 0

        # Create a DataFrame with the input data
        input_df = pd.DataFrame({
            "CGPA": [CGPA],
            "Internships": [Internships],
            "Projects": [Projects],
            "Workshops/Certifications": [WorkshopsCertifications],
            "AptitudeTestScore": [AptitudeTestScore],
            "SoftSkillsRating": [SoftSkillsRating],
            "SSC_Marks": [SSC_Marks],
            "HSC_Marks": [HSC_Marks],
            "ExtracurricularActivities": [ExtracurricularActivities],
            "PlacementTraining": [PlacementTraining]
        })

        # Get the prediction result
        ans = predictinpdata(input_df)

        return render_template("display.html", data=ans)

    except ValueError as e:
        return render_template("display.html", data="Error: Invalid input format. Please enter numeric values where required.")
    except Exception as e:
        return render_template("display.html", data=f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    app.run(debug=True)
