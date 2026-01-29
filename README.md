# ☁️ Cloud-Backed Authentication & Task Management System
### REST API–Driven Login & To-Do Application using Supabase

This project demonstrates how to build a **working login and task management system** using a **managed backend (Supabase)** — without writing a custom backend server.

The system uses **Supabase PostgREST APIs** to interact directly with a cloud-hosted PostgreSQL database and supports **multiple clients**.

---

## 🧠 Core Problem Solved

> How can I build authentication and task management using a cloud backend and REST APIs — without maintaining my own backend server?

This project explores:
- Backend-as-a-Service (BaaS)
- REST-based database access
- Multi-client application design

---

## 🧩 High-Level Architecture


---

## 🖥️ Client Implementations

### 🟢 Streamlit Web Application
- Interactive UI
- Sidebar navigation
- Forms for login and task actions
- REST API integration

### 🟢 Python CLI Application
- Terminal-based interface
- Secure password input (`getpass`)
- Supports login and full CRUD operations
- Reuses the same Supabase backend

> Supporting both web and CLI clients demonstrates **backend-first thinking**.

---

## 🧠 Key Technical Components

### 1️⃣ Database Design (Basic but Correct)

**Database:** PostgreSQL (Supabase)

**Tables:**
- `users(id, username, password)`
- `todo(id, task, status)`

✔ Primary keys  
✔ Unique constraints  
✔ Boolean status field  

❌ No user–task relationship (no foreign key mapping)

> This is a **beginner-level schema**, sufficient for learning REST and cloud DB interaction.

---

### 2️⃣ Backend Style — BaaS (Supabase)

- Uses **Supabase PostgREST**
- Interacts via REST APIs
- Performs CRUD operations using:
  - `GET`
  - `POST`
  - `PATCH`
  - `DELETE`
- Authenticated using Supabase **anon API key**

This demonstrates:
- Understanding of RESTful APIs
- Comfort with managed cloud databases
- Backend-less application architecture

❌ No Row Level Security (RLS)  
❌ No role-based access control  

---

### 3️⃣ Authentication Logic (Demo-Level)

Authentication is implemented via:

```sql
SELECT * FROM users
WHERE username = X AND password = Y
