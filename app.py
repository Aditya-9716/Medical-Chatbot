from flask import Flask, render_template, request
import openai

app = Flask(__name__)

# Set your OpenAI API key here
openai.api_key = ""

# Mocked responses for common medical queries
def get_response(prompt):
    mock_responses = {
        "what are the flu symptoms": "Common symptoms of the flu include fever, chills, muscle aches, cough, congestion, runny nose, headaches, and fatigue. If you experience these symptoms, it's important to rest, stay hydrated, and take over-the-counter medications to alleviate symptoms. If symptoms persist, consult a healthcare provider.",
        "can you provide me detail about common cold treatment": "While there is no cure for the common cold, you can relieve symptoms by resting, staying hydrated, and using over-the-counter medications such as decongestants, cough suppressants, and pain relievers.",
        "tell me the headache causes": "Headaches can be caused by stress, dehydration, poor posture, eye strain, or underlying medical conditions like migraines.",
        "what are the fever remedies": "To reduce a fever, stay hydrated, rest, and use over-the-counter medications like acetaminophen or ibuprofen.",
        "what are the sore throat relief": "For a sore throat, you can try gargling warm salt water, staying hydrated, using throat lozenges, and taking over-the-counter pain relievers.",
        "what are the covid-19 symptoms": "Common symptoms of COVID-19 include fever, cough, fatigue, loss of taste or smell, and difficulty breathing. If you suspect you have COVID-19, please get tested and follow public health guidelines.",
        "what are the stomach ache treatment": "For a stomach ache, try drinking clear fluids, eating bland foods, and avoiding spicy or fatty foods. If the pain is severe or persistent, consult a healthcare provider.",
        "please tell me about allergy symptoms": "Allergy symptoms can include sneezing, itching, runny or stuffy nose, and watery eyes. Over-the-counter antihistamines and decongestants can help relieve symptoms.",
        "can you give me some high blood pressure advice": "To manage high blood pressure, maintain a healthy diet, exercise regularly, reduce salt intake, and take any prescribed medications. Regular monitoring and consultations with a healthcare provider are important.",
        "how can i manage diabetes": "Managing diabetes involves monitoring blood sugar levels, following a healthy diet, exercising regularly, and taking prescribed medications. Regular check-ups with a healthcare provider are crucial.",
        "give me suggestions for back pain relief": "To relieve back pain, try resting, applying ice or heat, taking over-the-counter pain relievers, and doing gentle stretches. If the pain persists, consult a healthcare provider.",
        "anxiety management": "Managing anxiety can involve practicing relaxation techniques, exercising, getting enough sleep, and seeking support from a mental health professional if needed.",
        "insomnia remedies": "For insomnia, maintain a regular sleep schedule, create a restful sleeping environment, limit caffeine and screen time before bed, and try relaxation techniques such as deep breathing or meditation.",
        "asthma symptoms": "Common asthma symptoms include wheezing, shortness of breath, chest tightness, and coughing, especially at night or early in the morning. It's important to follow your asthma action plan and take prescribed medications.",
        "depression signs": "Signs of depression can include persistent sadness, loss of interest in activities, changes in appetite or weight, difficulty sleeping, and feelings of worthlessness. Seeking support from a mental health professional is important.",
        "hello": "Hello! How can I assist you today?",
        "hi": "Hi there! What can I help you with?",
        "how are you": "I'm a medical chatbot, so I don't have feelings, but I'm here to help you with your questions!",
        "what is your name": "I'm your medical assistant chatbot. How can I help you today?",
        "thank you": "You're welcome! If you have any more questions, feel free to ask.",
        "bye": "Goodbye! Take care and stay healthy!",
        "exit": "Goodbye! If you have any more questions later, feel free to come back.",
        "flu symptoms": "Common symptoms of the flu include fever, chills, muscle aches, cough, congestion, runny nose, headaches, and fatigue. If you experience these symptoms, it's important to rest, stay hydrated, and take over-the-counter medications to alleviate symptoms. If symptoms persist, consult a healthcare provider.",
        "common cold treatment": "While there is no cure for the common cold, you can relieve symptoms by resting, staying hydrated, and using over-the-counter medications such as decongestants, cough suppressants, and pain relievers.",
        "headache causes": "Headaches can be caused by stress, dehydration, poor posture, eye strain, or underlying medical conditions like migraines.",
        "fever remedies": "To reduce a fever, stay hydrated, rest, and use over-the-counter medications like acetaminophen or ibuprofen.",
        "sore throat relief": "For a sore throat, you can try gargling warm salt water, staying hydrated, using throat lozenges, and taking over-the-counter pain relievers.",
        "covid-19 symptoms": "Common symptoms of COVID-19 include fever, cough, fatigue, loss of taste or smell, and difficulty breathing. If you suspect you have COVID-19, please get tested and follow public health guidelines.",
        "stomach ache treatment": "For a stomach ache, try drinking clear fluids, eating bland foods, and avoiding spicy or fatty foods. If the pain is severe or persistent, consult a healthcare provider.",
        "allergy symptoms": "Allergy symptoms can include sneezing, itching, runny or stuffy nose, and watery eyes. Over-the-counter antihistamines and decongestants can help relieve symptoms.",
        "high blood pressure advice": "To manage high blood pressure, maintain a healthy diet, exercise regularly, reduce salt intake, and take any prescribed medications. Regular monitoring and consultations with a healthcare provider are important.",
        "how can i manage diabetes": "Managing diabetes involves monitoring blood sugar levels, following a healthy diet, exercising regularly, and taking prescribed medications. Regular check-ups with a healthcare provider are crucial.",
        "back pain relief": "To relieve back pain, try resting, applying ice or heat, taking over-the-counter pain relievers, and doing gentle stretches. If the pain persists, consult a healthcare provider.",
        "anxiety management": "Managing anxiety can involve practicing relaxation techniques, exercising, getting enough sleep, and seeking support from a mental health professional if needed.",
        "insomnia remedies": "For insomnia, maintain a regular sleep schedule, create a restful sleeping environment, limit caffeine and screen time before bed, and try relaxation techniques such as deep breathing or meditation.",
        "asthma symptoms": "Common asthma symptoms include wheezing, shortness of breath, chest tightness, and coughing, especially at night or early in the morning. It's important to follow your asthma action plan and take prescribed medications.",
        "depression signs": "Signs of depression can include persistent sadness, loss of interest in activities, changes in appetite or weight, difficulty sleeping, and feelings of worthlessness. Seeking support from a mental health professional is important.",
        "i am 25 years old and i am having fever what could be the reason": "Fever can be caused by a variety of factors such as infections (bacterial or viral), heat exhaustion, or inflammatory conditions. It's best to monitor your symptoms and consult a healthcare professional if the fever persists or is accompanied by other symptoms.",
        "i am 30 years old and i have a headache what could be the reason": "Headaches can be caused by stress, dehydration, eye strain, or underlying health conditions. Ensure you stay hydrated, rest, and seek medical advice if the headache is severe or persistent.",
        "i am 40 years old and i am experiencing chest pain what could be the reason": "Chest pain can be a serious symptom and could be related to heart conditions, respiratory issues, or gastrointestinal problems. It's important to seek immediate medical attention.",
        "i am 50 years old and i have a cough what could be the reason": "A cough can be caused by infections, allergies, or chronic conditions like asthma. If it's persistent or accompanied by other symptoms like fever, consult a healthcare provider.",
        "i am 35 years old and i am feeling dizzy what could be the reason": "Dizziness can be related to dehydration, low blood pressure, or other underlying conditions. Rest and hydrate, and if dizziness continues, seek medical advice.",
        "i am 60 years old and i have joint pain what could be the reason": "Joint pain at this age could be due to arthritis, overuse, or injury. It's advisable to consult a healthcare provider for a proper diagnosis and treatment plan.",
        "i am 20 years old and i have a sore throat what could be the reason": "A sore throat can be due to a viral infection, allergies, or irritants. Rest, stay hydrated, and if it persists for more than a few days, consider seeing a doctor.",
        "i am 45 years old and i have shortness of breath what could be the reason": "Shortness of breath could be due to respiratory issues, heart conditions, or anxiety. It's important to seek medical attention if it's sudden or severe.",
        "i am 28 years old and i have a sore throat what could be the reason": "A sore throat is often caused by viral infections like the common cold or flu. Allergies, dry air, or throat irritation could also be factors. If it persists, consider seeking medical advice.",
        "i am 45 years old and i have shortness of breath what could be the reason": "Shortness of breath could be due to respiratory issues like asthma or bronchitis, or heart-related conditions. It's important to get medical attention, especially if it's sudden or severe.",
        "i am 55 years old and i have stomach pain what could be the reason": "Stomach pain could be due to indigestion, ulcers, or more serious conditions like gallstones. Persistent or severe pain should be evaluated by a healthcare provider.",
        "i am 32 years old and i am feeling fatigued what could be the reason": "Fatigue can result from lack of sleep, stress, poor diet, or underlying health issues such as anemia or thyroid problems. It's important to address lifestyle factors and consult a doctor if fatigue is ongoing.",
        "i am 22 years old and i have a rash what could be the reason": "Rashes can be caused by allergies, skin conditions like eczema, or infections. If the rash is itchy, painful, or spreading, it's best to seek medical advice.",
        "i am 37 years old and i have nausea what could be the reason": "Nausea can be caused by food poisoning, motion sickness, pregnancy, or infections. If it persists, consider seeing a healthcare professional for further evaluation.",
        "i am 65 years old and i have swollen ankles what could be the reason": "Swollen ankles can be due to fluid retention, heart failure, or kidney problems, especially at an older age. It's important to get it checked by a doctor.",
        "i am 50 years old and i have back pain what could be the reason": "Back pain can result from muscle strain, herniated discs, or arthritis. Maintaining good posture, staying active, and seeking medical advice if the pain persists or is severe is recommended.",
        "i am 29 years old and i have difficulty sleeping what could be the reason": "Difficulty sleeping could be due to stress, anxiety, or poor sleep habits. It's important to establish a good sleep routine and consult a healthcare provider if the issue continues.",
        "i am 48 years old and i have tingling in my hands what could be the reason": "Tingling in the hands could be due to nerve compression, carpal tunnel syndrome, or circulatory issues. It's advisable to consult a healthcare provider for proper diagnosis.",
        "i am 55 years old and i have stomach pain what could be the reason": "Stomach pain can be caused by indigestion, infections, or more serious conditions like ulcers. If the pain is severe or persistent, seek medical advice.",
    }

    disease_precautions = {
        "Drug Reaction": "stop irritation, consult nearest hospital, stop taking drug, follow up",
        "Malaria": "Consult nearest hospital, avoid oily food, avoid non veg food, keep mosquitos out",
        "Allergy": "apply calamine, cover area with bandage, use ice to compress itching",
        "Hypothyroidism": "reduce stress, exercise, eat healthy, get proper sleep",
        "Psoriasis": "wash hands with warm soapy water, stop bleeding using pressure, consult doctor, salt baths",
        "GERD": "avoid fatty spicy food, avoid lying down after eating, maintain healthy weight, exercise",
        "Chronic cholestasis": "cold baths, anti-itch medicine, consult doctor, eat healthy",
        "hepatitis A": "Consult nearest hospital, wash hands through, avoid fatty spicy food, medication",
        "Osteoarthristis": "acetaminophen, consult nearest hospital, follow up, salt baths",
        "(vertigo) Paroymsal Positional Vertigo": "lie down, avoid sudden change in body, avoid abrupt head movement, relax",
        "Hypoglycemia": "lie down on side, check in pulse, drink sugary drinks, consult doctor",
        "Acne": "bath twice, avoid fatty spicy food, drink plenty of water, avoid too many products",
        "Diabetes": "have balanced diet, exercise, consult doctor, follow up",
        "Impetigo": "soak affected area in warm water, use antibiotics, remove scabs with wet compressed cloth, consult doctor",
        "Hypertension": "meditation, salt baths, reduce stress, get proper sleep",
        "Peptic ulcer disease": "avoid fatty spicy food, consume probiotic food, eliminate milk, limit alcohol",
        "Dimorphic hemorrhoids (piles)": "avoid fatty spicy food, consume witch hazel, warm bath with epsom salt, consume aloe vera juice",
        "Common Cold": "drink vitamin C rich drinks, take vapour, avoid cold food, keep fever in check",
        "Chicken pox": "use neem in bathing, consume neem leaves, take vaccine, avoid public places",
        "Cervical spondylosis": "use heating pad or cold pack, exercise, take otc pain reliever, consult doctor",
        "Hyperthyroidism": "eat healthy, massage, use lemon balm, take radioactive iodine treatment",
        "Urinary tract infection": "drink plenty of water, increase vitamin C intake, drink cranberry juice, take probiotics",
        "Varicose veins": "lie down flat and raise the leg high, use ointments, use vein compression, don't stand still for long",
        "AIDS": "avoid open cuts, wear PPE if possible, consult doctor, follow up",
        "Paralysis (brain hemorrhage)": "massage, eat healthy, exercise, consult doctor",
        "Typhoid": "eat high calorie vegetables, antibiotic therapy, consult doctor, medication",
        "Hepatitis B": "consult nearest hospital, vaccination, eat healthy, medication",
        "Fungal infection": "bath twice, use dettol or neem in bathing water, keep infected area dry, use clean clothes",
        "Hepatitis C": "Consult nearest hospital, vaccination, eat healthy, medication",
        "Migraine": "meditation, reduce stress, use polaroid glasses in sun, consult doctor",
        "Bronchial Asthma": "switch to loose clothing, take deep breaths, get away from trigger, seek help",
        "Alcoholic hepatitis": "stop alcohol consumption, consult doctor, medication, follow up",
        "Jaundice": "drink plenty of water, consume milk thistle, eat fruits and high fiber food, medication",
        "Hepatitis E": "stop alcohol consumption, rest, consult doctor, medication",
        "Dengue": "drink papaya leaf juice, avoid fatty spicy food, keep mosquitoes away, keep hydrated",
        "Hepatitis D": "consult doctor, medication, eat healthy, follow up",
        "Heart attack": "call ambulance, chew or swallow aspirin, keep calm",
        "Pneumonia": "consult doctor, medication, rest, follow up",
        "Arthritis": "exercise, use hot and cold therapy, try acupuncture, massage",
        "Gastroenteritis": "stop eating solid food for a while, try taking small sips of water, rest, ease back into eating",
        "Tuberculosis": "cover mouth, consult doctor, medication, rest",
    }

    disease_descriptions = {
        "Drug Reaction": "An adverse drug reaction (ADR) is an injury caused by taking medication. ADRs may occur following a single dose or prolonged administration of a drug or result from the combination of two or more drugs.",
        "Malaria": "An infectious disease caused by protozoan parasites from the Plasmodium family that can be transmitted by the bite of the Anopheles mosquito or by a contaminated needle or transfusion. Falciparum malaria is the most deadly type.",
        "Allergy": "A condition in which the immune system reacts abnormally to a foreign substance.",
        "Hypothyroidism": "A condition in which the thyroid gland doesn't produce enough thyroid hormone.",
        "Psoriasis": "A condition in which skin cells build up and form scales and itchy, dry patches.",
        "GERD": "Gastroesophageal reflux disease (GERD) is a chronic digestive disease. GERD occurs when stomach acid or, occasionally, stomach content, flows back into your food pipe (esophagus). The backwash (reflux) irritates the lining of your esophagus and causes GERD.",
        "Chronic cholestasis": "Chronic cholestasis is a long-term condition where bile cannot flow from the liver to the duodenum.",
        "Hepatitis A": "A highly contagious liver infection caused by the hepatitis A virus.",
        "Osteoarthritis": "A type of arthritis that occurs when flexible tissue at the ends of bones wears down.",
        "(vertigo) Paroymsal Positional Vertigo": "A sudden sensation that you're spinning or that the inside of your head is spinning.",
        "Hypoglycemia": "A condition caused by a very low level of blood sugar (glucose), your body's main energy source.",
        "Acne": "A skin condition that occurs when your hair follicles become plugged with oil and dead skin cells.",
        "Diabetes": "A group of diseases that result in too much sugar in the blood (high blood glucose).",
        "Impetigo": "A highly contagious skin infection that causes red sores on the face.",
        "Hypertension": "A condition in which the force of the blood against the artery walls is too high.",
        "Peptic ulcer disease": "Peptic ulcer disease is a condition in which open sores develop on the inside lining of your stomach and the upper portion of your small intestine.",
        "Dimorphic hemorrhoids (piles)": "Swollen and inflamed veins in the rectum and anus that cause discomfort and bleeding.",
        "Common Cold": "A common viral infection of the nose and throat.",
        "Chicken pox": "A highly contagious viral infection causing an itchy, blister-like rash on the skin.",
        "Cervical spondylosis": "Age-related wear and tear affecting the spinal disks in your neck.",
        "Hyperthyroidism": "The overproduction of a hormone by the butterfly-shaped gland in the neck (thyroid).",
        "Urinary tract infection": "An infection in any part of the urinary system, the kidneys, bladder, or urethra.",
        "Varicose veins": "Gnarled, enlarged veins, most commonly appearing in the legs and feet.",
        "AIDS": "A chronic, potentially life-threatening condition caused by the human immunodeficiency virus (HIV).",
        "Paralysis (brain hemorrhage)": "The loss of the ability to move (and sometimes to feel anything) in part or most of the body, typically as a result of illness, poison, or injury.",
        "Typhoid": "A bacterial infection that can spread throughout the body, affecting many organs. Without prompt treatment, it can cause serious complications and be fatal.",
        "Hepatitis B": "A serious liver infection caused by the hepatitis B virus that's easily preventable by a vaccine.",
        "Fungal infection": "A fungal infection, also called mycosis, is a skin disease caused by a fungus.",
        "Hepatitis C": "An infection caused by a virus that attacks the liver and leads to inflammation.",
        "Migraine": "A headache of varying intensity, often accompanied by nausea and sensitivity to light and sound.",
        "Bronchial Asthma": "A condition in which your airways narrow and swell and may produce extra mucus.",
        "Alcoholic hepatitis": "Liver inflammation caused by drinking too much alcohol.",
        "Jaundice": "A yellow tint to the skin or eyes caused by an excess of bilirubin, a substance created when red blood cells break down.",
        "Hepatitis E": "A liver disease caused by the hepatitis E virus: a non-enveloped, positive-sense, single-stranded ribonucleic acid (RNA) virus.",
        "Dengue": "A mosquito-borne viral disease occurring in tropical and subtropical areas.",
        "Hepatitis D": "A serious liver disease caused by infection with the hepatitis D virus, a virus that requires hepatitis B for its replication.",
        "Heart attack": "A blockage of blood flow to the heart muscle.",
        "Pneumonia": "An infection that inflames the air sacs in one or both lungs. The air sacs may fill with fluid or pus (purulent material), causing a cough with phlegm or pus, fever, chills, and difficulty breathing.",
        "Arthritis": "Inflammation of one or more joints, causing pain and stiffness that can worsen with age.",
        "Gastroenteritis": "An intestinal infection marked by diarrhea, cramps, nausea, vomiting, and fever.",
        "Tuberculosis": "A potentially serious infectious bacterial disease that mainly affects the lungs.",
    }

    # Checking if the prompt matches any key in the dictionaries
    for key in mock_responses:
        if key in prompt.lower():
            return mock_responses[key]

    # Checking if the prompt matches any key in the disease precautions and descriptions dictionaries
    for disease in disease_precautions:
        if disease.lower() in prompt.lower():
            description = disease_descriptions.get(disease, "Description not found.")
            precautions = disease_precautions.get(disease, "Precautions not found.")
            return f"Disease: {disease}\nDescription: {description}\nPrecautions: {precautions}"

    # Default response if no match is found
    return "I'm sorry, I don't have information on that topic. Please consult a healthcare professional."

@app.route("/", methods=["GET", "POST"])
def index():
    response = None
    if request.method == "POST":
        user_input = request.form["user_input"]
        response = get_response(user_input)
    return render_template("index.html", response=response)

if __name__ == "__main__":
    app.run(debug=True)
