import streamlit as st

def calculate_bmi(weight, height_cm):
    if height_cm <= 0:
        return 0
    height_m = height_cm / 100
    return weight / (height_m * height_m)

def bmi_category(bmi):
    if bmi < 18.5:
        return "Underweight"
    elif bmi < 24.9:
        return "Normal weight"
    elif bmi < 29.9:
        return "Overweight"
    else:
        return "Obese"

def display_gym_workouts():
    st.subheader("Gym Workouts")
    st.write("- **Chest:** Push-ups, Bench Press")
    st.write("- **Back:** Pull-ups, Lat Pulldown")
    st.write("- **Shoulders:** Shoulder Press")
    st.write("- **Arms:** Bicep Curls, Tricep Dips")
    st.write("- **Legs:** Squats, Lunges")

def display_yoga_asanas():
    st.subheader("Beginner Friendly Yoga Asanas")
    st.write("- Tadasana, Vrikshasana, Bhujangasana")
    st.write("- Adho Mukha Svanasana, Balasana")

def display_veg_diet():
    st.subheader("Weekly Vegetarian Diet (80g+ Protein/Day)")
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    
    # Using an expander for each day to keep the UI clean
    for day in days:
        with st.expander(day):
            st.write("**Breakfast:** Paneer + Milk (30g protein)")
            st.write("**Lunch:** Dal + Rice + Curd (30g protein)")
            st.write("**Dinner:** Chickpeas + Roti (25g protein)")
            st.write("**Total Protein:** 85g")

def display_nonveg_diet():
    st.subheader("Weekly Non-Vegetarian Diet (80g+ Protein/Day)")
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    
    for day in days:
        with st.expander(day):
            st.write("**Breakfast:** Boiled Eggs + Milk (30g protein)")
            st.write("**Lunch:** Chicken + Rice (35g protein)")
            st.write("**Dinner:** Fish / Omelette (25g protein)")
            st.write("**Total Protein:** 90g")

# --- Main Streamlit App ---
st.set_page_config(page_title="Fitness Advisor", page_icon="💪")

st.title("===== Welcome to Fitness Advisor =====")

# Sidebar for User Inputs
with st.sidebar:
    st.header("Enter Your Details")
    name = st.text_input("Name")
    age = st.number_input("Age", min_value=1, max_value=120, step=1)
    height_cm = st.number_input("Height (cm)", min_value=1.0, format="%.2f")
    weight = st.number_input("Weight (kg)", min_value=1.0, format="%.2f")
    
    st.markdown("---")
    st.write("Fill in your details to see the report.")

# Main Content Area
if name and height_cm and weight:
    # 1. Health Report
    bmi = calculate_bmi(weight, height_cm)
    category = bmi_category(bmi)

    st.header("Health Report")
    col1, col2 = st.columns(2)
    with col1:
        st.write(f"**Name:** {name}")
        st.write(f"**Age:** {age}")
    with col2:
        st.write(f"**BMI:** {bmi:.2f}")
        st.write(f"**Category:** {category}")
        
    # Color-coded metric for BMI
    if category == "Normal weight":
        st.success(f"You are in the {category} range.")
    elif category == "Underweight":
        st.warning(f"You are in the {category} range.")
    else:
        st.error(f"You are in the {category} range.")

    st.divider()

    # 2. Workout Selection
    st.header("Choose Workout Type")
    workout_choice = st.radio("Select your preferred workout:", ["Gym", "Yoga"], horizontal=True)

    if workout_choice == "Gym":
        display_gym_workouts()
    elif workout_choice == "Yoga":
        display_yoga_asanas()

    st.divider()

    # 3. Diet Selection
    st.header("Choose Diet Type")
    diet_choice = st.radio("Select your preferred diet:", ["Vegetarian", "Non-Vegetarian"], horizontal=True)

    if diet_choice == "Vegetarian":
        display_veg_diet()
    elif diet_choice == "Non-Vegetarian":
        display_nonveg_diet()

    st.divider()
    st.success("Thank you for using Fitness Advisor!")

else:
    st.info("👈 Please enter your name, height, and weight in the sidebar to generate your fitness plan.")
