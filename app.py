import os
import streamlit as st
from dotenv import load_dotenv
import requests

# --- Load environment variables ---
load_dotenv()
SUPABASE_URL = os.getenv("supabase_url")
SUPABASE_KEY = os.getenv("supabase_key")

if not SUPABASE_URL or not SUPABASE_KEY:
    st.error(
        "Missing Supabase credentials in .env file.\n"
        "Add these to your .env file and restart:\n"
        "supabase_url=https://your-project-ref.supabase.co\n"
        "supabase_key=your-anon-key"
    )
    st.stop()

SUPABASE_URL = SUPABASE_URL.rstrip("/")
API_URL = f"{SUPABASE_URL}/rest/v1"

HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json",
    "Prefer": "return=representation",
}

# --- Utility Functions ---


def test_connection():
    try:
        response = requests.get(f"{API_URL}/", headers=HEADERS)
        return response.status_code == 200
    except Exception:
        return False


def register_user(username, password):
    data = {"username": username, "password": password}
    try:
        response = requests.post(f"{API_URL}/users", headers=HEADERS, json=data)
        if response.status_code == 201:
            st.success("User registered successfully.")
        elif response.status_code == 409:
            st.error("Username already exists. Try a different one.")
        else:
            st.error(f"Registration failed: {response.text}")
    except Exception as e:
        st.error(f"Error during registration: {e}")


def login_user(username, password):
    try:
        response = requests.get(
            f"{API_URL}/users?username=eq.{username}&password=eq.{password}",
            headers=HEADERS,
        )
        users = response.json() if response.status_code == 200 else []
        return users and len(users) > 0
    except Exception as e:
        st.error(f"Error during login: {e}")
        return False


def get_tasks():
    try:
        response = requests.get(f"{API_URL}/todo", headers=HEADERS)
        return response.json() if response.status_code == 200 else []
    except Exception as e:
        st.error(f"Error displaying tasks: {e}")
        return []


def add_task(task_name):
    try:
        res = requests.post(
            f"{API_URL}/todo",
            headers=HEADERS,
            json={"task": task_name, "status": False},
        )
        return res.status_code == 201
    except Exception:
        return False


def mark_task_done(task_name):
    try:
        res = requests.patch(
            f"{API_URL}/todo?task=eq.{task_name}",
            headers=HEADERS,
            json={"status": True},
        )
        return res.status_code in [200, 204]
    except Exception:
        return False


def delete_task(task_name):
    try:
        res = requests.delete(f"{API_URL}/todo?task=eq.{task_name}", headers=HEADERS)
        return res.status_code in [200, 204]
    except Exception:
        return False


# --- Streamlit UI ---

st.title("Supabase Auth & TODO App")

if not test_connection():
    st.error("Cannot connect to Supabase. Check credentials and network.")
    st.stop()

st.info(
    "Make sure the following tables exist in Supabase:\n"
    "CREATE TABLE IF NOT EXISTS users (\n"
    "    id SERIAL PRIMARY KEY,\n"
    "    username VARCHAR(255) NOT NULL UNIQUE,\n"
    "    password VARCHAR(255) NOT NULL\n"
    ");\n\n"
    "CREATE TABLE IF NOT EXISTS todo (\n"
    "    id SERIAL PRIMARY KEY,\n"
    "    task VARCHAR(255) NOT NULL,\n"
    "    status BOOLEAN NOT NULL DEFAULT FALSE\n"
    ");\n"
    "```"
)

menu = st.sidebar.selectbox(
    "Choose action", ["Register", "Login", "View All Tasks", "Exit"]
)

if menu == "Register":
    st.header("Register New User")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Register"):
        if username and password:
            register_user(username, password)
        else:
            st.warning("Please enter both username and password.")

elif menu == "Login":
    st.header("User Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if login_user(username, password):
            st.success(f"Welcome, {username}!")
            st.subheader("TODO List")

            # Display tasks
            tasks = get_tasks()
            for task in tasks:
                status = "✓ Done" if task["status"] else "○ Pending"
                st.write(f"{task['id']}. [{status}] {task['task']}")

            # Add new task
            st.markdown("---")
            new_task = st.text_input("New Task")
            if st.button("Add Task"):
                if new_task:
                    if add_task(new_task):
                        st.success("Task added.")
                    else:
                        st.error("Failed to add task.")
                else:
                    st.warning("Enter a task name.")

            # Mark as done
            mark_task = st.text_input("Task to mark as done")
            if st.button("Mark as Done"):
                if mark_task:
                    if mark_task_done(mark_task):
                        st.success("Task marked as done.")
                    else:
                        st.error("Failed to mark as done or task not found.")
                else:
                    st.warning("Enter a task name to mark done.")

            # Delete task
            del_task = st.text_input("Task to delete")
            if st.button("Delete Task"):
                if del_task:
                    if delete_task(del_task):
                        st.success("Task deleted.")
                    else:
                        st.error("Failed to delete or not found.")
                else:
                    st.warning("Enter a task name to delete.")
        else:
            st.error("Invalid username or password.")

elif menu == "View All Tasks":
    st.header("All Tasks")
    tasks = get_tasks()
    if tasks:
        for task in tasks:
            status = "✓ Done" if task["status"] else "○ Pending"
            st.write(f"{task['id']}. [{status}] {task['task']}")
    else:
        st.info("No tasks found.")

elif menu == "Exit":
    st.write("Goodbye!")
