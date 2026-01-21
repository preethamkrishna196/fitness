import streamlit as st

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
        h1, h2, h3, label, p {
            color: white !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

# ---------------- Diet Section ----------------
def display_diet_plan(diet_type, bmi_cat, gender):
    st.subheader(f"{diet_type} Diet Plan")

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

# ---------------- Workout Tips ----------------
def display_gender_workout_tips(gender):
    st.subheader("Personalized Workout Tips")
    if gender == "Male":
        st.info("💪 Focus on strength training, compound lifts, 4–5 days/week.")
    else:
        st.info("🌸 Focus on toning, flexibility, core strength, 3–5 days/week.")

# ---------------- Gym Workouts ----------------
def display_gym_workouts(gender):
    st.subheader("Gym Workouts")

    if gender == "Male":
        workouts = {
            "Chest": ["Bench Press", "Push-ups", "Incline Dumbbell Press"],
            "Back": ["Pull-ups", "Lat Pulldown", "Deadlifts"],
            "Shoulders": ["Overhead Press", "Lateral Raises"],
            "Arms": ["Bicep Curls", "Tricep Dips"],
            "Legs": ["Squats", "Leg Press", "Lunges"]
        }
    else:
        workouts = {
            "Lower Body": ["Glute Bridges", "Lunges", "Leg Press"],
            "Core": ["Plank", "Crunches", "Russian Twists"],
            "Arms": ["Resistance Band Curls", "Tricep Kickbacks"],
            "Full Body": ["Bodyweight Squats", "Push-ups"],
            "Cardio": ["Treadmill", "Cycling"]
        }

    for muscle, exercises in workouts.items():
        with st.expander(muscle):
            for ex in exercises:
                st.write(f"• {ex}")

# ---------------- Yoga Workouts ----------------
def display_yoga_asanas(gender):
    st.subheader("Yoga Asanas")

    if gender == "Male":
        asanas = [
            "Surya Namaskar",
            "Bhujangasana (Cobra Pose)",
            "Trikonasana (Triangle Pose)",
            "Vrikshasana (Tree Pose)",
            "Adho Mukha Svanasana"
        ]
    else:
        asanas = [
            "Surya Namaskar",
            "Utkatasana (Chair Pose)",
            "Setu Bandhasana (Bridge Pose)",
            "Balasana (Child’s Pose)",
            "Baddha Konasana (Butterfly Pose)"
        ]

    for pose in asanas:
        with st.expander(pose):
            st.write(f"✔ Recommended for {gender}")

# ---------------- Main App ----------------
st.set_page_config(page_title="Fitness Advisor", page_icon="🏋️")
add_bg_from_url()

st.title("Welcome to Fitness Advisor")

# ---------------- Sidebar ----------------
with st.sidebar:
    st.header("Enter Your Details")
    name = st.text_input("Name")
    age = st.number_input("Age", min_value=1, max_value=120)
    gender = st.radio("Gender", ["Male", "Female"], horizontal=True)
    height_cm = st.number_input("Height (cm)", min_value=1.0)
    weight = st.number_input("Weight (kg)", min_value=1.0)

# ---------------- Main Content ----------------
if name and height_cm > 0 and weight > 0:
    bmi = calculate_bmi(weight, height_cm)
    category = bmi_category(bmi)

    st.header("Health Report")
    col1, col2 = st.columns(2)

    with col1:
        st.write(f"**Name:** {name}")
        st.write(f"**Age:** {age}")
        st.write(f"**Gender:** {gender}")

    with col2:
        st.write(f"**BMI:** {bmi:.2f}")
        st.write(f"**Category:** {category}")

    st.divider()

    # Workout Section
    st.header("Workout Recommendations")
    display_gender_workout_tips(gender)

    workout_choice = st.radio(
        "Choose workout type:",
        ["Gym", "Yoga"],
        horizontal=True
    )

    if workout_choice == "Gym":
        display_gym_workouts(gender)
    else:
        display_yoga_asanas(gender)

    st.divider()

    # Diet Section
    st.header("Diet Plan")
    diet_choice = st.radio(
        "Choose diet type:",
        ["Vegetarian", "Non-Vegetarian"],
        horizontal=True
    )

    display_diet_plan(diet_choice, category, gender)

    st.success("Thank you for using Fitness Advisor!")
else:
    st.info("👉 Please fill all details in the sidebar.")
