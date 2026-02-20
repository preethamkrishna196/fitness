import streamlit as st
import time
import json
import os
import datetime
import pandas as pd
import random
import hashlib
import subprocess
import sys
import re
import plotly.graph_objects as go

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
        /* Custom button styles */
        div[data-testid="stButton"] > button {
            background-color: #ff0000;
            color: white;
            border-color: #ff0000;
        }
        div[data-testid="stButton"] > button:hover {
            background-color: #cc0000;
            border-color: #cc0000;
            color: white;
        }
        div[data-testid="stButton"] > button:disabled {
            background-color: #ff0000;
            border-color: #ff0000;
            color: white;
            opacity: 0.65;
        }
        /* Animation */
        @keyframes pulse {
            0% { transform: scale(1); }
            50% { transform: scale(1.2); }
            100% { transform: scale(1); }
        }
        .fitness-animate {
            animation: pulse 2s infinite;
            font-size: 80px;
            text-align: center;
            display: block;
            margin-bottom: 20px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

# ---------------- Diet Section (Daily BMI Based) ----------------
def display_diet_plan(diet_type, bmi_cat, gender, restrictions):
    st.subheader(f"{diet_type} Daily Diet Plan")

    gender_note = "Higher calorie needs" if gender == "Male" else "Moderate calorie needs"
    st.caption(f"👤 {gender} • {bmi_cat} • {gender_note}")

    # Display selected restrictions
    if restrictions:
        st.info(f"Applying restrictions: **{', '.join(restrictions)}**")

    plans = {}
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
    elif diet_type == "Vegan":
        plans = {
            "Underweight": {
                "Breakfast": "Tofu Scramble + Avocado Toast",
                "Lunch": "Lentil Soup + Brown Rice",
                "Dinner": "Quinoa Bowl + Roasted Veggies",
                "Total": "≈1850 kcal | 80g protein"
            },
            "Normal weight": {
                "Breakfast": "Oatmeal + Berries + Seeds",
                "Lunch": "Chickpea Salad Sandwich",
                "Dinner": "Black Bean Burgers",
                "Total": "≈1550 kcal | 75g protein"
            },
            "Overweight": {
                "Breakfast": "Berry Smoothie + Protein Powder",
                "Lunch": "Large Salad + Beans & Seeds",
                "Dinner": "Vegetable Stir-fry + Tofu",
                "Total": "≈1250 kcal | 70g protein"
            },
            "Obese": {
                "Breakfast": "Fruit Bowl + Flax Seeds",
                "Lunch": "Miso Soup + Edamame",
                "Dinner": "Steamed Vegetables + Hummus",
                "Total": "≈1000 kcal | 60g protein"
            }
        }
    elif diet_type == "Keto":
        plans = {
            "Underweight": {"Breakfast": "Bacon, Eggs, Avocado", "Lunch": "Steak Salad", "Dinner": "Salmon + Asparagus", "Total": "≈2000 kcal | 120g protein"},
            "Normal weight": {"Breakfast": "Cheese Omelette", "Lunch": "Chicken Breast + Broccoli", "Dinner": "Tuna Salad", "Total": "≈1600 kcal | 100g protein"},
            "Overweight": {"Breakfast": "Scrambled Eggs", "Lunch": "Grilled Chicken Strips", "Dinner": "Zucchini Noodles + Pesto", "Total": "≈1300 kcal | 90g protein"},
            "Obese": {"Breakfast": "Avocado with Salt & Pepper", "Lunch": "Lettuce Wraps + Ground Turkey", "Dinner": "Bone Broth", "Total": "≈1100 kcal | 80g protein"}
        }
    else: # Standard (Non-Vegetarian)
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

    if bmi_cat in plans:
        with st.expander("View Daily Diet Plan"):
            for meal, value in plans[bmi_cat].items():
                st.write(f"**{meal}:** {value}")
    else:
        st.warning("No specific plan available for this combination. Please consult a nutritionist.")

    # Add warnings for restrictions
    if "Gluten-Free" in restrictions:
        st.warning("**Gluten-Free Note:** Please ensure ingredients like oats, bread, and grains are certified gluten-free. Substitute with alternatives like quinoa, rice, or gluten-free bread where necessary.")
    if "Dairy-Free" in restrictions:
        st.warning("**Dairy-Free Note:** Replace milk, cheese, and curd with dairy-free alternatives like almond milk, soy paneer (tofu), or coconut yogurt.")
    if "Nut-Free" in restrictions:
        st.warning("**Nut-Free Note:** Avoid nuts and seeds in meal suggestions. Be cautious of hidden nuts in sauces and dressings.")

# ---------------- Weekly Diet Plan ----------------
def display_weekly_diet_plan(diet_type, restrictions):
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

    # Add more diet types to weekly plan (example for Monday)
    weekly_plan["Monday"]["Vegan"] = ["Tofu Scramble", "Lentil Soup + Rice", "Quinoa Bowl"]
    weekly_plan["Monday"]["Keto"] = ["Eggs & Avocado", "Chicken Salad", "Steak & Asparagus"]
    # In a real app, you'd fill this out for all days

    for day, meals in weekly_plan.items():
        with st.expander(day):
            key = "Non-Veg" # Default to Standard/Non-Veg
            if diet_type == "Vegetarian":
                key = "Veg"
            elif diet_type == "Vegan":
                key = "Vegan"
            elif diet_type == "Keto":
                key = "Keto"

            if key not in meals:
                st.warning(f"No weekly plan available for {diet_type} on {day}. Showing Non-Veg plan as a placeholder.")
                key = "Non-Veg"

            selected_meals = meals[key]
            st.write(f"**Breakfast:** {selected_meals[0]}")
            st.write(f"**Lunch:** {selected_meals[1]}")
            st.write(f"**Dinner:** {selected_meals[2]}")
    
    if restrictions:
        st.info(f"Remember to adapt the weekly plan according to your restrictions: **{', '.join(restrictions)}**.")

# ---------------- Workout Tips ----------------
def display_goal_workout_tips(goal):
    st.subheader("Tips for Your Goal")
    tips = {
        "Weight Loss": "Incorporate more cardiovascular exercise like running, cycling, or HIIT. Combine with full-body strength training to preserve muscle mass.",
        "Muscle Gain": "Focus on progressive overload in your strength training. Ensure you're lifting heavy enough and getting adequate protein. Compound lifts like squats, deadlifts, and bench press are key.",
        "Endurance Training": "Gradually increase the duration and intensity of your cardio sessions. Mix in long, slow distance training with some higher-intensity interval work.",
        "General Health": "Aim for a balanced routine including 150 minutes of moderate cardio and 2 strength training sessions per week. Don't forget flexibility and mobility work like yoga or stretching."
    }
    st.info(tips.get(goal, "Select a goal to see personalized tips."))

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
def adjust_calories_for_goal(tdee, goal):
    adjustments = {
        "Weight Loss": -500,
        "Muscle Gain": 300,
        "Endurance Training": 0,
        "General Health": 0
    }
    adjustment = adjustments.get(goal, 0)
    return tdee + adjustment, adjustment

def calculate_calories(weight, height, age, gender, activity_level):
    # Mifflin-St Jeor Equation
    if gender == "Male":
        bmr = (10 * weight) + (6.25 * height) - (5 * age) + 5
    else:
        bmr = (10 * weight) + (6.25 * height) - (5 * age) - 161
    
    multipliers = {
        "Sedentary": 1.2,
        "Lightly Active": 1.375,
        "Moderately Active": 1.55,
        "Very Active": 1.725
    }
    return int(bmr * multipliers[activity_level])

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
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = ""

def make_hashes(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

def check_hashes(password, hashed_text):
    if make_hashes(password) == hashed_text:
        return True
    return False

def login_page():
    st.markdown('<div class="fitness-animate">🏋️</div>', unsafe_allow_html=True)
    st.title("Fitness Advisor Login")
    
    tab1, tab2 = st.tabs(["Login", "Sign Up"])
    
    with tab1:
        username = st.text_input("Username")
        password = st.text_input("Password", type='password')
        if st.button("Login"):
            if not os.path.exists("users.json"):
                st.error("No users found. Please sign up.")
            else:
                with open("users.json", "r") as f:
                    users = json.load(f)
                if username in users and check_hashes(password, users[username]):
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.success("Logged in!")
                    st.rerun()
                else:
                    st.error("Incorrect Username or Password")

    with tab2:
        new_user = st.text_input("New Username")
        new_password = st.text_input("New Password", type='password')
        if st.button("Sign Up"):
            if not os.path.exists("users.json"):
                with open("users.json", "w") as f:
                    json.dump({}, f)
            with open("users.json", "r") as f:
                users = json.load(f)
            if new_user in users:
                st.error("Username already exists.")
            else:
                users[new_user] = make_hashes(new_password)
                with open("users.json", "w") as f:
                    json.dump(users, f)
                st.success("Account created! Please login.")

if not st.session_state.logged_in:
    login_page()
    st.stop()

add_bg_from_url()

USER_DATA_FILE = f"user_data_{st.session_state.username}.json"

st.title("Welcome to Fitness Advisor")

# ---------------- Sidebar ----------------
with st.sidebar:
    st.write(f"Logged in as: **{st.session_state.username}**")
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.rerun()
    st.divider()

    st.header("Enter Your Details")

    # Load saved data if exists
    default_data = {
        "name": "", "age": 25, "gender": "Male", 
        "height": 170.0, "weight": 60.0, "goal": "General Health",
        "history": [], "streak": 0, "last_visit": "",
        "schedule": {"Monday": "", "Tuesday": "", "Wednesday": "", "Thursday": "", "Friday": "", "Saturday": "", "Sunday": ""}
    }
    
    if os.path.exists(USER_DATA_FILE):
        try:
            with open(USER_DATA_FILE, "r") as f:
                default_data.update(json.load(f))
        except Exception as e:
            st.error(f"Error loading data: {e}")

    name = st.text_input("Name", value=default_data["name"])
    if name and not re.match(r"^[A-Za-z ]+$", name):
        st.error("Name must contain only letters and spaces. No numbers or symbols allowed.")
        name = ""
    age = st.number_input("Age", min_value=1, max_value=120, value=int(default_data["age"]))
    gender_index = 0 if default_data["gender"] == "Male" else 1
    gender = st.radio("Gender", ["Male", "Female"], index=gender_index, horizontal=True)

    goal_options = ["Weight Loss", "Muscle Gain", "Endurance Training", "General Health"]
    goal_index = goal_options.index(default_data.get("goal", "General Health"))
    goal = st.selectbox("Your Fitness Goal", goal_options, index=goal_index)

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
            "name": name, "age": age, "gender": gender, "height": height_cm, "weight": weight, "goal": goal,
            "history": default_data["history"], "streak": default_data["streak"], "last_visit": today_str,
            "schedule": default_data.get("schedule", {})
        }
        with open(USER_DATA_FILE, "w") as f:
            json.dump(user_data, f)
        st.success("Profile saved!")

# ---------------- Main Content ----------------
if name and height_cm > 0 and weight > 0:
    bmi = calculate_bmi(weight, height_cm)
    category = bmi_category(bmi)
    
    # Create Tabs
    tab1, tab2, tab3 = st.tabs(["📊 Dashboard", "🏋️ Workouts", "🥗 Diet"])

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

        # BMI Gauge Chart
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=bmi,
            title={'text': f"BMI Category: {category}"},
            gauge={
                'axis': {'range': [10, 50]},
                'bar': {'color': "darkblue"},
                'steps': [
                    {'range': [10, 18.5], 'color': "lightblue"},
                    {'range': [18.5, 24.9], 'color': "lightgreen"},
                    {'range': [24.9, 29.9], 'color': "orange"},
                    {'range': [29.9, 50], 'color': "red"}
                ],
            }
        ))
        st.plotly_chart(fig, use_container_width=True)
        st.caption("🔵 Underweight | 🟢 Normal | 🟠 Overweight | 🔴 Obese")

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

    # --- TAB 2: WORKOUTS ---
    with tab2:
        st.header("Workout Recommendations")
        display_goal_workout_tips(goal)
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
                with open(USER_DATA_FILE, "w") as f:
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
                "Sedentary",
                "Lightly Active",
                "Moderately Active",
                "Very Active"
            ])
            tdee = calculate_calories(weight, height_cm, age, gender, activity)
            st.info(f"Your estimated daily maintenance calories (TDEE): **{tdee} kcal**")

            goal_calories, adjustment = adjust_calories_for_goal(tdee, goal)

            if adjustment > 0:
                st.success(f"For your goal of **{goal}**, you should aim for a caloric surplus. We suggest adding **{adjustment} kcal**.")
            elif adjustment < 0:
                st.warning(f"For your goal of **{goal}**, you should aim for a caloric deficit. We suggest subtracting **{-adjustment} kcal**.")
            
            st.metric(label=f"Your Daily Goal for {goal}", value=f"{goal_calories} kcal")

        # Meal Reminders (Static for now)
        st.subheader("⏰ Meal Reminders")
        st.caption("Suggested timings for your meals:")
        st.write("🍳 **Breakfast:** 8:00 AM")
        st.write("🥗 **Lunch:** 1:00 PM")
        st.write("🍎 **Snack:** 4:30 PM")
        st.write("🍲 **Dinner:** 8:00 PM")
        st.divider()

        st.subheader("🍽️ Your Diet Plan")
        c1, c2 = st.columns(2)
        with c1:
            diet_preference = st.selectbox(
                "Primary Diet Style",
                ["Standard (Non-Vegetarian)", "Vegetarian", "Vegan", "Keto"]
            )
        with c2:
            dietary_restrictions = st.multiselect(
                "Additional Restrictions",
                ["Gluten-Free", "Dairy-Free", "Nut-Free"],
                help="Select any dietary restrictions you have. The plans will be adjusted with notes."
            )

        diet_view = st.radio("Choose plan format:", ["Daily (BMI Based)", "Weekly"], horizontal=True)

        if diet_view == "Daily (BMI Based)":
            display_diet_plan(diet_preference, category, gender, dietary_restrictions)
        else:
            display_weekly_diet_plan(diet_preference, dietary_restrictions)

else:
    st.info("👉 Please fill all details in the sidebar.")
