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
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import difflib
from openai import OpenAI

# ---------------- Configuration ----------------
SYSTEM_EMAIL = "your_app_email@gmail.com"  # Replace with the sender email
SYSTEM_PASSWORD = "your_app_password"      # Replace with the sender app password
OPENAI_API_KEY = "your_openai_api_key"     # Replace with your OpenAI API key

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
        /* Light blue button */
        .light-blue-button div[data-testid="stButton"] > button,
        .light-blue-button div[data-testid="stDownloadButton"] > button,
        .light-blue-button div[data-testid="stFormSubmitButton"] > button {
            background-color: #3498db !important;
            border-color: #3498db !important;
        }
        .light-blue-button div[data-testid="stButton"] > button:hover,
        .light-blue-button div[data-testid="stDownloadButton"] > button:hover,
        .light-blue-button div[data-testid="stFormSubmitButton"] > button:hover {
            background-color: #2980b9 !important; /* A darker shade for hover */
            border-color: #2980b9 !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

def send_email_notification(sender_email, sender_password, receiver_email, subject, body):
    try:
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, receiver_email, msg.as_string())
        return True, "Email sent successfully!"
    except Exception as e:
        return False, f"Error sending email: {e}"

# ---------------- Diet Section (Daily BMI Based) ----------------
def display_diet_plan(diet_type, bmi_cat, gender, restrictions):
    st.subheader(f"{diet_type} Daily Diet Plan")

    gender_note = "Higher calorie needs" if gender == "Male" else "Moderate calorie needs"
    st.caption(f"👤 {gender} • {bmi_cat} • {gender_note}")

    # Display selected restrictions
    if restrictions:
        st.info(f"Applying restrictions: **{', '.join(restrictions)}**")

    plans = {}
    if diet_type == "Veg":
        plans = {
            "Underweight": {
                "Breakfast": "Oats + Milk + Banana",
                "Lunch": "Rice + Dal + Paneer",
                "Dinner": "Roti + Chickpeas",
                "Snacks": "Fruit Smoothie + Nuts",
                "Total": "≈1800 kcal | 90g protein"
            },
            "Normal weight": {
                "Breakfast": "Paneer Sandwich + Milk",
                "Lunch": "Dal + Rice",
                "Dinner": "Roti + Soybean",
                "Snacks": "Roasted Chana / Corn",
                "Total": "≈1500 kcal | 85g protein"
            },
            "Overweight": {
                "Breakfast": "Sprouts + Green Tea",
                "Lunch": "Dal + Salad",
                "Dinner": "Veg Soup + Paneer",
                "Snacks": "Cucumber/Carrot Sticks",
                "Total": "≈1200 kcal | 80g protein"
            },
            "Obese": {
                "Breakfast": "Fruit Bowl",
                "Lunch": "Mixed Veg + Dal",
                "Dinner": "Soup + Salad",
                "Snacks": "Green Tea + 2 Almonds",
                "Total": "≈1050 kcal | 70g protein"
            }
        }
    elif diet_type == "Vegan":
        plans = {
            "Underweight": {
                "Breakfast": "Tofu Scramble + Avocado Toast",
                "Lunch": "Lentil Soup + Brown Rice",
                "Dinner": "Quinoa Bowl + Roasted Veggies",
                "Snacks": "Peanut Butter Toast",
                "Total": "≈1850 kcal | 80g protein"
            },
            "Normal weight": {
                "Breakfast": "Oatmeal + Berries + Seeds",
                "Lunch": "Chickpea Salad Sandwich",
                "Dinner": "Black Bean Burgers",
                "Snacks": "Mixed Seeds + Fruit",
                "Total": "≈1550 kcal | 75g protein"
            },
            "Overweight": {
                "Breakfast": "Berry Smoothie + Protein Powder",
                "Lunch": "Large Salad + Beans & Seeds",
                "Dinner": "Vegetable Stir-fry + Tofu",
                "Snacks": "Apple Slices",
                "Total": "≈1250 kcal | 70g protein"
            },
            "Obese": {
                "Breakfast": "Fruit Bowl + Flax Seeds",
                "Lunch": "Miso Soup + Edamame",
                "Dinner": "Steamed Vegetables + Hummus",
                "Snacks": "Cucumber Slices",
                "Total": "≈1000 kcal | 60g protein"
            }
        }
    elif diet_type == "Non-Veg":
        plans = {
            "Underweight": {
                "Breakfast": "4 Eggs + Milk",
                "Lunch": "Chicken + Rice",
                "Dinner": "Fish + Roti",
                "Snacks": "Boiled Eggs + Toast",
                "Total": "≈1900 kcal | 110g protein"
            },
            "Normal weight": {
                "Breakfast": "3 Eggs + Toast",
                "Lunch": "Chicken + Rice",
                "Dinner": "Omelette + Veggies",
                "Snacks": "Boiled Egg / Yogurt",
                "Total": "≈1500 kcal | 95g protein"
            },
            "Overweight": {
                "Breakfast": "Boiled Eggs",
                "Lunch": "Grilled Chicken + Salad",
                "Dinner": "Fish Soup",
                "Snacks": "Egg White / Green Tea",
                "Total": "≈1200 kcal | 85g protein"
            },
            "Obese": {
                "Breakfast": "Fruit + Nuts",
                "Lunch": "Grilled Fish + Salad",
                "Dinner": "Soup",
                "Snacks": "Black Coffee / Green Tea",
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
            if diet_type == "Veg":
                key = "Veg"
            elif diet_type == "Vegan":
                key = "Vegan"

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
    st.subheader(f"Weekly Workout Schedule: {goal}")
    
    schedules = {
        "Weight Loss": [
            {"Day": "Monday", "Workout": "HIIT + Core"},
            {"Day": "Tuesday", "Workout": "Full Body Strength"},
            {"Day": "Wednesday", "Workout": "Cardio (Running/Cycling)"},
            {"Day": "Thursday", "Workout": "Rest / Yoga"},
            {"Day": "Friday", "Workout": "Circuit Training"},
            {"Day": "Saturday", "Workout": "Active Recovery (Hike)"},
            {"Day": "Sunday", "Workout": "Rest"}
        ],
        "Fat Loss": [
            {"Day": "Monday", "Workout": "Cardio + Abs"},
            {"Day": "Tuesday", "Workout": "Upper Body Strength"},
            {"Day": "Wednesday", "Workout": "Lower Body Strength"},
            {"Day": "Thursday", "Workout": "HIIT Cardio"},
            {"Day": "Friday", "Workout": "Full Body Workout"},
            {"Day": "Saturday", "Workout": "Active Recovery"},
            {"Day": "Sunday", "Workout": "Rest"}
        ],
        "Muscle Gain": [
            {"Day": "Monday", "Workout": "Chest & Triceps"},
            {"Day": "Tuesday", "Workout": "Back & Biceps"},
            {"Day": "Wednesday", "Workout": "Rest"},
            {"Day": "Thursday", "Workout": "Legs & Shoulders"},
            {"Day": "Friday", "Workout": "Upper Body Hypertrophy"},
            {"Day": "Saturday", "Workout": "Lower Body Power"},
            {"Day": "Sunday", "Workout": "Rest"}
        ],
        "Increase Stamina": [
            {"Day": "Monday", "Workout": "Long Distance Run"},
            {"Day": "Tuesday", "Workout": "Interval Training"},
            {"Day": "Wednesday", "Workout": "Cross-Training (Swim/Cycle)"},
            {"Day": "Thursday", "Workout": "Strength Training"},
            {"Day": "Friday", "Workout": "Tempo Run"},
            {"Day": "Saturday", "Workout": "Long Distance Run"},
            {"Day": "Sunday", "Workout": "Rest"}
        ],
        "Stay Fit": [
            {"Day": "Monday", "Workout": "Chest"},
            {"Day": "Tuesday", "Workout": "Cardio"},
            {"Day": "Wednesday", "Workout": "Legs"},
            {"Day": "Thursday", "Workout": "Rest"},
            {"Day": "Friday", "Workout": "Arms"},
            {"Day": "Saturday", "Workout": "Full Body"},
            {"Day": "Sunday", "Workout": "Yoga"}
        ]
    }

    plan = schedules.get(goal, schedules["Stay Fit"])
    df = pd.DataFrame(plan)
    st.table(df.set_index("Day"))

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
        "Fat Loss": -500,
        "Muscle Gain": 300,
        "Increase Stamina": 0,
        "Stay Fit": 0
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

def calculate_macros(calories, goal):
    """Calculates macronutrient breakdown based on total calories and goal."""
    macro_splits = {
        "Weight Loss": {"protein": 0.4, "carbs": 0.3, "fat": 0.3},
        "Fat Loss": {"protein": 0.45, "carbs": 0.25, "fat": 0.3},
        "Muscle Gain": {"protein": 0.3, "carbs": 0.4, "fat": 0.3},
        "Increase Stamina": {"protein": 0.2, "carbs": 0.5, "fat": 0.3},
        "Stay Fit": {"protein": 0.3, "carbs": 0.4, "fat": 0.3}
    }
    split = macro_splits.get(goal, macro_splits["Stay Fit"])

    protein_grams = int((calories * split["protein"]) / 4)
    carb_grams = int((calories * split["carbs"]) / 4)
    fat_grams = int((calories * split["fat"]) / 9)

    return {"protein": protein_grams, "carbs": carb_grams, "fat": fat_grams}

def generate_fitness_plan_text(user_data):
    name = user_data.get("name", "User")
    goal = user_data.get("goal", "Stay Fit")
    weight = user_data.get("weight", 60.0)
    height = user_data.get("height", 170.0)
    age = user_data.get("age", 25)
    gender = user_data.get("gender", "Male")
    activity = user_data.get("activity_level", "Sedentary")
    diet_type = user_data.get("diet_preference", "Veg")
    
    bmi = calculate_bmi(weight, height)
    bmi_cat = bmi_category(bmi)
    tdee = calculate_calories(weight, height, age, gender, activity)
    target, _ = adjust_calories_for_goal(tdee, goal)
    macros = calculate_macros(target, goal)
    
    plan_text = f"""FITNESS PLAN FOR {name.upper()}
Date: {datetime.date.today()}
----------------------------------------
PROFILE
Goal: {goal}
Height: {height} cm | Weight: {weight} kg
BMI: {bmi:.2f} ({bmi_cat})
Activity Level: {activity}

CALORIE TARGETS
TDEE (Maintenance): {tdee} kcal
Target Calories: {target} kcal
Macros: {macros['protein']}g Protein, {macros['carbs']}g Carbs, {macros['fat']}g Fat

WORKOUT SCHEDULE ({goal})
"""
    schedules = {
        "Weight Loss": ["Mon: HIIT + Core", "Tue: Full Body Strength", "Wed: Cardio", "Thu: Rest", "Fri: Circuit", "Sat: Active Recovery", "Sun: Rest"],
        "Fat Loss": ["Mon: Cardio + Abs", "Tue: Upper Body", "Wed: Lower Body", "Thu: HIIT", "Fri: Full Body", "Sat: Recovery", "Sun: Rest"],
        "Muscle Gain": ["Mon: Chest/Triceps", "Tue: Back/Biceps", "Wed: Rest", "Thu: Legs/Shoulders", "Fri: Upper Body", "Sat: Lower Body", "Sun: Rest"],
        "Increase Stamina": ["Mon: Long Run", "Tue: Intervals", "Wed: Cross-Train", "Thu: Strength", "Fri: Tempo Run", "Sat: Long Run", "Sun: Rest"],
        "Stay Fit": ["Mon: Chest", "Tue: Cardio", "Wed: Legs", "Thu: Rest", "Fri: Arms", "Sat: Full Body", "Sun: Yoga"]
    }
    
    schedule = schedules.get(goal, schedules["Stay Fit"])
    for day in schedule:
        plan_text += f"- {day}\n"

    plan_text += f"\nDIET PLAN ({diet_type} - {bmi_cat})\n"
    
    if diet_type == "Veg":
        if bmi_cat == "Underweight": plan_text += "Breakfast: Oats+Milk+Banana\nLunch: Rice+Dal+Paneer\nDinner: Roti+Chickpeas"
        elif bmi_cat == "Overweight": plan_text += "Breakfast: Sprouts\nLunch: Dal+Salad\nDinner: Soup+Paneer"
        elif bmi_cat == "Obese": plan_text += "Breakfast: Fruit Bowl\nLunch: Mixed Veg+Dal\nDinner: Soup+Salad"
        else: plan_text += "Breakfast: Paneer Sandwich\nLunch: Dal+Rice\nDinner: Roti+Soybean"
    elif diet_type == "Vegan":
        if bmi_cat == "Underweight": plan_text += "Breakfast: Tofu Scramble\nLunch: Lentil Soup+Rice\nDinner: Quinoa Bowl"
        elif bmi_cat == "Overweight": plan_text += "Breakfast: Smoothie\nLunch: Salad+Beans\nDinner: Stir-fry+Tofu"
        elif bmi_cat == "Obese": plan_text += "Breakfast: Fruit\nLunch: Miso Soup\nDinner: Steamed Veg"
        else: plan_text += "Breakfast: Oatmeal\nLunch: Chickpea Salad\nDinner: Black Bean Burgers"
    else: # Non-Veg
        if bmi_cat == "Underweight": plan_text += "Breakfast: 4 Eggs+Milk\nLunch: Chicken+Rice\nDinner: Fish+Roti"
        elif bmi_cat == "Overweight": plan_text += "Breakfast: Boiled Eggs\nLunch: Grilled Chicken\nDinner: Fish Soup"
        elif bmi_cat == "Obese": plan_text += "Breakfast: Fruit+Nuts\nLunch: Grilled Fish\nDinner: Soup"
        else: plan_text += "Breakfast: 3 Eggs+Toast\nLunch: Chicken+Rice\nDinner: Omelette+Veggies"

    plan_text += "\n\nGenerated by Fitness Advisor App"
    return plan_text

# ---------------- Chatbot Data ----------------
QA_DATA = {
    "Can I drink milk during weight loss?": "Yes, you can drink low-fat milk in small quantity. Avoid adding sugar.",
    "Is banana good for fat loss?": "Yes, banana is healthy. But eat in moderation as it has natural sugar.",
    "Can I eat eggs daily?": "Yes, eggs are a great source of protein. 1–2 eggs daily is good.",
    "Is it okay to eat after 8 PM?": "Try to eat at least 2–3 hours before sleep for better digestion.",
    "How much water should I drink daily?": "Drink around 2–3 litres of water daily.",
    "Can I eat junk food once a week?": "Yes, you can have a cheat meal once a week in small portion.",
    "Is intermittent fasting good for beginners?": "Yes, start with a 12–14 hour fasting window.",
    "Can I eat chapati at night?": "Yes, 1–2 chapatis are better than rice at night.",
    "Should I avoid sugar completely?": "Try to reduce sugar intake as much as possible.",
    "Is coffee good for weight loss?": "Black coffee without sugar may help in fat burning.",
    "Is jogging better than walking?": "Jogging burns more calories but walking is safer for beginners.",
    "How long should I exercise daily?": "Exercise at least 30–45 minutes daily.",
    "Can I lose weight without gym?": "Yes, home workouts and diet control can help.",
    "Is skipping good for belly fat?": "Yes, skipping helps burn calories and reduce fat.",
    "How many squats should I do daily?": "Start with 15–20 squats daily.",
    "Is home workout effective?": "Yes, consistency matters more than gym equipment.",
    "Can I workout twice a day?": "Yes, but ensure proper rest in between.",
    "Should I do cardio everyday?": "Yes, light cardio daily is beneficial.",
    "What is the best time to exercise?": "Morning or evening, whichever suits your routine.",
    "Can I build muscles at home?": "Yes, bodyweight exercises are effective.",
    "Why am I not losing weight?": "It may be due to poor diet, lack of exercise or sleep.",
    "How to lose thigh fat?": "Combine cardio with leg workouts.",
    "How to lose face fat?": "Overall weight loss helps reduce face fat.",
    "How to lose arm fat?": "Try pushups and arm exercises regularly.",
    "Can I target belly fat only?": "No, overall fat loss is needed.",
    "Why is my belly fat not reducing?": "Lack of consistency may be the reason.",
    "How many calories should I burn daily?": "Burn 300–500 calories daily.",
    "How fast can I lose weight safely?": "0.5–1 kg per week is safe.",
    "What causes weight gain?": "Overeating and inactivity.",
    "How to reduce love handles?": "Try side planks and cardio.",
    "Is sleep important for weight loss?": "Yes, 7–8 hours of sleep is important.",
    "How many hours should I sleep?": "Sleep at least 7–8 hours daily.",
    "Can stress cause weight gain?": "Yes, stress can lead to weight gain.",
    "Is drinking water before meals helpful?": "Yes, it helps control hunger.",
    "Can I skip breakfast?": "Not recommended regularly.",
    "Does green tea help in fat loss?": "Yes, it may support metabolism.",
    "Is sitting for long hours bad?": "Yes, take breaks often.",
    "Should I rest after workout?": "Yes, rest is necessary for recovery.",
    "Can I eat before workout?": "Yes, eat a light snack.",
    "Is late night snacking bad?": "Yes, it may lead to weight gain."
}

def get_smart_response(question, user_data):
    goal = user_data.get("goal", "Stay Fit")
    question_lower = question.lower()
    
    # 1. Try to find a direct answer from the Knowledge Base
    matches = difflib.get_close_matches(question, QA_DATA.keys(), n=1, cutoff=0.5)
    base_answer = QA_DATA[matches[0]] if matches else None
    
    additional_tip = ""
    
    # 2. Analyze Topic & Generate Contextual Tip based on Goal
    is_diet = any(w in question_lower for w in ["eat", "food", "diet", "drink", "sugar", "fat", "rice", "bread", "milk", "meal", "snack", "tea", "coffee", "water", "fasting"])
    is_workout = any(w in question_lower for w in ["gym", "exercise", "workout", "run", "cardio", "weights", "muscle", "squat", "pushup", "walk", "jog", "yoga", "stretch"])
    
    if is_diet:
        if goal in ["Weight Loss", "Fat Loss"]:
            additional_tip = "📉 **Goal Tip:** Since you're aiming for fat loss, ensure you maintain a calorie deficit and watch portion sizes."
        elif goal == "Muscle Gain":
            additional_tip = "💪 **Goal Tip:** For muscle gain, prioritize protein with every meal to support recovery."
    elif is_workout:
        if goal in ["Weight Loss", "Fat Loss"]:
            additional_tip = "🔥 **Goal Tip:** High-intensity interval training (HIIT) combined with consistency is very effective for your goal."
        elif goal == "Muscle Gain":
            additional_tip = "🏋️ **Goal Tip:** Focus on progressive overload—lifting slightly heavier or doing more reps over time."
            
    # 3. Construct Final Response
    if base_answer:
        return f"{base_answer}\n\n{additional_tip}" if additional_tip else base_answer
    elif additional_tip:
        return f"I don't have a specific answer for that, but here is some advice based on your goal:\n\n{additional_tip}"
    else:
        return f"I'm not sure about that. But keep going with your goal of **{goal}**! Try asking about specific foods or exercises."

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
    # Centered layout with columns
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        st.markdown('<div class="fitness-animate">🏋️</div>', unsafe_allow_html=True)
        st.markdown("<h1 style='text-align: center; color: white; text-shadow: 2px 2px 4px #000000;'>Fitness Advisor</h1>", unsafe_allow_html=True)
        
        # Add a semi-transparent background for readability
        st.markdown(
            """
            <style>
            div[data-testid="stTabs"] {
                background-color: rgba(255, 255, 255, 0.1);
                padding: 20px;
                border-radius: 15px;
                backdrop-filter: blur(10px);
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            }
            </style>
            """,
            unsafe_allow_html=True
        )

        tab1, tab2, tab3 = st.tabs(["Login", "Sign Up", "Forgot Password"])
        
        with tab1:
            st.subheader("Welcome Back")
            username = st.text_input("Username", key="login_user")
            password = st.text_input("Password", type='password', key="login_pass")
            if st.button("Login", use_container_width=True):
                if not os.path.exists("users.json"):
                    st.error("No users found. Please sign up.")
                else:
                    with open("users.json", "r") as f:
                        users = json.load(f)
                    
                    # Handle legacy (string) vs new (dict) format
                    stored_pass = users.get(username)
                    if isinstance(stored_pass, dict):
                        stored_pass = stored_pass.get("password")

                    if username in users and check_hashes(password, stored_pass):
                        st.session_state.logged_in = True
                        st.session_state.username = username
                        st.success("Logged in!")
                        st.rerun()
                    else:
                        st.error("Incorrect Username or Password")

            st.markdown("<div style='text-align: center; color: white; margin: 10px 0;'>OR</div>", unsafe_allow_html=True)
            if st.button("🇬 Google", key="google_login", use_container_width=True):
                with st.spinner("Authenticating with Google..."):
                    time.sleep(1.5)  # Simulate API call
                
                g_user = "jane.doe.google"
                if not os.path.exists("users.json"):
                    with open("users.json", "w") as f:
                        json.dump({}, f)
                with open("users.json", "r") as f:
                    users = json.load(f)
                
                if g_user not in users:
                    users[g_user] = {
                        "password": make_hashes("google_oauth_pass"),
                        "question": "Auth Method",
                        "answer": make_hashes("Google")
                    }
                    with open("users.json", "w") as f:
                        json.dump(users, f)
                
                st.session_state.logged_in = True
                st.session_state.username = g_user
                st.success("Logged in with Google!")
                st.rerun()

        with tab2:
            st.subheader("Create Account")
            new_user = st.text_input("New Username", key="signup_user")
            new_password = st.text_input("New Password", type='password', key="signup_pass")
            
            # Security Question
            sec_q = st.selectbox("Security Question (for password recovery)", [
                "What is the name of your first pet?",
                "What is your mother's maiden name?",
                "What was your first car?",
                "What elementary school did you attend?",
                "What is the name of the town where you were born?"
            ], key="signup_sec_q")
            sec_a = st.text_input("Security Answer", key="signup_sec_a")

            if st.button("Sign Up", use_container_width=True):
                if not new_user or not new_password or not sec_a:
                    st.error("Please fill in all fields.")
                else:
                    if not os.path.exists("users.json"):
                        with open("users.json", "w") as f:
                            json.dump({}, f)
                    with open("users.json", "r") as f:
                        users = json.load(f)
                    if new_user in users:
                        st.error("Username already exists.")
                    else:
                        users[new_user] = {
                            "password": make_hashes(new_password),
                            "question": sec_q,
                            "answer": make_hashes(sec_a)
                        }
                        with open("users.json", "w") as f:
                            json.dump(users, f)
                        st.success("Account created! Please login.")
            
            st.markdown("<div style='text-align: center; color: white; margin: 10px 0;'>OR</div>", unsafe_allow_html=True)
            
            s_col1, s_col2, s_col3 = st.columns(3)
            with s_col1:
                if st.button("🇬 Google", key="google_signup", use_container_width=True):
                    with st.spinner("Authenticating with Google..."):
                        time.sleep(1.5)  # Simulate API call
                    
                    g_user = "jane.doe.google"
                    if not os.path.exists("users.json"):
                        with open("users.json", "w") as f:
                            json.dump({}, f)
                    with open("users.json", "r") as f:
                        users = json.load(f)
                    
                    if g_user not in users:
                        users[g_user] = {
                            "password": make_hashes("google_oauth_pass"),
                            "question": "Auth Method",
                            "answer": make_hashes("Google")
                        }
                        with open("users.json", "w") as f:
                            json.dump(users, f)
                    
                    st.session_state.logged_in = True
                    st.session_state.username = g_user
                    st.success("Signed in with Google!")
                    time.sleep(0.5)
                    st.rerun()

            with s_col2:
                if st.button("📧 Email", key="email_signup_opt", use_container_width=True):
                    st.info("Please enter a Username and Password in the fields above to sign up via Email.")

            with s_col3:
                if st.button("🐙 GitHub", key="github_signup", use_container_width=True):
                    with st.spinner("Authenticating with GitHub..."):
                        time.sleep(1.5)  # Simulate API call
                    
                    gh_user = "john-dev-github"
                    if not os.path.exists("users.json"):
                        with open("users.json", "w") as f:
                            json.dump({}, f)
                    with open("users.json", "r") as f:
                        users = json.load(f)
                    
                    if gh_user not in users:
                        users[gh_user] = {
                            "password": make_hashes("github_oauth_pass"),
                            "question": "Auth Method",
                            "answer": make_hashes("GitHub")
                        }
                        with open("users.json", "w") as f:
                            json.dump(users, f)
                    
                    st.session_state.logged_in = True
                    st.session_state.username = gh_user
                    st.success("Signed in with GitHub!")
                    time.sleep(0.5)
                    st.rerun()

        with tab3:
            st.subheader("Reset Password")
            reset_username = st.text_input("Enter Username", key="reset_username")
            
            if reset_username:
                if os.path.exists("users.json"):
                    with open("users.json", "r") as f:
                        users = json.load(f)
                    
                    if reset_username in users:
                        user_data = users[reset_username]
                        # Check if user has security question set up
                        if isinstance(user_data, dict) and "question" in user_data:
                            st.info(f"Security Question: **{user_data['question']}**")
                            reset_answer = st.text_input("Your Answer", key="reset_answer")
                            new_reset_pass = st.text_input("New Password", type="password", key="new_reset_pass")
                            
                            if st.button("Reset Password", key="btn_reset", use_container_width=True):
                                if check_hashes(reset_answer, user_data['answer']):
                                    user_data['password'] = make_hashes(new_reset_pass)
                                    users[reset_username] = user_data
                                    with open("users.json", "w") as f:
                                        json.dump(users, f)
                                    st.success("Password updated successfully! Please login.")
                                else:
                                    st.error("Incorrect security answer.")
                        else:
                            st.warning("This account is not set up for password recovery.")
                    else:
                        st.error("Username not found.")
                else:
                    st.error("No users found.")

if not st.session_state.logged_in:
    login_page()
    st.stop()

add_bg_from_url()

USER_DATA_FILE = f"user_data_{st.session_state.username}.json"

st.title("Welcome to Fitness Advisor")

# ---------------- Data Loading ----------------
default_data = {
    "name": "", "age": 25, "gender": "Male", 
    "height": 170.0, "weight": 60.0, "goal": "Stay Fit", "activity_level": "Sedentary",
    "history": [], "workout_log": [], "streak": 0, "last_visit": "",
    "schedule": {"Monday": "", "Tuesday": "", "Wednesday": "", "Thursday": "", "Friday": "", "Saturday": "", "Sunday": ""},
    "diet_preference": "Veg", "dietary_restrictions": [], "chat_log": []
}

if os.path.exists(USER_DATA_FILE):
    try:
        with open(USER_DATA_FILE, "r") as f:
            default_data.update(json.load(f))
    except Exception as e:
        st.error(f"Error loading data: {e}")

# Ensure backward compatibility for workout_log
if "workout_log" not in default_data:
    default_data["workout_log"] = []
if "chat_log" not in default_data:
    default_data["chat_log"] = []

# Streak Logic
today_str = datetime.date.today().isoformat()
if default_data["last_visit"] != today_str:
    if default_data["last_visit"] == (datetime.date.today() - datetime.timedelta(days=1)).isoformat():
        default_data["streak"] += 1
    elif default_data["last_visit"] < today_str:
            last_visit_date = datetime.date.fromisoformat(default_data["last_visit"]) if default_data["last_visit"] else datetime.date.min
            if (datetime.date.today() - last_visit_date).days > 1:
                default_data["streak"] = 1
            elif default_data["streak"] == 0:
                default_data["streak"] = 1
    default_data["last_visit"] = today_str

# Extract variables
name = default_data["name"]
age = int(default_data["age"])
gender = default_data["gender"]
height_cm = float(default_data["height"])
weight = float(default_data["weight"])
goal = default_data["goal"]

# Calculate BMI
bmi = 0
category = "Normal weight"
if height_cm > 0 and weight > 0:
    bmi = calculate_bmi(weight, height_cm)
    category = bmi_category(bmi)

# ---------------- Sidebar ----------------
with st.sidebar:
    st.write(f"Logged in as: **{st.session_state.username}**")
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.rerun()
    
    st.divider()
    with st.expander("📧 Notification Settings"):
        st.caption("Enter your email to receive workout updates.")
        st.session_state.receiver_email = st.text_input("Receiver Email", value=st.session_state.get("receiver_email", ""))
    st.divider()

    page = st.radio("Navigate", ["Input Form", "Dashboard", "Workout Routine", "Nutrition Plan", "AI Chat Help"])

# ---------------- Main Content ----------------
if page == "Input Form":
    st.header("Edit Profile")
    
    new_name = st.text_input("Name", value=name)
    if new_name and not re.match(r"^[A-Za-z ]+$", new_name):
        st.error("Name must contain only letters and spaces. No numbers or symbols allowed.")
        new_name = ""
        
    new_age = st.number_input("Age", min_value=1, max_value=120, value=age)
    
    gender_index = 0 if gender == "Male" else 1
    new_gender = st.radio("Gender", ["Male", "Female"], index=gender_index, horizontal=True)

    goal_options = ["Weight Loss", "Muscle Gain", "Stay Fit", "Fat Loss", "Increase Stamina"]
    try:
        goal_index = goal_options.index(goal)
    except ValueError:
        goal_index = 2
    new_goal = st.selectbox("Your Fitness Goal", goal_options, index=goal_index)

    new_height = st.number_input("Height (cm)", min_value=50.0, max_value=300.0, value=max(50.0, min(height_cm, 300.0)))
    new_weight = st.number_input("Weight (kg)", min_value=10.0, max_value=500.0, value=max(10.0, min(weight, 500.0)))

    activity_options = ["Sedentary", "Lightly Active", "Moderately Active", "Very Active"]
    current_activity = default_data.get("activity_level", "Sedentary")
    try:
        activity_index = activity_options.index(current_activity)
    except ValueError:
        activity_index = 0
    new_activity_level = st.selectbox("Activity Level", activity_options, index=activity_index)

    uploaded_pic = st.file_uploader("Upload Profile Picture", type=["jpg", "jpeg", "png"])
    profile_pic = default_data.get("profile_pic", "")

    if uploaded_pic:
        if not os.path.exists("profile_pics"):
            os.makedirs("profile_pics")
        profile_pic = f"profile_pics/{st.session_state.username}_{uploaded_pic.name}"
        with open(profile_pic, "wb") as f:
            f.write(uploaded_pic.getbuffer())

    if st.button("Save Profile"):
        new_history_entry = {"date": today_str, "weight": new_weight, "bmi": calculate_bmi(new_weight, new_height)}
        if not default_data["history"] or default_data["history"][-1]["date"] != today_str:
            default_data["history"].append(new_history_entry)
        else:
            default_data["history"][-1] = new_history_entry

        user_data = {
            "name": new_name, "age": new_age, "gender": new_gender, 
            "height": new_height, "weight": new_weight, "goal": new_goal, "activity_level": new_activity_level,
            "history": default_data["history"], "streak": default_data["streak"], "last_visit": today_str,
            "schedule": default_data.get("schedule", {}),
            "workout_log": default_data.get("workout_log", []),
            "profile_pic": profile_pic
        }
        with open(USER_DATA_FILE, "w") as f:
            json.dump(user_data, f)
        st.success("Profile saved!")
        st.rerun()

elif page == "Dashboard":
    if name and height_cm > 0 and weight > 0:
        st.header(f"Hello, {name}!")
        
        # Badges
        badges = check_badges(default_data["streak"], default_data["history"])
        if badges:
            st.write("### Achievements")
            st.write(" ".join([f"`{b}`" for b in badges]))
        
        # Calculate BMR, TDEE, Target
        if gender == "Male":
            bmr_val = (10 * weight) + (6.25 * height_cm) - (5 * age) + 5
        else:
            bmr_val = (10 * weight) + (6.25 * height_cm) - (5 * age) - 161
        
        activity_lvl = default_data.get("activity_level", "Sedentary")
        tdee_val = calculate_calories(weight, height_cm, age, gender, activity_lvl)
        target_val, _ = adjust_calories_for_goal(tdee_val, goal)

        col1, col2, col3 = st.columns(3)
        col1.metric("BMI", f"{bmi:.2f}", category)
        col2.metric("BMR", f"{int(bmr_val)} kcal")
        col3.metric("TDEE", f"{tdee_val} kcal")

        col4, col5, col6 = st.columns(3)
        col4.metric("Target Calories", f"{target_val} kcal", goal)
        col5.metric("Current Weight", f"{weight} kg")
        col6.metric("Streak", f"{default_data['streak']} Days")

        st.markdown('<div class="light-blue-button">', unsafe_allow_html=True)
        st.download_button(
            label="📥 Download My Fitness Plan",
            data=generate_fitness_plan_text(default_data),
            file_name=f"fitness_plan_{name}.txt",
            mime="text/plain"
        )
        st.markdown('</div>', unsafe_allow_html=True)

        # Workout History Table
        st.subheader("🏋️ Recent Workouts")
        if default_data.get("workout_log"):
            w_df = pd.DataFrame(default_data["workout_log"])
            st.dataframe(w_df.sort_values(by="date", ascending=False).head(5), use_container_width=True)
        else:
            st.info("No workouts logged yet. Go to 'Workout Routine' to log one!")

        # Progress Graph
        st.subheader("Weight Progress")
        
        with st.expander("⚖️ Weekly Check-in: Update Weight"):
            checkin_weight = st.number_input("Current Weight (kg)", min_value=10.0, max_value=500.0, value=weight, key="checkin_w")
            if st.button("Update Weight"):
                new_bmi = calculate_bmi(checkin_weight, height_cm)
                new_entry = {"date": today_str, "weight": checkin_weight, "bmi": new_bmi}
                
                if not default_data["history"]:
                    default_data["history"].append(new_entry)
                elif default_data["history"][-1]["date"] == today_str:
                    default_data["history"][-1] = new_entry
                else:
                    default_data["history"].append(new_entry)
                
                default_data["weight"] = checkin_weight
                with open(USER_DATA_FILE, "w") as f:
                    json.dump(default_data, f)
                st.toast("Weight updated successfully!")
                time.sleep(1)
                st.rerun()

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
    else:
        st.info("👉 Please go to **Input Form** to fill your details.")

elif page == "Workout Routine":
    if name and height_cm > 0 and weight > 0:
        st.header("Workout Recommendations")
        
        # Log Workout Section
        with st.expander("📝 Log Completed Workout", expanded=True):
            with st.form("log_workout_form"):
                c1, c2 = st.columns(2)
                with c1:
                    w_type = st.selectbox("Activity Type", ["Gym", "Yoga", "Cardio", "Sports", "Home Workout"])
                    w_duration = st.number_input("Duration (mins)", min_value=5, value=45, step=5)
                with c2:
                    w_cal = st.number_input("Calories Burned (approx)", min_value=0, value=200, step=10)
                    w_date = st.date_input("Date", datetime.date.today())
                
                w_notes = st.text_area("Notes (e.g., 'Hit a PR on bench press')")
                st.markdown('<div class="light-blue-button">', unsafe_allow_html=True)
                submit_log = st.form_submit_button("Log Workout & Notify")
                st.markdown('</div>', unsafe_allow_html=True)
                
                if submit_log:
                    log_entry = {
                        "date": w_date.isoformat(),
                        "type": w_type,
                        "duration": w_duration,
                        "calories": w_cal,
                        "notes": w_notes
                    }
                    default_data["workout_log"].append(log_entry)
                    
                    # Save to file
                    with open(USER_DATA_FILE, "w") as f:
                        json.dump(default_data, f)
                    
                    st.success("Workout logged successfully!")

                    # Send Email
                    if st.session_state.get("receiver_email") and SYSTEM_EMAIL != "your_app_email@gmail.com":
                        subject = f"Fitness Update: {w_type} Completed! ✅"
                        body = f"Great job, {name}!\n\nYou just completed a {w_duration} minute {w_type} session burning approx {w_cal} calories.\n\nNotes: {w_notes}\n\nKeep up the streak!"
                        success, msg = send_email_notification(SYSTEM_EMAIL, SYSTEM_PASSWORD, st.session_state.receiver_email, subject, body)
                        if success:
                            st.toast(msg)
                        else:
                            st.error(msg)
                    elif not st.session_state.get("receiver_email"):
                        st.warning("Workout saved. To receive emails, enter your email in the Sidebar.")
                    elif SYSTEM_EMAIL == "your_app_email@gmail.com":
                        st.warning("Workout saved. Email notification disabled (System Email not configured in code).")

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
                with open(USER_DATA_FILE, "w") as f:
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
    else:
        st.info("👉 Please go to **Input Form** to fill your details.")

elif page == "Nutrition Plan":
    if name and height_cm > 0 and weight > 0:
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

            st.subheader("Suggested Macronutrient Breakdown")
            macros = calculate_macros(goal_calories, goal)
            p_col, c_col, f_col = st.columns(3)
            p_col.metric("Protein", f"{macros['protein']}g")
            c_col.metric("Carbs", f"{macros['carbs']}g")
            f_col.metric("Fat", f"{macros['fat']}g")

        # Meal Reminders
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
            saved_diet = default_data.get("diet_preference", "Veg")
            options = ["Veg", "Non-Veg", "Vegan"]
            try:
                idx = options.index(saved_diet)
            except ValueError:
                idx = 0
            
            diet_preference = st.selectbox(
                "Primary Diet Style",
                options,
                index=idx
            )
        with c2:
            saved_restrictions = default_data.get("dietary_restrictions", [])
            dietary_restrictions = st.multiselect(
                "Additional Restrictions",
                ["Gluten-Free", "Dairy-Free", "Nut-Free"],
                default=saved_restrictions,
                help="Select any dietary restrictions you have. The plans will be adjusted with notes."
            )
        
        if st.button("Save Nutrition Plan"):
            default_data["diet_preference"] = diet_preference
            default_data["dietary_restrictions"] = dietary_restrictions
            with open(USER_DATA_FILE, "w") as f:
                json.dump(default_data, f)
            st.success("Nutrition plan saved successfully!")

        diet_view = st.radio("Choose plan format:", ["Daily (BMI Based)", "Weekly"], horizontal=True)

        if diet_view == "Daily (BMI Based)":
            display_diet_plan(diet_preference, category, gender, dietary_restrictions)
        else:
            display_weekly_diet_plan(diet_preference, dietary_restrictions)
    else:
        st.info("👉 Please go to **Input Form** to fill your details.")

elif page == "AI Chat Help":
    st.header("🤖 Fitness Chat Assistant")
    
    c1, c2 = st.columns([3, 1])
    with c1:
        st.write("Ask me anything about fitness, diet, or weight loss!")
    with c2:
        if st.button("🗑️ Clear Chat"):
            st.session_state.messages = [{"role": "assistant", "content": "Chat cleared. How can I help you now?"}]
            st.rerun()

    with st.expander("📜 Chat History"):
        if default_data.get("chat_log"):
            # Deduplicate and show recent
            seen = set()
            unique_history = []
            for q in reversed(default_data["chat_log"]):
                if q not in seen:
                    unique_history.append(q)
                    seen.add(q)
            
            st.caption("Click a question to ask it again:")
            for q in unique_history[:5]:
                if st.button(q, key=f"hist_{q}"):
                    st.session_state.messages.append({"role": "user", "content": q})
                    
                    answer = "I'm not sure about that. Try asking something else from the list!"
                    matches = difflib.get_close_matches(q, QA_DATA.keys(), n=1, cutoff=0.5)
                    if matches:
                        answer = QA_DATA[matches[0]]
                    
                    st.session_state.messages.append({"role": "assistant", "content": answer})
                    
                    # Update log order
                    if q in default_data["chat_log"]:
                        default_data["chat_log"].remove(q)
                    default_data["chat_log"].append(q)
                    with open(USER_DATA_FILE, "w") as f:
                        json.dump(default_data, f)
                    st.rerun()
        else:
            st.info("No search history yet.")

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": "Hello! I am your AI Fitness Advisor. Ask me about workouts, diet plans, or general health tips!"}]

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        avatar = "👤" if message["role"] == "user" else "🤖"
        with st.chat_message(message["role"], avatar=avatar):
            st.markdown(message["content"])

    # Voice Input
    audio_value = st.audio_input("🎤 Record your question")
    voice_prompt = None

    if audio_value:
        if OPENAI_API_KEY == "your_openai_api_key":
            st.warning("⚠️ OpenAI API Key not configured. Please set OPENAI_API_KEY in the code.")
        else:
            try:
                client = OpenAI(api_key=OPENAI_API_KEY)
                with st.spinner("Transcribing audio..."):
                    transcription = client.audio.transcriptions.create(
                        model="whisper-1", 
                        file=audio_value
                    )
                    voice_prompt = transcription.text
                    st.success(f"Transcribed: {voice_prompt}")
            except Exception as e:
                st.error(f"Error transcribing audio: {e}")

    # React to user input
    chat_input = st.chat_input("Type your question here...")
    
    prompt = chat_input if chat_input else voice_prompt

    # Prevent re-processing the same voice input on rerun
    if voice_prompt and not chat_input:
        if "last_voice_prompt" in st.session_state and st.session_state.last_voice_prompt == voice_prompt:
            prompt = None
        else:
            st.session_state.last_voice_prompt = voice_prompt

    if prompt:
        # Display user message in chat message container
        st.chat_message("user", avatar="👤").markdown(prompt)
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Save to chat log
        default_data["chat_log"].append(prompt)
        with open(USER_DATA_FILE, "w") as f:
            json.dump(default_data, f)

        # Find answer
        answer = get_smart_response(prompt, default_data)

        # Display assistant response in chat message container
        with st.chat_message("assistant", avatar="🤖"):
            st.markdown(answer)
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": answer})
