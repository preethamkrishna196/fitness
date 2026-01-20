import streamlit as st

def calculate_bmi(weight, height_cm):
    if height_cm <= 0:
        return 0
    height_m = height_cm / 100
    return weight / (height_m * height_m)

def add_bg_from_url():
    st.markdown(
         f"""
         <style>
         .stApp {{
             background-image: url("https://images.pexels.com/photos/841130/pexels-photo-841130.jpeg");
             background-attachment: fixed;
             background-size: cover;
         }}

         /* Make text white for readability on dark background */
         h1, h2, h3, label, summary, [data-testid="stRadio"] [role="radiogroup"] div {{
            color: white !important;
         }}

         [data-testid="stMarkdownContainer"] p, [data-testid="stMarkdownContainer"] li {{
            color: white !important;
         }}

         [data-testid="stSidebar"] {{
            background-color: rgba(0, 0, 0, 0);
            backdrop-filter: blur(10px);
         }}

         </style>
         """,
         unsafe_allow_html=True
     )

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
    
    gym_exercises = {
        "Chest": [
            {"name": "Push-ups", "img": "https://images.pexels.com/photos/176782/pexels-photo-176782.jpeg?auto=compress&cs=tinysrgb&w=800"},
            {"name": "Bench Press", "img": "https://images.pexels.com/photos/3837781/pexels-photo-3837781.jpeg?auto=compress&cs=tinysrgb&w=800"},
        ],
        "Back": [
            {"name": "Pull-ups", "img": "https://images.pexels.com/photos/35649982/pexels-photo-35649982.jpeg"},
            {"name": "Lat Pulldown", "img": "https://www.pexels.com/photo/back-view-of-a-man-doing-pull-ups-in-a-gym-29084397/"},
        ],
        "Shoulders": [
            {"name": "Shoulder Press", "img": "https://images.pexels.com/photos/1552249/pexels-photo-1552249.jpeg?auto=compress&cs=tinysrgb&w=800"},
        ],
        "Arms": [
            {"name": "Bicep Curls", "img": "https://images.pexels.com/photos/1229356/pexels-photo-1229356.jpeg?auto=compress&cs=tinysrgb&w=800"},
            {"name": "Tricep Dips", "img": "https://www.pexels.com/photo/strong-man-training-in-modern-gym-5496589/"},
        ],
        "Legs": [
            {"name": "Squats", "img": "https://images.pexels.com/photos/1552252/pexels-photo-1552252.jpeg?auto=compress&cs=tinysrgb&w=800"},
            {"name": "Lunges", "img": "https://images.pexels.com/photos/4162445/pexels-photo-4162445.jpeg?auto=compress&cs=tinysrgb&w=800"},
        ]
    }

    for muscle, exercises in gym_exercises.items():
        st.markdown(f"#### {muscle}")
        for ex in exercises:
            with st.expander(ex["name"]):
                st.image(ex["img"], caption=ex["name"], use_container_width=True)

def display_yoga_asanas():
    st.subheader("Beginner Friendly Yoga Asanas")
    
    yoga_asanas = [
        {"name": "Sun Salutations (Surya Namaskar)", "img": "https://m.media-amazon.com/images/I/71YQoq8+neL._AC_UF894,1000_QL80_.jpg"},
        {"name": "Chair Pose (Utkatasana)", "img": "https://thumbs.dreamstime.com/b/beautiful-yoga-chair-pose-side-view-portrait-young-woman-wearing-white-sportswear-working-out-against-grey-wall-doing-83518417.jpg"},
        {"name": "Warrior I & II (Virabhadrasana)", "img": "https://www.shutterstock.com/image-vector/young-woman-standing-virabhadrasana-active-260nw-2125965767.jpg"},
        {"name": "Cobra Pose (Bhujangasana)", "img": "https://images.pexels.com/photos/3823076/pexels-photo-3823076.jpeg?auto=compress&cs=tinysrgb&w=800"},
        {"name": "Bridge Pose (Setu Bandhasana)", "img": "https://i.pinimg.com/736x/75/b1/ea/75b1ea4d05b89cf46917566978c7fc19.jpg"},
        {"name": "Triangle Pose (Trikonasana)", "img": "https://media.istockphoto.com/id/636608240/photo/utthita-trikonasana-extended-triangle-pose.jpg?s=612x612&w=0&k=20&c=F8F8TMH1sB2YbQst13-5SqqocAkyDN3cMJJsjIaVnMs="},
    ]

    for asana in yoga_asanas:
        with st.expander(asana["name"]):
            st.image(asana["img"], caption=asana["name"], use_container_width=True)

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

add_bg_from_url()

st.title("Welcome to Fitness Advisor ")

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
if name.strip() != "" and height_cm > 0 and weight > 0:
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
