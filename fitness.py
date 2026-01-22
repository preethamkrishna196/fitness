import streamlit as st
import time
import json
import os
import datetime
import pandas as pd
import random

try:
    from fpdf import FPDF
except ImportError:
    FPDF = None

# ---------------- Utility Functions ----------------
def calculate_bmi(weight, height_cm):
    height_m = height_cm / 100
    return weight / (height_m ** 2)

def bmi_category(bmi):
    if bmi < 18.5:
        return "Underweight"
    elif bmi < 24.9:
        return "Normal weight"
    elif bmi < 29.9:
        return "Overweight"
    else:
        return "Obese"

def add_bg_from_url():
    st.markdown(
        """
        <style>
        .stApp {
            background-image: url("https://images.pexels.com/photos/841130/pexels-photo-841130.jpeg");
            background-size: cover;
            background-attachment: fixed;
        }
        [data-testid="stSidebar"] {
            background-color: grey;
        }
        h1, h2, h3, label, p {
            color: white !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

# ---------------- Diet Section (Daily BMI Based) ----------------
def display_diet_plan(diet_type, bmi_cat, gender):
    st.subheader(f"{diet_type} Daily Diet Plan")

    gender_note = "Higher calorie needs" if gender == "Male" else "Moderate calorie needs"
    st.caption(f"👤 {gender} • {bmi_cat} • {gender_note}")

    if diet_type == "Vegetarian":
        plans = {
            "Underweight": {
                "Breakfast": "Oats + Milk + Banana",
                "Lunch": "Rice + Dal + Paneer",
                "Dinner": "Roti + Chickpeas",
                "Total": "≈1800 kcal | 90g protein"
            },
            "Normal weight": {
                "Breakfast": "Paneer Sandwich + Milk",
                "Lunch": "Dal + Rice",
                "Dinner": "Roti + Soybean",
                "Total": "≈1500 kcal | 85g protein"
            },
            "Overweight": {
                "Breakfast": "Sprouts + Green Tea",
                "Lunch": "Dal + Salad",
                "Dinner": "Veg Soup + Paneer",
                "Total": "≈1200 kcal | 80g protein"
            },
            "Obese": {
                "Breakfast": "Fruit Bowl",
                "Lunch": "Mixed Veg + Dal",
                "Dinner": "Soup + Salad",
                "Total": "≈1050 kcal | 70g protein"
            }
        }
    else:
        plans = {
            "Underweight": {
                "Breakfast": "4 Eggs + Milk",
                "Lunch": "Chicken + Rice",
                "Dinner": "Fish + Roti",
                "Total": "≈1900 kcal | 110g protein"
            },
            "Normal weight": {
                "Breakfast": "3 Eggs + Toast",
                "Lunch": "Chicken + Rice",
                "Dinner": "Omelette + Veggies",
                "Total": "≈1500 kcal | 95g protein"
            },
            "Overweight": {
                "Breakfast": "Boiled Eggs",
                "Lunch": "Grilled Chicken + Salad",
                "Dinner": "Fish Soup",
                "Total": "≈1200 kcal | 85g protein"
            },
            "Obese": {
                "Breakfast": "Fruit + Nuts",
                "Lunch": "Grilled Fish + Salad",
                "Dinner": "Soup",
                "Total": "≈1050 kcal | 75g protein"
            }
        }

    with st.expander("View Daily Diet Plan"):
        for meal, value in plans[bmi_cat].items():
            st.write(f"**{meal}:** {value}")

# ---------------- Weekly Diet Plan ----------------
def display_weekly_diet_plan(diet_type):
    st.subheader(f"🗓️ Weekly {diet_type} Diet Plan")

    weekly_plan = {
        "Monday": {
            "Veg": ["Upma + Chutney", "Rice + Dal + Veg", "Chapati + Paneer"],
            "Non-Veg": ["Eggs + Toast", "Chicken Curry + Rice", "Chapati + Egg Curry"]
        },
        "Tuesday": {
            "Veg": ["Idli + Sambar", "Chapati + Rajma", "Veg Pulao + Curd"],
            "Non-Veg": ["Omelette + Dosa", "Fish Curry + Chapati", "Chicken Pulao"]
        },
        "Wednesday": {
            "Veg": ["Poha", "Rice + Sambar + Veg", "Chapati + Mixed Veg"],
            "Non-Veg": ["Egg Bhurji + Bread", "Chicken Fry + Rice", "Chapati + Fish"]
        },
        "Thursday": {
            "Veg": ["Oats Porridge", "Lemon Rice + Curd", "Chapati + Dal"],
            "Non-Veg": ["Oats + Boiled Eggs", "Egg Curry + Rice", "Chapati + Chicken"]
        },
        "Friday": {
            "Veg": ["Veg Sandwich", "Rice + Veg Fry + Curd", "Chapati + Paneer"],
            "Non-Veg": ["Egg Sandwich", "Fish Curry + Rice", "Chapati + Egg Curry"]
        },
        "Saturday": {
            "Veg": ["Dosa + Chutney", "Veg Biryani + Raita", "Khichdi"],
            "Non-Veg": ["Dosa + Omelette", "Chicken Biryani + Raita", "Chicken Soup"]
        },
        "Sunday": {
            "Veg": ["Paratha + Curd", "Rice + Dal + Veg", "Veg Soup + Chapati"],
            "Non-Veg": ["Paratha + Omelette", "Mutton/Chicken Curry + Rice", "Egg Soup"]
        }
    }

    for day, meals in weekly_plan.items():
        with st.expander(day):
            selected_meals = meals["Veg"] if diet_type == "Vegetarian" else meals["Non-Veg"]
            st.write(f"**Breakfast:** {selected_meals[0]}")
            st.write(f"**Lunch:** {selected_meals[1]}")
            st.write(f"**Dinner:** {selected_meals[2]}")

# ---------------- Workout Tips ----------------
def display_gender_workout_tips(gender):
    st.subheader("Personalized Workout Tips")
    if gender == "Male":
        st.info("💪 Focus on strength training, compound lifts, 4–5 days/week.")
    else:
        st.info("🌸 Focus on toning, flexibility, core strength, 3–5 days/week.")

# ---------------- Workout Database ----------------
WORKOUT_DB = {
    "advanced": {
        "Chest": [
            {"name": "Bench Press", "sets": 4, "reps": "8-10", "img": "https://images.pexels.com/photos/3837781/pexels-photo-3837781.jpeg"},
            {"name": "Push-ups", "sets": 3, "reps": "12-15", "img": "https://images.pexels.com/photos/176782/pexels-photo-176782.jpeg"},
            {"name": "Incline Dumbbell Press", "sets": 3, "reps": "10-12", "img": "https://images.pexels.com/photos/7187890/pexels-photo-7187890.jpeg"}
        ],
        "Back": [
            {"name": "Pull-ups", "sets": 3, "reps": "6-10", "img": "https://i0.wp.com/post.healthline.com/wp-content/uploads/2019/12/pull-up-pullup-gym-1296x728-header-1296x728.jpg?w=1155&h=1528"},
            {"name": "Lat Pulldown", "sets": 3, "reps": "10-12", "img": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Lat-Pulldown.gif"},
        ],
        "Shoulders": [
            {"name": "Overhead Press", "sets": 3, "reps": "10-12", "img": "https://weighttraining.guide/wp-content/uploads/2016/05/Dumbbell-Shoulder-Press-resized.png"},
            {"name": "Lateral Raises", "sets": 3, "reps": "12-15", "img": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Dumbbell-Lateral-Raise.gif"}
        ],
        "Arms": [
            {"name": "Bicep Curls", "sets": 3, "reps": "10-12", "img": "https://images.pexels.com/photos/1229356/pexels-photo-1229356.jpeg"},
            {"name": "Tricep Dips", "sets": 3, "reps": "10-12", "img": "https://liftmanual.com/wp-content/uploads/2023/04/dumbbell-standing-triceps-extension.jpg"}
        ],
        "Legs": [
            {"name": "Squats", "sets": 4, "reps": "8-10", "img": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Jump-Squat.gif"},
            {"name": "Leg Press", "sets": 3, "reps": "10-12", "img": "https://fitnessprogramer.com/wp-content/uploads/2015/11/Leg-Press.gif"},
            {"name": "Lunges", "sets": 3, "reps": "12-15", "img": "https://media.post.rvohealth.io/wp-content/uploads/2023/08/AltruisticFantasticCub-size_restricted-1.gif"}
        ]
    },
    "beginner": {
        "Full Body": [
            {"name": "Bodyweight Squats", "sets": 3, "reps": "12-15", "img": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Jump-Squat.gif"},
            {"name": "Push-ups", "sets": 3, "reps": "8-12", "img": "https://images.pexels.com/photos/176782/pexels-photo-176782.jpeg"}
        ],
        "Cardio": [
            {"name": "Treadmill", "duration": "20 min", "img": "https://images.pexels.com/photos/1954524/pexels-photo-1954524.jpeg"},
            {"name": "Cycling", "duration": "15 min", "img": "https://fitnessprogramer.com/wp-content/uploads/2021/06/Bike.gif"}
        ],
        "Lower Body": [
            {"name": "Glute Bridges", "sets": 3, "reps": "12-15", "img": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Glute-Bridge-.gif"},
            {"name": "Lunges", "sets": 3, "reps": "10-12", "img": "https://media.post.rvohealth.io/wp-content/uploads/2023/08/AltruisticFantasticCub-size_restricted-1.gif"},
            {"name": "Leg Press", "sets": 3, "reps": "10-12", "img": "https://fitnessprogramer.com/wp-content/uploads/2015/11/Leg-Press.gif"}
        ],
        "Core": [
            {"name": "Plank", "duration": "30-60 sec", "img": "https://www.inspireusafoundation.org/file/2022/11/body-saw-plank.gif"},
            {"name": "Crunches", "sets": 3, "reps": "15-20", "img": "https://fitnessprogramer.com/wp-content/uploads/2022/07/Cross-Crunch.gif"},
            {"name": "Russian Twists", "sets": 3, "reps": "20", "img": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Russian-Twist.gif"}
        ],
        "Arms": [
            {"name": "Resistance Band Curls", "sets": 3, "reps": "12-15", "img": "https://fitnessprogramer.com/wp-content/uploads/2022/02/Band-Biceps-Curl.gif"},
            {"name": "Tricep Kickbacks", "sets": 3, "reps": "12-15", "img": "https://media.tenor.com/PZjMZqyfPgcAAAAM/db-tricep-kickback.gif"}
        ]
    }
}

# ---------------- Gym Workouts ----------------
def display_gym_workouts(gender):
    st.subheader("Gym Workouts")

    # Default to advanced for Male, beginner for Female, but allow switching
    default_idx = 0 if gender == "Female" else 1
    level = st.radio("Select Level", ["beginner", "advanced"], index=default_idx, format_func=lambda x: x.capitalize(), horizontal=True)
    
    workouts = WORKOUT_DB[level]

    for muscle, exercises in workouts.items():
        with st.expander(muscle):
            for ex in exercises:
                col1, col2 = st.columns([1, 3])
                with col1:
                    st.image(ex["img"], use_column_width=True)
                with col2:
                    st.write(f"**{ex['name']}**")
                    if "duration" in ex:
                        st.write(f"Duration: {ex['duration']}")
                    else:
                        st.write(f"{ex['sets']} sets x {ex['reps']} reps")
                st.divider()

# ---------------- Yoga Workouts ----------------
def display_yoga_asanas(gender):
    st.subheader("Yoga Asanas")

    if gender == "Male":
        asanas = [
            {"name": "Surya Namaskar", "img": "https://i.pinimg.com/736x/77/1a/d0/771ad07e2bff1a844011657366b97bdd.jpg"},
            {"name": "Bhujangasana (Cobra Pose)", "img": "https://media.istockphoto.com/id/924163406/photo/young-woman-doing-cobra-exercise.jpg?s=612x612&w=0&k=20&c=h9nNF3H0eYGIZMTTPy1aGuU8_grk0Hc_caQEU93CU2Y="},
            {"name": "Trikonasana (Triangle Pose)", "img": "https://media.istockphoto.com/id/636608240/photo/utthita-trikonasana-extended-triangle-pose.jpg?s=612x612&w=0&k=20&c=F8F8TMH1sB2YbQst13-5SqqocAkyDN3cMJJsjIaVnMs="},
            {"name": "Vrikshasana (Tree Pose)", "img": "https://media.istockphoto.com/id/667293728/photo/young-yogi-attractive-woman-in-vrksasana-pose-white-loft-background.jpg?s=612x612&w=0&k=20&c=4gRlwc21131Q_SKrj3evMNERTL_kiLWgcEA_Z6Eucco="},
            {"name": "Adho Mukha Svanasana", "img": "https://media.istockphoto.com/id/1152625738/photo/woman-practicing-yoga-downward-facing-dog-adho-mukha-svanasana.jpg?s=612x612&w=0&k=20&c=s2NN_rAFN3ImQrWayCP7WYySo5O8Q5zs8trmBQuUlk4="}
        ]
    else:
        asanas = [
            {"name": "Surya Namaskar", "img": "https://i.pinimg.com/736x/77/1a/d0/771ad07e2bff1a844011657366b97bdd.jpg"},
            {"name": "Utkatasana (Chair Pose)", "img": "https://media.istockphoto.com/id/639103576/photo/chair-pose.jpg?s=612x612&w=0&k=20&c=J1EZ71EYaZgmVxnfa0ZpziCPSnBBsRtiK2dvpXCQxvY="},
            {"name": "Setu Bandhasana (Bridge Pose)", "img": "https://media.istockphoto.com/id/607482492/photo/beautiful-sporty-fit-yogi-girl-practices-yoga-asana-setu-bandhas.jpg?s=612x612&w=0&k=20&c=8_Lz_YnL5rN4659ht0PKjJfGU7iMXvRt4b9rizz66Lk="},
            {"name": "Balasana (Child’s Pose)", "img": "https://media.istockphoto.com/id/542715024/photo/pregnant-young-woman-doing-prenatal-child-yoga-pose-balasana.jpg?s=612x612&w=0&k=20&c=-UI9AuOGvipPNPHTdUjmZyUINw9tq5Kid8CCGe_klHw="},
            {"name": "Baddha Konasana (Butterfly Pose)", "img": "https://media.istockphoto.com/id/579760132/photo/sporty-fit-woman-practices-yoga-asana-baddha-konasana-outdoors.jpg?s=612x612&w=0&k=20&c=RtO8sS8lqszUXvZA4it-lVRjOa6ivS6A6pdnSg1JXQU="}
        ]

    for pose in asanas:
        with st.expander(pose["name"]):
            col1, col2 = st.columns([1, 2])
            with col1:
                st.image(pose["img"], use_column_width=True)
            with col2:
                st.write(f"**{pose['name']}**")
                st.write(f"✔ Recommended for {gender}")
                st.write("Focus on proper form and breathing for maximum benefit.")

# ---------------- Countdown Timer ----------------
def display_countdown_timer():
    st.subheader("Workout Countdown Timer")

    # Initialize session state variables
    if 'timer_running' not in st.session_state:
        st.session_state.timer_running = False
    if 'countdown_seconds' not in st.session_state:
        st.session_state.countdown_seconds = 60
    if 'end_time' not in st.session_state:
        st.session_state.end_time = 0
    if 'timer_finished' not in st.session_state:
        st.session_state.timer_finished = False

    # Display the success message and balloons when the timer finishes
    if st.session_state.timer_finished:
        st.success("🎉 Time's up!")
        st.balloons()
        st.session_state.timer_finished = False  # Reset for the next run

    # Input for setting the timer duration
    seconds = st.number_input(
        "Set timer (seconds):",
        min_value=1,
        value=st.session_state.countdown_seconds,
        disabled=st.session_state.timer_running
    )
    if not st.session_state.timer_running:
        st.session_state.countdown_seconds = seconds

    def start_timer():
        st.session_state.timer_running = True
        st.session_state.end_time = time.time() + st.session_state.countdown_seconds
        st.session_state.timer_finished = False

    def stop_timer():
        st.session_state.timer_running = False

    col1, col2 = st.columns(2)
    with col1:
        st.button("Start Timer", on_click=start_timer, disabled=st.session_state.timer_running)
    with col2:
        st.button("Stop Timer", on_click=stop_timer, disabled=not st.session_state.timer_running)

    timer_placeholder = st.empty()

    if st.session_state.timer_running:
        remaining_time = st.session_state.end_time - time.time()
        if remaining_time > 0:
            mins, secs = divmod(remaining_time, 60)
            timer_placeholder.metric("⏳ Time Remaining", f"{int(mins):02d}:{int(secs):02d}")
            time.sleep(1)
            st.rerun()
        else:
            st.session_state.timer_running = False
            st.session_state.timer_finished = True
            st.rerun()
    elif not st.session_state.timer_finished:
        mins, secs = divmod(st.session_state.countdown_seconds, 60)
        timer_placeholder.metric("⏳ Time Remaining", f"{int(mins):02d}:{int(secs):02d}")

# ---------------- New Features ----------------
def calculate_calories(weight, height, age, gender, activity_level):
    # Mifflin-St Jeor Equation
    if gender == "Male":
        bmr = (10 * weight) + (6.25 * height) - (5 * age) + 5
    else:
        bmr = (10 * weight) + (6.25 * height) - (5 * age) - 161
    
    multipliers = {
        "Sedentary (little or no exercise)": 1.2,
        "Lightly active (1-3 days/week)": 1.375,
        "Moderately active (3-5 days/week)": 1.55,
        "Very active (6-7 days/week)": 1.725,
        "Super active (physical job)": 1.9
    }
    return int(bmr * multipliers[activity_level])

def get_ai_response(prompt):
    # Simple rule-based AI response simulation
    prompt = prompt.lower()
    if "weight" in prompt:
        return "To manage weight, focus on a caloric deficit for loss or surplus for gain, combined with consistent strength training."
    elif "muscle" in prompt:
        return "Building muscle requires progressive overload in your workouts and sufficient protein intake (1.6g-2.2g per kg of bodyweight)."
    elif "diet" in prompt or "food" in prompt:
        return "A balanced diet should include lean proteins, healthy fats, and complex carbohydrates. Avoid processed sugars."
    elif "pain" in prompt or "hurt" in prompt:
        return "If you're experiencing pain, please stop exercising immediately and consult a medical professional. Rest is crucial."
    elif "hello" in prompt or "hi" in prompt:
        return "Hello! I'm your AI Fitness Coach. How can I help you reach your goals today?"
    else:
        return "That's a great question. Consistency is key! Focus on your daily habits, stay hydrated, and get enough sleep."

def create_pdf(user_data, bmi, category, advice):
    if FPDF is None:
        return None
    
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt="Fitness Advisor - Health Report", ln=1, align='C')
    pdf.ln(10)
    
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"Date: {datetime.date.today()}", ln=1)
    pdf.cell(200, 10, txt=f"Name: {user_data['name']}", ln=1)
    pdf.cell(200, 10, txt=f"Age: {user_data['age']} | Gender: {user_data['gender']}", ln=1)
    pdf.cell(200, 10, txt=f"Height: {user_data['height']} cm | Weight: {user_data['weight']} kg", ln=1)
    pdf.ln(10)
    
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(200, 10, txt=f"BMI: {bmi:.2f} ({category})", ln=1)
    pdf.ln(5)
    
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, txt=f"Workout Focus: {advice}")
    pdf.ln(5)
    pdf.multi_cell(0, 10, txt="Remember to stay hydrated and maintain a balanced diet!")
    
    return pdf.output(dest='S').encode('latin-1')

def check_badges(streak, bmi_history):
    badges = []
    if streak >= 5:
        badges.append("🔥 5 Day Streak")
    if len(bmi_history) > 1 and bmi_history[-1]['bmi'] < bmi_history[0]['bmi']:
        badges.append("🎯 BMI Improved")
    if len(bmi_history) >= 1:
        badges.append("🏆 First Step Taken")
    return badges

# ---------------- Main App ----------------
st.set_page_config(page_title="Fitness Advisor", page_icon="🏋️")
add_bg_from_url()

st.title("Welcome to Fitness Advisor")

# ---------------- Sidebar ----------------
with st.sidebar:
    st.header("Enter Your Details")

    # Load saved data if exists
    default_data = {
        "name": "", "age": 25, "gender": "Male", 
        "height": 170.0, "weight": 60.0, 
        "history": [], "streak": 0, "last_visit": "",
        "schedule": {"Monday": "", "Tuesday": "", "Wednesday": "", "Thursday": "", "Friday": "", "Saturday": "", "Sunday": ""}
    }
    
    if os.path.exists("user_data.json"):
        try:
            with open("user_data.json", "r") as f:
                default_data.update(json.load(f))
        except Exception as e:
            st.error(f"Error loading data: {e}")

    name = st.text_input("Name", value=default_data["name"])
    age = st.number_input("Age", min_value=1, max_value=120, value=int(default_data["age"]))
    gender_index = 0 if default_data["gender"] == "Male" else 1
    gender = st.radio("Gender", ["Male", "Female"], index=gender_index, horizontal=True)
    height_cm = st.number_input("Height (cm)", min_value=1.0, value=float(default_data["height"]))
    weight = st.number_input("Weight (kg)", min_value=1.0, value=float(default_data["weight"]))

    # Streak Logic
    today_str = datetime.date.today().isoformat()
    if default_data["last_visit"] != today_str:
        if default_data["last_visit"] == (datetime.date.today() - datetime.timedelta(days=1)).isoformat():
            default_data["streak"] += 1
        elif default_data["last_visit"] < today_str: # Reset if missed a day, but not if same day
             # Only reset if the gap is more than 1 day. 
             # If last visit was yesterday, streak++ (handled above).
             # If last visit was today, do nothing.
             # If last visit was before yesterday, reset to 1.
             last_visit_date = datetime.date.fromisoformat(default_data["last_visit"]) if default_data["last_visit"] else datetime.date.min
             if (datetime.date.today() - last_visit_date).days > 1:
                 default_data["streak"] = 1
             elif default_data["streak"] == 0:
                 default_data["streak"] = 1
        default_data["last_visit"] = today_str

    if st.button("Save Profile"):
        new_history_entry = {"date": today_str, "weight": weight, "bmi": calculate_bmi(weight, height_cm)}
        # Append only if today's date isn't already the last entry, or update it
        if not default_data["history"] or default_data["history"][-1]["date"] != today_str:
            default_data["history"].append(new_history_entry)
        else:
            default_data["history"][-1] = new_history_entry

        user_data = {
            "name": name, "age": age, "gender": gender, "height": height_cm, "weight": weight,
            "history": default_data["history"], "streak": default_data["streak"], "last_visit": today_str,
            "schedule": default_data.get("schedule", {})
        }
        with open("user_data.json", "w") as f:
            json.dump(user_data, f)
        st.success("Profile saved!")

# ---------------- Main Content ----------------
if name and height_cm > 0 and weight > 0:
    bmi = calculate_bmi(weight, height_cm)
    category = bmi_category(bmi)
    
    # Create Tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Dashboard", "🏋️ Workouts", "🥗 Diet", "🤖 AI Coach"])

    # --- TAB 1: DASHBOARD ---
    with tab1:
        st.header(f"Hello, {name}!")
        
        # Badges
        badges = check_badges(default_data["streak"], default_data["history"])
        if badges:
            st.write("### Achievements")
            st.write(" ".join([f"`{b}`" for b in badges]))
        
        col1, col2, col3 = st.columns(3)
        col1.metric("BMI", f"{bmi:.2f}", category)
        col2.metric("Current Weight", f"{weight} kg")
        col3.metric("Streak", f"{default_data['streak']} Days")

        # Progress Graph
        st.subheader("Weight Progress")
        if default_data["history"]:
            df = pd.DataFrame(default_data["history"])
            st.line_chart(df.set_index("date")["weight"])
        else:
            st.info("Save your profile to start tracking progress!")

        # Water Reminder / Tracker
        st.subheader("💧 Water Tracker")
        if "water_count" not in st.session_state:
            st.session_state.water_count = 0
        
        w_col1, w_col2 = st.columns([1, 3])
        with w_col1:
            if st.button("Drink Water 🥤"):
                st.session_state.water_count += 1
        with w_col2:
            st.write(f"**Glasses today:** {st.session_state.water_count} / 8")
            st.progress(min(st.session_state.water_count / 8, 1.0))

        # PDF Download
        st.divider()
        if FPDF:
            pdf_bytes = create_pdf(default_data, bmi, category, "Focus on consistency!")
            if pdf_bytes:
                st.download_button(
                    label="📄 Download Health Report (PDF)",
                    data=pdf_bytes,
                    file_name="health_report.pdf",
                    mime="application/pdf"
                )
        else:
            st.warning("Install 'fpdf' to enable PDF downloads: `pip install fpdf`")

    # --- TAB 2: WORKOUTS ---
    with tab2:
        st.header("Workout Recommendations")
        display_gender_workout_tips(gender)
        
        # Workout Scheduler
        with st.expander("📅 Weekly Workout Scheduler"):
            schedule = default_data.get("schedule", {})
            days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
            cols = st.columns(2)
            updated_schedule = {}
            for i, day in enumerate(days):
                with cols[i % 2]:
                    updated_schedule[day] = st.text_input(day, value=schedule.get(day, ""))
            
            if st.button("Save Schedule"):
                default_data["schedule"] = updated_schedule
                # Save to file logic repeated for simplicity or create a helper
                with open("user_data.json", "w") as f:
                    # Merge with existing data to not lose other fields
                    full_data = default_data.copy()
                    full_data["schedule"] = updated_schedule
                    json.dump(full_data, f)
                st.success("Schedule Updated!")

        display_countdown_timer()
        st.divider()

        workout_choice = st.radio("Choose workout type:", ["Gym", "Yoga"], horizontal=True)
        if workout_choice == "Gym":
            display_gym_workouts(gender)
        else:
            display_yoga_asanas(gender)

    # --- TAB 3: DIET ---
    with tab3:
        st.header("Diet & Nutrition")
        
        # Calorie Calculator
        with st.expander("🔥 Daily Calorie Calculator"):
            activity = st.selectbox("Activity Level", [
                "Sedentary (little or no exercise)",
                "Lightly active (1-3 days/week)",
                "Moderately active (3-5 days/week)",
                "Very active (6-7 days/week)",
                "Super active (physical job)"
            ])
            daily_cals = calculate_calories(weight, height_cm, age, gender, activity)
            st.info(f"Your estimated daily maintenance calories: **{daily_cals} kcal**")

        # Meal Reminders (Static for now)
        st.subheader("⏰ Meal Reminders")
        st.caption("Suggested timings for your meals:")
        st.write("🍳 **Breakfast:** 8:00 AM")
        st.write("🥗 **Lunch:** 1:00 PM")
        st.write("🍎 **Snack:** 4:30 PM")
        st.write("🍲 **Dinner:** 8:00 PM")
        st.divider()

        diet_view = st.radio("Choose diet plan type:", ["Daily (BMI Based)", "Weekly"], horizontal=True)
        diet_choice = st.radio("Choose diet type:", ["Vegetarian", "Non-Vegetarian"], horizontal=True)

        if diet_view == "Daily (BMI Based)":
            display_diet_plan(diet_choice, category, gender)
        else:
            display_weekly_diet_plan(diet_choice)

    # --- TAB 4: AI COACH ---
    with tab4:
        st.header("🤖 AI Fitness Coach")
        
        st.write("Ask me anything about workouts, diet, or motivation!")
        
        # Chat Interface
        if "messages" not in st.session_state:
            st.session_state.messages = [{"role": "assistant", "content": "Hello! How can I help you get fit today?"}]

        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.write(msg["content"])

        if prompt := st.chat_input("Type your question here..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.write(prompt)
            
            response = get_ai_response(prompt)
            st.session_state.messages.append({"role": "assistant", "content": response})
            with st.chat_message("assistant"):
                st.write(response)

else:
    st.info("👉 Please fill all details in the sidebar.")
