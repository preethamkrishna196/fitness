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
             background-image: url("https://images.unsplash.com/photo-1517836357463-d25dfeac3438");
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
            {"name": "Push-ups", "img": "https://images.unsplash.com/photo-1571019614242-c5c5dee9f50b", "vid": "https://www.youtube.com/watch?v=IODxDxX7oi4"},
            {"name": "Bench Press", "img": "https://images.unsplash.com/photo-1534438327276-14e5300c3a48", "vid": "https://www.youtube.com/watch?v=rT7DgCr-3pg"},
        ],
        "Back": [
            {"name": "Pull-ups", "img": "https://images.unsplash.com/photo-1598971639058-211a74a96aea", "vid": "https://www.youtube.com/watch?v=eGo4IYlbE5g"},
            {"name": "Lat Pulldown", "img": "https://images.unsplash.com/photo-1605296867304-6f2a41a42262", "vid": "https://www.youtube.com/watch?v=CAwf7n6Luuc"},
        ],
        "Shoulders": [
            {"name": "Shoulder Press", "img": "https://images.unsplash.com/photo-1541534741688-6078c6bfb5c5", "vid": "https://www.youtube.com/watch?v=qEwKCR5JCog"},
        ],
        "Arms": [
            {"name": "Bicep Curls", "img": "https://images.unsplash.com/photo-1581009146145-b5ef050c2e1e", "vid": "https://www.youtube.com/watch?v=ykJmrZ5v0Oo"},
            {"name": "Tricep Dips", "img": "https://images.unsplash.com/photo-1583454110551-21f2fa2afe61", "vid": "https://www.youtube.com/watch?v=6kALZikXxLc"},
        ],
        "Legs": [
            {"name": "Squats", "img": "https://images.unsplash.com/photo-1574680096141-1cddd32e04ca", "vid": "https://www.youtube.com/watch?v=YaXPRqUwItQ"},
            {"name": "Lunges", "img": "https://images.unsplash.com/photo-1434608519344-49d77a699ded", "vid": "https://www.youtube.com/watch?v=QOVaHwm-Q6U"},
        ]
    }

    for muscle, exercises in gym_exercises.items():
        st.markdown(f"#### {muscle}")
        for ex in exercises:
            with st.expander(ex["name"]):
                col1, col2 = st.columns(2)
                with col1:
                    st.image(ex["img"], caption=ex["name"], use_column_width=True)
                with col2:
                    st.video(ex["vid"])

def display_yoga_asanas():
    st.subheader("Beginner Friendly Yoga Asanas")
    
    yoga_asanas = [
        {"name": "Sun Salutations (Surya Namaskar)", "img": "https://chatgpt.com/backend-api/estuary/content?id=786379a34887956%23file_00000000da0871f88d9921555c9b3354%23md&ts=491173&p=fs&cid=1&sig=4fefd52ee7ffbc560dd34f2806ae7c64307d1a45c875ae20eb3d442b3da7def9&v=0", "vid": "https://www.youtube.com/watch?v=6IUyY9Dyr5w"},
        {"name": "Chair Pose (Utkatasana)", "img": "https://chatgpt.com/backend-api/estuary/content?id=6707b6017504ac5%23file_00000000dd2871f8b274ee6f41de50fd%23md&ts=491173&p=fs&cid=1&sig=148f8e59545982854d8549f614657eee70794134b424f374cef0be8a7229519a&v=0", "vid": "https://www.youtube.com/shorts/_GIKyB_n1TA"},
        {"name": "Warrior I & II (Virabhadrasana)", "img": "https://srisrischoolofyoga.org/na/wp-content/uploads/2023/01/warrior-pose-three-variations-1-2-3.jpg", "vid": "https://www.youtube.com/watch?v=sCReePaPF50"},
        {"name": "Cobra Pose (Bhujangasana)", "img": "https://chatgpt.com/backend-api/estuary/content?id=79cfe45a77484b7%23file_00000000945071fda73a71a738919e30%23md&ts=491174&p=fs&cid=1&sig=4a86723862867707467e034297818d21f8f39ff6877cb91fd8bb18546ea0bf4d&v=0", "vid": "https://www.youtube.com/watch?v=fOdrW7nf9gw"},
        {"name": "Bridge Pose (Setu Bandhasana)", "img": "https://chatgpt.com/backend-api/estuary/content?id=37ee69d03cfa829%23file_00000000f13c71f897a135fa711852e5%23md&ts=491174&p=fs&cid=1&sig=c264aa99d0467e0701db6aa375740c70f559a383784126e02334fb1d5f8434fc&v=0", "vid": "https://www.youtube.com/watch?v=NnbvPeAIhmA"},
        {"name": "Plank Pose (Phalakasana)", "img": "https://chatgpt.com/backend-api/estuary/content?id=8751a6defeec286%23file_00000000212871f881b56606a9d5adc4%23md&ts=491174&p=fs&cid=1&sig=57d5726c5f177d2a8d497dbf9b681e07d23c7cefd6b3cc28787ef3a94b9c1e50&v=0", "vid": "https://www.youtube.com/watch?v=RG4PwUP5njo"},
        {"name": "Boat Pose (Navasana)", "img": "https://www.rishikulyogshalarishikesh.com/blog/wp-content/uploads/2023/10/Navasana-1.jpg", "vid": "https://www.youtube.com/watch?v=U0uFz7sEw94"},
        {"name": "Triangle Pose (Trikonasana)", "img": "https://www.solara.in/cdn/shop/articles/Trikonasana_Benefits.jpg?v=1710761847&width=2048", "vid": "https://www.youtube.com/shorts/ailoSBERStw"},
    ]

    for asana in yoga_asanas:
        with st.expander(asana["name"]):
            col1, col2 = st.columns(2)
            with col1:
                st.image(asana["img"], caption=asana["name"], use_column_width=True)
            with col2:
                st.video(asana["vid"])

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
