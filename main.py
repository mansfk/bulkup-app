import streamlit as st
import pandas as pd
import datetime
import matplotlib.pyplot as plt

# Page config
st.set_page_config(
    page_title="BulkUp",
    page_icon=None,
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Hide Streamlit branding
hide_st_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
"""
st.markdown(hide_st_style, unsafe_allow_html=True)

st.markdown("<h2 style='text-align:center;'>💪 BulkUp: Your Fitness Tracker</h2>", unsafe_allow_html=True)
st.markdown("📱 Tip: On your phone, tap 'Share' or '⋮' → 'Add to Home Screen' to install BulkUp like an app!")

# Navigation logic
if 'unlocked' not in st.session_state:
    st.session_state.unlocked = False
page = st.radio("Navigate", ["🏠 Onboarding", "📈 Progress", "🍽️ Meals", "📚 Tips"], horizontal=True)
st.markdown("---")

if 'weights' not in st.session_state:
    st.session_state.weights = []
if 'dates' not in st.session_state:
    st.session_state.dates = []

if page == "🏠 Onboarding":
    st.subheader("🎯 Personalized Setup")
    with st.form("onboarding"):
        goal = st.radio("Primary Goal", ["Gain Weight", "Build Muscle", "Both"])
        gender = st.radio("Gender", ["Male", "Female", "Other"])
        age = st.number_input("Age", min_value=10, max_value=80, value=18, step=1)
        activity = st.selectbox("How often do you exercise per week?", [
    "0 days (Sedentary)",
    "1–2 days (Light)",
    "3–4 days (Moderate)",
    "5–6 days (Heavy)",
    "7 days (Very intense)"])
        current_weight = st.number_input("Current Weight (kg)", min_value=30.0, max_value=200.0, value=70.0, step=0.5)
        target_weight = st.number_input("Target Weight (kg)", min_value=current_weight+1, max_value=300.0, value=current_weight+5, step=0.5)
        submitted = st.form_submit_button("Create Plan")

    if submitted:
        st.session_state.unlocked = False  # reset access
        st.success("🎉 Your plan is ready!")
        st.markdown("We’ve created your personalized bulking plan. Tap below to unlock it.")
        if st.button("Start 7-Day Free Trial"):
            st.session_state.unlocked = True
            st.experimental_rerun()

elif page == "📈 Progress":
    if not st.session_state.unlocked:
        st.warning("🔒 Unlock your personalized plan through onboarding.")
    else:
        st.subheader("📊 Track Your Weight")
        new_weight = st.number_input("Log Today's Weight (kg)", min_value=30.0, max_value=200.0, value=70.0, step=0.5)
        if st.button("Add Weight"):
            st.session_state.weights.append(new_weight)
            st.session_state.dates.append(datetime.date.today())

        if st.session_state.weights:
            df = pd.DataFrame({"Date": st.session_state.dates, "Weight": st.session_state.weights})
            start_weight = st.session_state.weights[0]
            latest_weight = st.session_state.weights[-1]
            gain = latest_weight - start_weight
            st.success(f"You’ve gained {gain:.1f} kg since starting.")

            fig, ax = plt.subplots(figsize=(5, 3))
            ax.plot(df['Date'], df['Weight'], marker='o')
            ax.set_title("Weight Progress")
            ax.set_xlabel("Date")
            ax.set_ylabel("Weight (kg)")
            st.pyplot(fig)

elif page == "🍽️ Meals":
    if not st.session_state.unlocked:
        st.warning("🔒 Unlock your personalized plan through onboarding.")
    else:
        st.subheader("🍴 Calorie Estimator")
        st.write("Type your meals below:")

        FOOD_CALORIES = {
            "egg": 70,
            "banana": 105,
            "toast": 100,
            "milk": 150,
            "chicken breast": 165,
            "rice": 200,
            "apple": 95,
            "protein shake": 250,
            "oats": 150,
            "peanut butter": 180,
            "beef": 250
        }

        def estimate_calories(text):
            total = 0
            breakdown = []
            for food, cal in FOOD_CALORIES.items():
                count = text.lower().count(food)
                if count:
                    breakdown.append(f"{food} x{count} = {cal * count} kcal")
                    total += cal * count
            return total, breakdown

        meal = st.text_area("e.g. 2 eggs, banana, toast")
        if st.button("Estimate Calories"):
            if meal.strip():
                total, breakdown = estimate_calories(meal)
                st.success(f"Estimated total: {total} kcal")
                for item in breakdown:
                    st.write(f"- {item}")
            else:
                st.warning("Please enter your meal.")

elif page == "📚 Tips":
    st.subheader("📘 Bulking Tips")
    st.markdown("""
    - Eat calorie-dense meals consistently  
    - Train with progressive overload 3–5x/week  
    - Prioritize protein in every meal  
    - Track your weight weekly  
    - Be patient — real muscle takes time  
    - Sleep 7–9 hours per night  
    """)
  
