import streamlit as st
import google.generativeai as genai
import os

from dotenv import load_dotenv
# --- 1. SETTING UP GOOGLE API KEY ---

# This loads the variables from .env into the environment
load_dotenv()

                
GOOGLE_API_KEY =  os.getenv("API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-2.5-flash')

# --- 2. DEFINE PROMPT TEMPLATES ---
def get_nutrition_insights_prompt(food_items):
    return f"""
    Act as an expert Nutritionist. Analyze the following list of food items: {food_items}.
    For each item, provide:
    1. Calorie count.
    2. Macronutrients (Protein, Fats, Carbs in grams).
    3. Key Micronutrients (Vitamins/Minerals).
    4. A brief "Health Verdict" (e.g., 'High in fiber, good for digestion').
    Format the output as a clean, readable report with bold headings.
    """

def get_meal_plan_prompt(profile):
    return f"""
    Create a personalized 7-day meal plan based on the following user profile:
    - Restrictions/Allergies: {profile['restrictions']}
    - Health Goals: {profile['goals']}
    - Activity Level: {profile['activity']}
    - Taste Preferences: {profile['tastes']}
    
    Include a daily breakfast, lunch, dinner, and one snack. 
    Also, provide a consolidated grocery list at the end. 
    Ensure the plan is nutritionally balanced and varied.
    """

def get_coaching_prompt(user_query):
    return f"""
    You are a Virtual Nutrition Coach. A user has the following question: "{user_query}"
    Provide a supportive, scientifically-backed, and easy-to-understand answer. 
    Encourage sustainable lifestyle changes rather than quick fixes.
    """

# --- 3. BUILD STREAMLIT USER INTERFACE ---
st.set_page_config(page_title="NutriGen: AI Nutrition Science", layout="wide")

st.title("🥗 NutriGen: Advancing Nutrition Science")
st.markdown("---")

# Sidebar for Navigation
option = st.sidebar.radio(
    "Choose a Feature",
    ("Dynamic Nutritional Insights", "Tailored Meal Planning", "Virtual Nutrition Coaching")
)

# --- SCENARIO 2: DYNAMIC NUTRITIONAL INSIGHTS ---
if option == "Dynamic Nutritional Insights":
    st.header("🔍 Food Analysis & Insights")
    food_input = st.text_area("Enter food items (e.g., 2 eggs, 1 avocado, 100g grilled chicken):")
    
    if st.button("Analyze Nutrition"):
        if food_input:
            with st.spinner("Analyzing nutrients..."):
                prompt = get_nutrition_insights_prompt(food_input)
                response = model.generate_content(prompt)
                st.success("Analysis Complete!")
                st.markdown(response.text)
        else:
            st.warning("Please enter some food items first.")

# --- SCENARIO 1: TAILORED MEAL PLANNING ---
elif option == "Tailored Meal Planning":
    st.header("📅 Personalized 7-Day Meal Plan")
    
    col1, col2 = st.columns(2)
    with col1:
        restrictions = st.text_input("Allergies/Restrictions (e.g., Vegan, Gluten-free)")
        goals = st.selectbox("Primary Goal", ["Weight Loss", "Muscle Gain", "Maintenance", "Better Energy"])
    with col2:
        activity = st.select_slider("Activity Level", options=["Sedentary", "Moderate", "Very Active"])
        tastes = st.text_input("Favorite Cuisines (e.g., Mediterranean, Indian)")

    if st.button("Generate My Plan"):
        profile = {
            "restrictions": restrictions,
            "goals": goals,
            "activity": activity,
            "tastes": tastes
        }
        with st.spinner("Crafting your custom plan..."):
            prompt = get_meal_plan_prompt(profile)
            response = model.generate_content(prompt)
            st.markdown(response.text)

# --- SCENARIO 3: VIRTUAL NUTRITION COACHING ---
elif option == "Virtual Nutrition Coaching":
    st.header("💬 Talk to your Nutrition Coach")
    user_query = st.text_input("Ask anything (e.g., 'How can I get more protein as a vegan?')")
    
    if st.button("Ask Coach"):
        if user_query:
            with st.spinner("Consulting AI Coach..."):
                prompt = get_coaching_prompt(user_query)
                response = model.generate_content(prompt)
                st.info("Coach's Advice:")
                st.write(response.text)
        else:
            st.warning("Please ask a question.")