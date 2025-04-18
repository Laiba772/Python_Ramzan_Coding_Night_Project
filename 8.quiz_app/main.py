import streamlit as st
import random
import time
import pandas as pd

# Set the page configuration
st.set_page_config(
    page_title="Python Quiz Application",  # Page title
    page_icon="🐍",                          # Page icon (you can also use URLs to images)
    layout="centered",                       # Layout style, you can change to "wide" if you want
    initial_sidebar_state="auto"             # Sidebar state (if you use a sidebar)
)

st.title("🐍 Python Quiz Application ⏱️")

# Python questions
questions = [
    {
        "question": "What is the correct file extension for Python files?",
        "options": [".pyth", ".pt", ".py", ".pyt"],
        "answer": ".py",
    },
    {
        "question": "Which keyword is used to create a function in Python?",
        "options": ["func", "def", "function", "define"],
        "answer": "def",
    },
    {
        "question": "How do you insert comments in Python code?",
        "options": ["// comment", "/* comment */", "# comment", "-- comment"],
        "answer": "# comment",
    },
    {
        "question": "What will `print(2 ** 3)` output?",
        "options": ["6", "8", "9", "5"],
        "answer": "8",
    },
    {
        "question": "What data type is the result of `3 / 2` in Python 3?",
        "options": ["int", "float", "str", "bool"],
        "answer": "float",
    },
    {
        "question": "How do you start a for loop in Python?",
        "options": ["for(i=0;i<5;i++)", "foreach i in range(5)", "for i in range(5):", "loop i from 1 to 5"],
        "answer": "for i in range(5):",
    },
    {
        "question": "Which of the following is a valid variable name in Python?",
        "options": ["2value", "value_2", "value-2", "value 2"],
        "answer": "value_2",
    },
    {
        "question": "What does the `len()` function do?",
        "options": ["Returns the length", "Converts to int", "Returns type", "Prints output"],
        "answer": "Returns the length",
    },
    {
        "question": "What is the output of `bool([])`?",
        "options": ["True", "False", "None", "Error"],
        "answer": "False",
    },
    {
        "question": "What keyword is used to define a class in Python?",
        "options": ["define", "struct", "class", "object"],
        "answer": "class",
    },
]

# Session state init
if "score" not in st.session_state:
    st.session_state.score = 0
if "asked_questions" not in st.session_state:
    st.session_state.asked_questions = []
if "wrong_answers" not in st.session_state:
    st.session_state.wrong_answers = []
if "start_time" not in st.session_state:
    st.session_state.start_time = time.time()
if "current_question" not in st.session_state or st.session_state.current_question is None:
    remaining = [q for q in questions if q not in st.session_state.asked_questions]
    st.session_state.current_question = random.choice(remaining)
    st.session_state.start_time = time.time()

TIMER_DURATION = 10  # seconds

# Quiz Finished
if len(st.session_state.asked_questions) == len(questions):
    st.success(f"🎉 Quiz Completed! Your Score: {st.session_state.score} / {len(questions)}")

    # Show wrong answers
    if st.session_state.wrong_answers:
        st.subheader("❌ Questions You Got Wrong:")
        for wa in st.session_state.wrong_answers:
            st.markdown(f"""
            - **Q:** {wa['question']}  
              **Your Answer:** {wa['your_answer']}  
              **Correct Answer:** {wa['correct_answer']}
            """)

    # CSV Export
    data = []
    for q in st.session_state.asked_questions:
        user_answer = next((w["your_answer"] for w in st.session_state.wrong_answers if w["question"] == q["question"]), q["answer"])
        correct = user_answer == q["answer"]
        data.append({
            "Question": q["question"],
            "Your Answer": user_answer,
            "Correct Answer": q["answer"],
            "Correct?": "✅" if correct else "❌"
        })

    df = pd.DataFrame(data)
    st.download_button("📅 Download Results as CSV", df.to_csv(index=False), file_name="quiz_results.csv", mime="text/csv")

    if st.button("🔁 Restart Quiz"):
        st.session_state.score = 0
        st.session_state.asked_questions = []
        st.session_state.wrong_answers = []
        st.session_state.current_question = None
        st.session_state.start_time = time.time()
        st.rerun()

else:
    # Get the current question and display the question number
    q = st.session_state.current_question
    question_number = len(st.session_state.asked_questions) + 1
    st.subheader(f"Q{question_number}: {q['question']}")  # Display question with its number
    selected_option = st.radio("Choose your answer", q["options"], key=q["question"])

    elapsed = int(time.time() - st.session_state.start_time)
    remaining = max(TIMER_DURATION - elapsed, 0)
    st.warning(f"⏰ Time Remaining: {remaining} seconds")

    submit = st.button("Submit Answer")

    if remaining == 0 or submit:
        if remaining == 0 and not submit:
            st.warning("⏱️ Time's up! Auto-submitting the question.")

        if selected_option == q["answer"]:
            st.success("✅ Correct!")
            st.session_state.score += 1
        else:
            st.error(f"❌ Incorrect! The correct answer is {q['answer']}")
            st.session_state.wrong_answers.append({
                "question": q["question"],
                "your_answer": selected_option,
                "correct_answer": q["answer"]
            })

        st.session_state.asked_questions.append(q)
        time.sleep(2)

        # New Question
        remaining_qs = [q for q in questions if q not in st.session_state.asked_questions]
        if remaining_qs:
            st.session_state.current_question = random.choice(remaining_qs)
            st.session_state.start_time = time.time()
        else:
            st.session_state.current_question = None
        st.rerun()
    else:
        time.sleep(1)
        st.rerun()


# End of the code
# Note: This code is designed to be run in a Streamlit environment.
# Make sure to run this code in a Streamlit app using streamlit run main.py
# to see the quiz application in action.
# The code includes a timer, score tracking, and the ability to download results as a CSV file.
# The quiz will end when all questions have been answered, and the user will be able to see their score and the questions they got wrong.
# The code also includes a restart button to allow users to retake the quiz.
# The quiz questions are stored in a list of dictionaries, each containing the question, options, and the correct answer.
# The session state is used to keep track of the user's score, asked questions, wrong answers, and the current question.
# The quiz is interactive, with radio buttons for answer selection and a submit button to check the answer.
# The timer is implemented using the time module, and the remaining time is displayed to the user.
# The code is structured to provide a smooth user experience, with appropriate feedback for correct and incorrect answers.
# The quiz is designed to be fun and educational, helping users test their knowledge of Python programming.
# The code is modular and can be easily extended with more questions or features.
# The quiz is a great way to learn Python and improve programming skills.
# The code is well-commented and easy to understand, making it suitable for beginners and experienced programmers alike.
# The quiz can be customized with different themes, styles, and layouts to enhance the user experience.
# The code is designed to be user-friendly and engaging, with a focus on providing a positive learning experience.