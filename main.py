import streamlit as st
import pandas as pd
import datetime
import matplotlib.pyplot as plt

st.set_page_config(page_title="BulkUp", layout="centered")

if 'weights' not in st.session_state:
    st.session_state.weights = []
if 'dates' not in st.session_state:
    st.session_state.dates = []

st.markdown("<h2 style='text-align:center;'>💪 Welcome to BulkUp</h2>", unsafe_allow_html=True)
st.markdown("---")

with st.form("onboarding"):
    st.subheader("🎯 Let's set your goal")
    name = st.text_input("Name")
    age = st.number_input("Age", min_value=10, max_value=80, step=1)
    current_weight = st.number_input("Current Weight (kg)", min_value=20.0, max_value=200.0, step=0.5)
    target_weight = st.number_input("Target Weight (kg)", min_value=current_weight+1, max_value=300.0, step=0.5)
    goal = st.radio("Primary Goal", ["Gain Weight", "Build Muscle", "Both"])
    submitted = st.form_submit_button("Continue")

if submitted:
    st.success(f"Welcome {name}! Let's bulk up smartly.")
    st.markdown("---")

    st.subheader("🏋️ Training Plan")
    train_type = st.radio("Preferred Training Type", ["Home Workouts", "Gym Workouts"])

    plans = {
        "Home Workouts": [
            ("Monday", "Full Body (Pushups, Squats, Planks)"),
            ("Tuesday", "Rest or Light Cardio"),
            ("Wednesday", "Upper Body (Chair Dips, Pike Pushups)"),
            ("Thursday", "Leg Day (Lunges, Calf Raises)"),
            ("Friday", "Full Body HIIT"),
            ("Saturday", "Core Blast (Planks, Leg Raises)"),
            ("Sunday", "Rest")
        ],
        "Gym Workouts": [
            ("Monday", "Push (Bench Press, Shoulder Press)"),
            ("Tuesday", "Pull (Deadlifts, Rows)"),
            ("Wednesday", "Legs (Squats, Lunges)"),
            ("Thursday", "Core & Cardio"),
            ("Friday", "Full Body Strength"),
            ("Saturday", "Active Recovery or Rest"),
            ("Sunday", "Rest")
        ]
    }

    for day, workout in plans[train_type]:
        st.write(f"**{day}:** {workout}")
    st.markdown("---")

    st.subheader("📈 Weight Progress Tracker")
    today = datetime.date.today()
    new_weight = st.number_input("Log Today's Weight (kg)", min_value=20.0, max_value=200.0, step=0.5, key="log_weight")
    if st.button("Add Entry"):
        st.session_state.weights.append(new_weight)
        st.session_state.dates.append(today)

    if st.session_state.weights:
        df = pd.DataFrame({"Date": st.session_state.dates, "Weight": st.session_state.weights})
        fig, ax = plt.subplots(figsize=(5, 3))
        ax.plot(df['Date'], df['Weight'], marker='o')
        ax.set_title("Weight Over Time")
        ax.set_ylabel("Weight (kg)")
        ax.set_xlabel("Date")
        st.pyplot(fig)

    st.markdown("---")

    st.subheader("🍽️ Calorie Tracker")
    st.write("Type what you ate today. We'll estimate the calories.")

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

    meal = st.text_area("What did you eat? (e.g. 2 eggs, banana, toast, milk)")
    if st.button("Estimate Calories"):
        if meal.strip():
            total, breakdown = estimate_calories(meal)
            st.success(f"Estimated total: {total} kcal")
            for item in breakdown:
                st.write(f"- {item}")
        else:
            st.warning("Please enter your meal.")

    st.markdown("---")
    st.subheader("📚 Bulking Tips")
    st.markdown("""
    - Eat calorie-dense, high-protein meals
    - Train 3–5x/week with progressive overload
    - Get 7–9 hours of sleep per night
    - Track weight weekly
    - Be consistent – gains take time!
    """)