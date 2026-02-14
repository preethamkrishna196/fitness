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

try:
    from fpdf import FPDF
except ImportError:
    FPDF = None

try:
    import google.generativeai as genai
except ImportError:
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "google-generativeai"])
        import google.generativeai as genai
    except Exception:
        genai = None


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


# ---------------- Background ----------------
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
        div[data-testid="stButton"] > button {
            background-color: #007bff;
            color: white;
            border-color: #007bff;
        }
        div[data-testid="stButton"] > button:hover {
            background-color: #0056b3;
            border-color: #0056b3;
            color: white;
        }
        </style>
        """,
        unsafe_allow_html=True
    )


# ---------------- Strict Name Validation ----------------
def validate_name():
    # Only letters and spaces allowed
    if not re.fullmatch(r"[A-Za-z\s]*", st.session_state.name_input):
        st.session_state.name_error = True
    else:
        st.session_state.name_error = False


# ---------------- Main Config ----------------
st.set_page_config(page_title="Fitness Advisor", page_icon="🏋️")
add_bg_from_url()

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = ""


# ---------------- Login System ----------------
def make_hashes(password):
    return hashlib.sha256(str.encode(password)).hexdigest()


def check_hashes(password, hashed_text):
    return make_hashes(password) == hashed_text


def login_page():
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

    default_data = {
        "name": "",
        "age": 25,
        "gender": "Male",
        "height": 170.0,
        "weight": 60.0,
        "history": [],
        "streak": 0,
        "last_visit": ""
    }

    if os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, "r") as f:
            default_data.update(json.load(f))

    # ---- Name Validation Section ----
    if "name_input" not in st.session_state:
        st.session_state.name_input = default_data["name"]

    if "name_error" not in st.session_state:
        st.session_state.name_error = False

    st.text_input(
        "Name",
        key="name_input",
        on_change=validate_name
    )

    if st.session_state.name_error:
        st.error("❌ Only letters and spaces are allowed. No numbers or symbols.")

    name = st.session_state.name_input if not st.session_state.name_error else ""

    age = st.number_input("Age", min_value=1, max_value=120, value=int(default_data["age"]))
    gender = st.radio("Gender", ["Male", "Female"], horizontal=True)
    height_cm = st.number_input("Height (cm)", min_value=1.0, value=float(default_data["height"]))
    weight = st.number_input("Weight (kg)", min_value=1.0, value=float(default_data["weight"]))

    if st.button("Save Profile"):
        if st.session_state.name_error or name.strip() == "":
            st.error("Please enter a valid name before saving.")
        else:
            today_str = datetime.date.today().isoformat()
            bmi = calculate_bmi(weight, height_cm)

            user_data = {
                "name": name,
                "age": age,
                "gender": gender,
                "height": height_cm,
                "weight": weight,
                "history": [{"date": today_str, "weight": weight, "bmi": bmi}],
                "last_visit": today_str
            }

            with open(USER_DATA_FILE, "w") as f:
                json.dump(user_data, f)

            st.success("Profile saved successfully!")


# ---------------- Main Content ----------------
if not st.session_state.name_error and st.session_state.name_input:

    bmi = calculate_bmi(weight, height_cm)
    category = bmi_category(bmi)

    st.subheader(f"Hello, {name}!")
    col1, col2 = st.columns(2)
    col1.metric("BMI", f"{bmi:.2f}", category)
    col2.metric("Weight", f"{weight} kg")

else:
    st.info("👉 Please enter a valid name to continue.")
