
import streamlit as st
import pandas as pd
import datetime
import matplotlib.pyplot as plt

st.set_page_config(page_title="BulkUp", layout="centered")

# Session state for user inputs
if 'step' not in st.session_state:
    st.session_state.step = 0

st.markdown("<h2 style='text-align:center;'>💪 Welcome to BulkUp</h2>", unsafe_allow_html=True)
st.markdown("---")

# Step-by-step onboarding
if st.session_state.step == 0:
    st.subheader("🎯 What's your primary goal?")
    goal = st.radio("Choose one:", ["Gain Weight", "Build Muscle", "Both"])
    if st.button("Next"):
        st.session_state.goal = goal
        st.session_state.step += 1

elif st.session_state.step == 1:
    st.subheader("📍 Let's learn more about you")
    gender = st.radio("Gender", ["Male", "Female", "Other"])
    age = st.number_input("Age", min_value=10, max_value=80, step=1)
    activity = st.selectbox("Activity Level", ["Sedentary", "Lightly Active", "Active", "Very Active"])
    if st.button("Next"):
        st.session_state.gender = gender
        st.session_state.age = age
        st.session_state.activity = activity
        st.session_state.step += 1

elif st.session_state.step == 2:
    st.subheader("📊 Current Stats")
    current_weight = st.number_input("Current Weight (kg)", min_value=20.0, max_value=200.0, step=0.5)
    target_weight = st.number_input("Target Weight (kg)", min_value=current_weight+1, max_value=300.0, step=0.5)
    st.session_state.current_weight = current_weight
    st.session_state.target_weight = target_weight
    if st.button("Finish Setup"):
        st.session_state.step += 1

elif st.session_state.step == 3:
    st.success("🎉 Your Personalized Bulking Plan is Ready!")
    st.markdown("---")

    st.subheader("🏋️ Workout Plan")
    st.write("Based on your input, here’s a simple weekly plan:")
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    workouts = [
        "Push Day (Chest, Shoulders, Triceps)",
        "Pull Day (Back, Biceps)",
        "Leg Day (Squats, Lunges)",
        "Core + Cardio",
        "Full Body Strength",
        "Active Recovery / Stretching",
        "Rest"
    ]
    for d, w in zip(days, workouts):
        st.write(f"**{d}:** {w}")
    st.markdown("---")

    st.subheader("📈 Track Your Weight")
    if 'weights' not in st.session_state:
        st.session_state.weights = []
        st.session_state.dates = []

    new_weight = st.number_input("Log Today's Weight (kg)", min_value=20.0, max_value=200.0, step=0.5, key="log_weight")
    if st.button("Add Weight"):
        st.session_state.weights.append(new_weight)
        st.session_state.dates.append(datetime.date.today())

    if st.session_state.weights:
        df = pd.DataFrame({"Date": st.session_state.dates, "Weight": st.session_state.weights})
        fig, ax = plt.subplots(figsize=(5, 3))
        ax.plot(df['Date'], df['Weight'], marker='o')
        ax.set_title("Progress Over Time")
        ax.set_xlabel("Date")
        ax.set_ylabel("Weight (kg)")
        st.pyplot(fig)

    st.markdown("---")

    st.subheader("🍽️ Calorie Estimator")
    st.write("Type what you ate today and we’ll estimate your calories.")

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

    meal = st.text_area("What did you eat? (e.g. 2 eggs, banana, toast)")
    if st.button("Estimate Calories"):
        if meal.strip():
            total, breakdown = estimate_calories(meal)
            st.success(f"Estimated total: {total} kcal")
            for item in breakdown:
                st.write(f"- {item}")
        else:
            st.warning("Please enter your meal.")

    st.markdown("---")

    st.subheader("📚 Tips for Bulking Success")
    st.markdown("""
    - Eat calorie-dense meals consistently
    - Train with progressive overload 3–5x/week
    - Prioritize protein in every meal
    - Track progress weekly
    - Stay patient. Muscle takes time!
    """)
