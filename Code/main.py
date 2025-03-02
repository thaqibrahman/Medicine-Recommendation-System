from flask import Flask, request, render_template

# flask app
app = Flask(__name__, template_folder="templates")


# Load data from CSVs (simulated as dictionaries for simplicity in this example)
description = {
    'Fungal infection': 'A fungal infection typically affects the skin.',
    'Allergy': 'An allergy occurs when your immune system reacts to a foreign substance.',
    'Diabetes': 'A chronic condition characterized by high blood sugar levels.',
    'Hypertension': 'A condition where blood pressure in the arteries is persistently elevated.',
    'Anemia': 'A condition where the blood lacks enough healthy red blood cells.',
    'Arthritis': 'A condition causing inflammation and pain in the joints.',
    'Malaria': 'A disease caused by a parasite transmitted by mosquito bites.',
    'Common Cold': 'A viral infection causing a runny nose, cough, and sore throat.',
    'Flu': 'A contagious respiratory illness caused by influenza viruses.',
    # Add more descriptions here...
}

precautions = {
    'Fungal infection': ['Use antifungal cream', 'Keep area dry', 'Avoid sharing personal items', 'Maintain hygiene'],
    'Allergy': ['Avoid allergens', 'Use antihistamines', 'Consult a doctor', 'Keep your environment clean'],
    'Diabetes': ['Monitor blood sugar', 'Maintain a healthy diet', 'Exercise regularly', 'Consult a doctor'],
    'Hypertension': ['Reduce salt intake', 'Exercise regularly', 'Avoid stress', 'Monitor blood pressure'],
    'Anemia': ['Eat iron-rich foods', 'Take iron supplements', 'Avoid caffeinated drinks with meals', 'Consult a doctor'],
    'Arthritis': ['Maintain a healthy weight', 'Exercise regularly', 'Use heat or cold therapy', 'Consult a rheumatologist'],
    'Malaria': ['Use mosquito nets', 'Apply insect repellents', 'Wear protective clothing', 'Take antimalarial drugs'],
    'Common Cold': ['Stay hydrated', 'Get plenty of rest', 'Use saline nasal spray', 'Avoid close contact with sick people'],
    'Flu': ['Get vaccinated', 'Wash hands frequently', 'Avoid crowded places', 'Stay home if sick'],
}

medications = {
    'Fungal infection': ['Clotrimazole', 'Ketoconazole'],
    'Allergy': ['Loratadine', 'Cetirizine'],
    'Diabetes': ['Metformin', 'Insulin'],
    'Hypertension': ['Amlodipine', 'Lisinopril'],
    'Anemia': ['Ferrous sulfate', 'Vitamin B12 supplements'],
    'Arthritis': ['Ibuprofen', 'Methotrexate'],
    'Malaria': ['Chloroquine', 'Artemisinin-based combination therapies'],
    'Common Cold': ['Paracetamol', 'Decongestants'],
    'Flu': ['Oseltamivir', 'Zanamivir'],
    # Add more medications here...
}

diets = {
    'Fungal infection': ['Yogurt', 'Probiotic-rich foods'],
    'Allergy': ['Foods rich in Vitamin C', 'Ginger', 'Turmeric'],
    'Diabetes': ['Low-carb foods', 'Whole grains', 'Vegetables'],
    'Hypertension': ['Low-sodium foods', 'Fruits and vegetables', 'DASH diet'],
    'Anemia': ['Iron-rich foods like spinach', 'Red meat', 'Lentils', 'Vitamin C-rich foods'],
    'Arthritis': ['Anti-inflammatory foods like fatty fish, spinach, and nuts'],
    'Malaria': ['Foods rich in Vitamin C and antioxidants', 'Coconut water'],
    'Common Cold': ['Warm fluids like soup', 'Vitamin C-rich foods like oranges'],
    'Flu': ['Hydrating fluids', 'Protein-rich foods like eggs and chicken'],
}

workout = {
    'Fungal infection': 'Light exercises to avoid excessive sweating.',
    'Allergy': 'Breathing exercises and yoga.',
    'Diabetes': 'Aerobic exercises like walking, cycling, or swimming.',
    'Hypertension': 'Moderate aerobic activities like brisk walking or cycling.',
    'Anemia': 'Light exercises and short-duration yoga.',
    'Arthritis': 'Gentle stretching and low-impact exercises like swimming.',
    'Malaria': 'Light walking after recovery to rebuild strength.',
    'Common Cold': 'Light yoga or simple breathing exercises.',
    'Flu': 'Rest is essential; avoid intense activities during recovery.',
}

