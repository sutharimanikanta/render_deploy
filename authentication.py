import os
from getpass import getpass
from dotenv import load_dotenv
import requests

# Load environment variables
load_dotenv()

print("Script started!")

# Get Supabase credentials from .env
SUPABASE_URL = os.getenv("supabase_url")
SUPABASE_KEY = os.getenv("supabase_key")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError(
        "Missing Supabase credentials in .env file\n"
        "Add these to your .env file:\n"
        "supabase_url=https://your-project-ref.supabase.co\n"
        "supabase_key=your-anon-key"
    )

# Remove trailing slash if present
SUPABASE_URL = SUPABASE_URL.rstrip("/")
API_URL = f"{SUPABASE_URL}/rest/v1"

# Headers for API requests
HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json",
    "Prefer": "return=representation",
}


def test_connection():
    """Test connection to Supabase"""
    try:
        response = requests.get(f"{API_URL}/", headers=HEADERS)
        if response.status_code == 200:
            print("✓ Successfully connected to Supabase!")
            return True
        else:
            print(f"✗ Connection failed with status code: {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Failed to connect to Supabase: {e}")
        return False


def setup():
    """Create tables using Supabase SQL editor or dashboard"""
    print("\n⚠ Note: Please create these tables in Supabase SQL Editor:")
    print("""
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        username VARCHAR(255) NOT NULL UNIQUE,
        password VARCHAR(255) NOT NULL
    );

    CREATE TABLE IF NOT EXISTS todo (
        id SERIAL PRIMARY KEY,
        task VARCHAR(255) NOT NULL,
        status BOOLEAN NOT NULL DEFAULT FALSE
    );
    """)
    print("\nGo to: Supabase Dashboard > SQL Editor > New Query")
    input("Press Enter after creating the tables...")


def reg():
    """Register a new user"""
    username = input("Enter username: ")
    password = getpass("Enter password: ")

    data = {"username": username, "password": password}

    try:
        response = requests.post(f"{API_URL}/users", headers=HEADERS, json=data)

        if response.status_code == 201:
            print("✓ User registered successfully.")
        elif response.status_code == 409:
            print("✗ Username already exists. Please choose a different username.")
        else:
            print(f"✗ Registration failed: {response.text}")
    except Exception as e:
        print(f"✗ Error during registration: {e}")


def todolist():
    """Manage todo list after login"""

    # Display all tasks
    try:
        response = requests.get(f"{API_URL}/todo", headers=HEADERS)

        if response.status_code == 200:
            tasks = response.json()
            if tasks:
                print("\n" + "=" * 50)
                print("TODO LIST")
                print("=" * 50)
                for task in tasks:
                    status = "✓ Done" if task["status"] else "○ Pending"
                    print(f"{task['id']}. [{status}] {task['task']}")
                print("=" * 50)
            else:
                print("\nNo tasks found in the todo list.")
        else:
            print(f"✗ Error fetching tasks: {response.text}")
    except Exception as e:
        print(f"✗ Error displaying tasks: {e}")

    # Add new task
    action = input("\nDo you want to add a new task? (yes/no): ").strip().lower()
    if action in ["yes", "y"]:
        task_name = input("Enter the task: ")
        try:
            response = requests.post(
                f"{API_URL}/todo",
                headers=HEADERS,
                json={"task": task_name, "status": False},
            )
            if response.status_code == 201:
                print("✓ Task added successfully.")
            else:
                print(f"✗ Error adding task: {response.text}")
        except Exception as e:
            print(f"✗ Error: {e}")

    # Mark task as done
    mark_done = input("Do you want to mark a task as done? (yes/no): ").strip().lower()
    if mark_done in ["yes", "y"]:
        task_to_mark = input("Enter the task to mark as done: ")
        try:
            response = requests.patch(
                f"{API_URL}/todo?task=eq.{task_to_mark}",
                headers=HEADERS,
                json={"status": True},
            )
            if response.status_code == 200 or response.status_code == 204:
                print("✓ Task marked as done.")
            else:
                print(f"✗ Task not found or error: {response.text}")
        except Exception as e:
            print(f"✗ Error: {e}")

    # Delete task
    delete_action = input("Do you want to delete a task? (yes/no): ").strip().lower()
    if delete_action in ["yes", "y"]:
        task_to_delete = input("Enter the task to delete: ")
        try:
            response = requests.delete(
                f"{API_URL}/todo?task=eq.{task_to_delete}", headers=HEADERS
            )
            if response.status_code == 200 or response.status_code == 204:
                print("✓ Task deleted successfully.")
            else:
                print(f"✗ Task not found or error: {response.text}")
        except Exception as e:
            print(f"✗ Error: {e}")


def login():
    """Login user"""
    username = input("Enter username: ")
    password = getpass("Enter password: ")

    try:
        response = requests.get(
            f"{API_URL}/users?username=eq.{username}&password=eq.{password}",
            headers=HEADERS,
        )

        if response.status_code == 200:
            users = response.json()
            if users and len(users) > 0:
                print(f"✓ Login successful. Welcome, {username}!")
                todolist()
            else:
                print("✗ Invalid username or password.")
        else:
            print(f"✗ Error during login: {response.text}")
    except Exception as e:
        print(f"✗ Error during login: {e}")


def display_tasks():
    """Display all tasks"""
    try:
        response = requests.get(f"{API_URL}/todo", headers=HEADERS)

        if response.status_code == 200:
            tasks = response.json()
            if tasks:
                print("\n" + "=" * 50)
                print("ALL TASKS")
                print("=" * 50)
                for task in tasks:
                    status = "✓ Done" if task["status"] else "○ Pending"
                    print(f"{task['id']}. [{status}] {task['task']}")
                print("=" * 50)
            else:
                print("\n✗ No tasks found.")
        else:
            print(f"✗ Error fetching tasks: {response.text}")
    except Exception as e:
        print(f"✗ Error displaying tasks: {e}")


def main_menu():
    """Main application menu"""
    if not test_connection():
        print("\n✗ Cannot proceed without Supabase connection.")
        print("\nPlease check your .env file:")
        print("supabase_url=https://your-project-ref.supabase.co")
        print("supabase_key=your-anon-key")
        return

    print("\n" + "=" * 50)
    print("WELCOME TO THE AUTHENTICATION SYSTEM")
    print("=" * 50)

    # Check if tables exist
    check = (
        input("\nHave you created the 'users' and 'todo' tables? (yes/no): ")
        .strip()
        .lower()
    )
    if check not in ["yes", "y"]:
        setup()

    while True:
        print("\n--- Main Menu ---")
        print("1. Register")
        print("2. Login")
        print("3. View All Tasks")
        print("4. Exit")
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            reg()
        elif choice == "2":
            login()
        elif choice == "3":
            display_tasks()
        elif choice == "4":
            print("\n✓ Exiting... Goodbye!")
            break
        else:
            print("✗ Invalid choice. Please try again.")


if __name__ == "__main__":
    main_menu()
    print("\nApplication ended.")
