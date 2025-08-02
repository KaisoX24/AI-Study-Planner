from groq import Groq
import os
from dotenv import load_dotenv
import streamlit as st
import datetime
import time

# Loading envs
load_dotenv()
client = Groq(
    api_key=os.getenv("GROQ_API_KEY"),
)

# AI logic for study Plan
def chat(days_until_exam, hours_per_day, subject_topic_list, weak_topics):
    prompt = f"""You are an expert study planner assistant. Your task is to help the user prepare for exams by distributing their study topics intelligently over the available days.

        Here is the input:
        - Total days until exam: {days_until_exam}
        - Daily available study hours: {hours_per_day}
        - Subjects and their topics:
        {subject_topic_list}

        The user has marked these topics as weak and should get more revision:
        {weak_topics}

        Now, do the following:
        1. Prioritize the subjects and topics based on importance and weakness.
        2. Suggest how the total study time should be allocated among subjects.
        3. Recommend a study order (which subject to study on which day).
        4. Recommend daily study blocks with break suggestions.

        Respond in a clear, structured format like this:
        ---
        Study Plan Summary:
        1. Priority Order: [Math, Physics, Chemistry, ...]
        2. Allocation of hours: Math - 40%, Physics - 30%, ...

        Example Daily Plan:
        Day 1:
        - 9:00 AM - 10:30 AM: Math - Calculus
        - 10:30 AM - 10:45 AM: Break
        - 10:45 AM - 12:15 PM: Physics - Motion
        ...

        End your response with a motivational line.
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",  
        messages=[
            {
                "role": "system",
                "content": "You are a helpful study planner assistant."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )
    return response.choices[0].message.content

def stream_plan(plan):
    full_text = ""
    placeholder = st.empty()
    for char in plan:
        full_text += char
        placeholder.markdown(full_text)
        time.sleep(0.01)


st.set_page_config(
    page_title='Study Planner',
    page_icon='📚',
    layout='centered',
)

st.title("🧠 AI Study Planner")
st.subheader('📆 Plan your exam prep with AI')

st.sidebar.header('Setup Your Study Plan')

exam_date = st.sidebar.date_input("🗓️ Exam Date",min_value=datetime.date.today())
study_hours = st.sidebar.slider("⏳ Daily Study Hours", 1, 12, 4)

subject_input = st.sidebar.text_area(
    '📚 Subjects and Topics',
    height=150,
    placeholder='Example:\nMath: Calculus, Algebra\nPhysics: Motion, Thermodynamics'
)

weak_input = st.sidebar.text_area(
    '⚠️ Weak Topics',
    placeholder='Example:\nCalculus\nThermodynamics'
)

delta_days = (exam_date - datetime.date.today()).days
if delta_days < 1:
    st.error("⚠️ Please select a future exam date (at least tomorrow).")
    st.stop()


if st.sidebar.button("🚀 Generate Study Plan"):
    with st.spinner("Generating your personalized plan..."):
        plan = chat(
            delta_days,
            study_hours,
            subject_input,
            weak_input
        )
        st.success("✅ Plan Generated!")
        stream_plan(plan)

        st.download_button("⬇️ Download Plan", plan, file_name="study_plan.txt")