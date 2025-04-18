import streamlit as st
import pandas as pd
import datetime
import csv
import os
import io

# === Config ===
MOOD_FILE = "mood_log.csv"

# === Function: Load Data ===
def load_mood_data():
    if not os.path.exists(MOOD_FILE):
        return pd.DataFrame(columns=["Date", "Mood"])
    try:
        data = pd.read_csv(MOOD_FILE, names=["Date", "Mood"], header=None)
        return data
    except Exception as e:
        st.error(f"Error reading mood data: {e}")
        return pd.DataFrame(columns=["Date", "Mood"])

# === Function: Save Entry ===
def save_mood_data(date, mood):
    file_exists = os.path.exists(MOOD_FILE)
    is_empty = os.path.getsize(MOOD_FILE) == 0 if file_exists else True

    with open(MOOD_FILE, "a", newline="", encoding="utf-8") as file:  # Add encoding='utf-8'
        writer = csv.writer(file)
        if is_empty:
            writer.writerow(["Date", "Mood"])
        writer.writerow([date, mood])


# === Function: Overwrite All Data (for edit/delete) ===
def overwrite_mood_data(dataframe):
    dataframe.to_csv(MOOD_FILE, index=False, header=False)

# === Theme Styling (Light Theme Always) ===
bg_color = "#F0F2F6"
text_color = "#000000"
box_color = "#ffffff"

st.markdown(f"""
    <style>
    body {{
        background-color: {bg_color};
        color: {text_color};
    }}
    
    .title {{
        font-size: 40px;
        font-weight: bold;
        margin-top: 0;
        
    }}
    .subtitle {{
        font-size: 22px;
        font-weight: 600;
        margin-top: 10px;
    }}
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-box">', unsafe_allow_html=True)

# === Title ===
st.markdown('<div class="title">🔗 Mood Tracker</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">How are you feeling today? 🌟</div>', unsafe_allow_html=True)

# === Mood Input ===
today = datetime.date.today()
mood = st.selectbox("Select your mood", [
    "😊 Happy", "😔 Sad", "👿 Angry", "😐 Neutral", "😃 Excited", "😫 Tired"
])

if st.button("Log Mood 📝"):
    save_mood_data(today, mood)
    st.success("✅ Mood Logged Successfully! 🎉")

# === Load Mood Data ===
data = load_mood_data()

# === Mood Chart ===
if not data.empty:
    st.subheader("📊 Mood Trends")
    try:
        data["Date"] = pd.to_datetime(data["Date"])
        mood_counts = data["Mood"].value_counts()
        st.bar_chart(mood_counts)
    except Exception as e:
        st.error(f"Error processing mood trends: {e}")

# === Mood Editor ===
st.subheader("⚙️ Edit / Delete Logged Moods")

if not data.empty:
    data.reset_index(drop=True, inplace=True)
    delete_indices = []
    for i, row in data.iterrows():
        col1, col2, col3 = st.columns([2, 3, 1])
        with col1:
            st.write(row["Date"].strftime("%Y-%m-%d"))
        with col2:
            new_mood = st.text_input(f"Edit Mood {i}", row["Mood"], key=f"edit_{i}")
        with col3:
            if st.checkbox("Delete ❌", key=f"delete_{i}"):
                delete_indices.append(i)
        data.at[i, "Mood"] = new_mood

    if delete_indices:
        data.drop(index=delete_indices, inplace=True)

    if st.button("💾 Save Changes"):
        overwrite_mood_data(data)
        st.success("✅ Changes Saved! 🎉")
        st.rerun()
else:
    st.info("No mood logs yet. Start by logging how you feel above! ✨")

# === Share Stats Section ===
st.subheader("📤 Share Your Mood Stats")

if not data.empty:
    data["Date"] = pd.to_datetime(data["Date"])
    mood_counts = data["Mood"].value_counts()

    share_text = "🌍 Here's my mood summary:\n"
    for mood, count in mood_counts.items():
        share_text += f"{mood} × {count}\n"
    share_text += "\nLogged with ❤️ using my Mood Tracker!"

    st.text_area("Copy & Share", share_text, height=150)

    csv = data.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="📥 Download CSV",
        data=csv,
        file_name="my_mood_log.csv",
        mime="text/csv",
    )

    txt_data = io.BytesIO(share_text.encode("utf-8"))
    st.download_button(
        label="📤 Download Mood Summary (.txt)",
        data=txt_data,
        file_name="mood_summary.txt",
        mime="text/plain"
    )
else:
    st.info("Log some moods to start sharing your stats! 🗣️")

# === Footer ===
st.markdown("---")
st.markdown("Built with ❤️ by [Laiba Naz](https://github.com/Laiba772)")
st.markdown('</div>', unsafe_allow_html=True)
st.markdown(
    """
    <style>
    footer {
        visibility: hidden;
    }
    </style>
    """,
    unsafe_allow_html=True
)
# === End of Script ===
# This script is a simple mood tracker application built using Streamlit.
# It allows users to log their mood, view trends, edit/delete entries, and share their stats.
