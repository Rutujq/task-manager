import streamlit as st
import pandas as pd
from datetime import date
from api_service import get_tasks, add_task, delete_task, update_task, search_tasks

# ---------------- UI SETTINGS ----------------
st.markdown("""
<style>

/* 🌸 Background */
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #ff4d6d, #ff8fa3, #ffccd5);
}

/* 🪟 Glass container */
.main .block-container {
    background: rgba(255, 255, 255, 0.10);
    backdrop-filter: blur(16px);
    border-radius: 18px;
    padding: 2rem;
}

/* ✨ Default text */
html, body, [class*="css"] {
    color: white;
}

/* 🔲 Inputs */
input, textarea, select {
    background: rgba(255,255,255,0.8) !important;
    color: black !important;   /* ✅ TEXT BLACK */
    border: 1px solid rgba(0,0,0,0.2) !important;
    border-radius: 10px !important;
}

/* 🟡 Placeholder */
input::placeholder, textarea::placeholder {
    color: rgba(0,0,0,0.6) !important;
}

/* 📊 Table */
[data-testid="stDataFrame"] {
    background: #ffffff !important;
    border-radius: 10px;
}

/* Table text */
table {
    color: #000 !important;
}

/* 🔘 Button */
.stButton > button {
    background: linear-gradient(90deg, #ff4d6d, #ff8fa3);
    color: black;
    border-radius: 10px;
}

</style>
""", unsafe_allow_html=True)

# ---------------- TITLE ----------------
st.title("🚀 Task Manager Dashboard")

# ---------------- LOAD ----------------
if "tasks" not in st.session_state:
    st.session_state.tasks = get_tasks()

# ---------------- ADD TASK ----------------
st.markdown('<div class="glass">', unsafe_allow_html=True)
st.markdown("## ➕ Add Task")

with st.form("task_form"):
    col1, col2 = st.columns(2)

    with col1:
        title = st.text_input("Title")

    with col2:
        description = st.text_area("Description")

    col3, col4 = st.columns(2)

    with col3:
        due_date = st.date_input("Due Date", min_value=date.today())

    with col4:
        priority = st.selectbox("Priority", ["Low", "Medium", "High"])

    if st.form_submit_button("Add Task"):
        if title:
            add_task(title, description, str(due_date), priority)
            st.success("Task Added")
            st.session_state.tasks = get_tasks()
        else:
            st.error("Enter Title")

st.markdown('</div>', unsafe_allow_html=True)

# ---------------- SEARCH ----------------
st.markdown('<div class="glass">', unsafe_allow_html=True)

st.markdown("## 🔍 Search")

keyword = st.text_input("Search by title")

if keyword:
    tasks = search_tasks(keyword)
else:
    tasks = get_tasks()

st.markdown('</div>', unsafe_allow_html=True)

# ---------------- DISPLAY ----------------
st.markdown('<div class="glass">', unsafe_allow_html=True)

st.markdown("## 📋 Tasks")

if tasks:
    df = pd.DataFrame(tasks)
    st.dataframe(df, use_container_width=True)

    # ---------------- DELETE ----------------
    st.markdown("## 🗑️ Delete Task")

    titles = [f"{i} - {t['title']}" for i, t in enumerate(tasks)]
    selected = st.selectbox("Select Task", titles)

    if st.button("Delete"):
        index = int(selected.split(" - ")[0])
        delete_task(index)
        st.success("Deleted")
        st.session_state.tasks = get_tasks()

    # ---------------- UPDATE ----------------
    st.markdown("## ✏️ Update Task")

    selected_update = st.selectbox("Select Task to Update", titles)

    new_title = st.text_input("New Title")
    new_desc = st.text_area("New Description")
    new_due = st.date_input("New Due Date")
    new_priority = st.selectbox("New Priority", ["Low", "Medium", "High"])

    if st.button("Update"):
        if new_title:
            index = int(selected_update.split(" - ")[0])
            update_task(index, new_title, new_desc, str(new_due), new_priority)
            st.success("Updated")
            st.session_state.tasks = get_tasks()
        else:
            st.error("Enter Title")

else:
    st.info("No tasks available")


st.markdown('</div>', unsafe_allow_html=True)