# Define a mapping between symptoms and diseases (rule-based logic)
symptom_to_disease = {
    'itching': 'Fungal infection',
    'dischromic _patches': 'Fungal infection',
    'skin_rash': 'Allergy',
    'continuous_sneezing': 'Allergy',
    'joint_pain': 'Arthritis',
    'high_fever': 'Malaria',
    'frequent urination': 'Diabetes',
    'increased thirst': 'Diabetes',
    'unexplained weight loss': 'Diabetes',
    'headache': 'Hypertension',
    'dizziness': 'Hypertension',
    'blurred vision': 'Hypertension',
    'fatigue': 'Anemia',
    'pale skin': 'Anemia',
    'shortness of breath': 'Anemia',
    'joint_pain': 'Arthritis',
    'swelling': 'Arthritis',
    'shivering': 'Malaria',
    'nausea': 'Malaria',
    'runny_nose': 'Common Cold',
    'cough': 'Flu',
    'sore_throat': 'Flu',
    'muscle_pain': 'Flu',
    ('itching', 'dischromic _patches'): 'Fungal infection',
    ('skin_rash', 'continuous_sneezing'): 'Allergy',
    ('frequent urination', 'increased thirst', 'unexplained weight loss'): 'Diabetes',
    ('headache', 'dizziness', 'blurred vision'): 'Hypertension',
    ('fatigue', 'pale skin', 'shortness of breath'): 'Anemia',
    ('joint_pain', 'swelling'): 'Arthritis',
    ('shivering', 'nausea'): 'Malaria',
    ('runny_nose', 'cough'): 'Common Cold',
    ('sore_throat', 'muscle_pain', 'cough'): 'Flu',
    ('itching', 'dischromic _patches'): 'Fungal infection',
    ('itching', 'skin_rash'): 'Fungal infection',

    # Allergy
    ('skin_rash', 'continuous_sneezing'): 'Allergy',
    ('continuous_sneezing', 'runny_nose', 'itching'): 'Allergy',

    # Diabetes
    ('frequent urination', 'increased thirst', 'unexplained weight loss'): 'Diabetes',
    ('blurred vision', 'frequent urination'): 'Diabetes',

    # Hypertension
    ('headache', 'dizziness', 'blurred vision'): 'Hypertension',
    ('dizziness', 'nausea', 'fatigue'): 'Hypertension',

    # Anemia
    ('fatigue', 'pale skin', 'shortness of breath'): 'Anemia',
    ('fatigue', 'dizziness', 'pale skin'): 'Anemia',

    # Arthritis
    ('joint_pain', 'swelling', 'fatigue'): 'Arthritis',
    ('joint_pain', 'stiffness', 'swelling'): 'Arthritis',

    # Malaria
    ('shivering', 'nausea', 'high_fever'): 'Malaria',
    ('high_fever', 'sweating', 'headache'): 'Malaria',

    # Common Cold
    ('runny_nose', 'cough', 'sore_throat'): 'Common Cold',
    ('cough', 'sore_throat', 'mild_fever'): 'Common Cold',

    # Flu
    ('sore_throat', 'muscle_pain', 'cough'): 'Flu',
    ('high_fever', 'muscle_pain', 'headache'): 'Flu',

    # COVID-19 (optional addition for relevance)
    ('cough', 'fever', 'loss_of_smell'): 'COVID-19',
    ('shortness of breath', 'fever', 'dry_cough'): 'COVID-19',
}

# Helper function to get disease information
def helper(dis):
    desc = description.get(dis, 'Description not available.')
    pre = precautions.get(dis, [])
    med = medications.get(dis, [])
    die = diets.get(dis, [])
    wrkout = workout.get(dis, 'Workout recommendations not available.')
    return desc, pre, med, die, wrkout

# Rule-based prediction function
def get_predicted_value(patient_symptoms):
    # Check for exact combinations
    for symptoms_combo, disease in symptom_to_disease.items():
        if all(symptom in patient_symptoms for symptom in symptoms_combo):
            return disease

    # If no combination matches, fall back to single symptoms
    disease_scores = {}
    for symptom in patient_symptoms:
        if symptom in symptom_to_disease:
            disease = symptom_to_disease[symptom]
            disease_scores[disease] = disease_scores.get(disease, 0) + 1

    return max(disease_scores, key=disease_scores.get) if disease_scores else "Consult a Doctor"

# Creating routes
@app.route("/")
def index():
    return render_template("index.html")

@app.route('/predict', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        symptoms = request.form.get('symptoms') or request.form.get('recognized_symptoms')
        if not symptoms or symptoms.strip() == "Symptoms":
            message = "Please either write symptoms or you have written misspelled symptoms."
            return render_template('index.html', message=message)
        else:
            user_symptoms = [s.strip() for s in symptoms.split(',')]
            predicted_disease = get_predicted_value(user_symptoms)
            dis_des, precautions, medications, rec_diet, workout = helper(predicted_disease)

            return render_template('index.html', predicted_disease=predicted_disease, dis_des=dis_des,
                                   my_precautions=precautions, medications=medications, my_diet=rec_diet,
                                   workout=workout)
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/contact')
def contact():
    return render_template("contact.html")

#@app.route('/developer')
#def developer():
#    return render_template("developer.html")

if __name__ == '__main__':
    app.run(debug=True, port=5001)