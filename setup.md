# 🎬 MovieMaking App – Local Dev Setup Guide
### Welcome! Let’s get your local development environment up and running in no time. Grab your ☕ and follow the steps below 👇

## 🔧 Step 1: Start Your PostgreSQL Container
Make sure Docker Desktop is running, then open your terminal and run the following command to spin up the database container:

`docker run --name postgres-dev -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=postgres  -e POSTGRES_DB=moviemaking_db -p 5432:5432   -d postgres`

✅ Verify: Open Docker Desktop and ensure the postgres-dev container is running.

## 🌱 Step 2: Seed the Local Database
From the root of the project, run the database seeding script:

`python seed_local.py`

🎉 You should see debug messages and some green checkmarks — that means you're on the right track!

## 🚀 Step 3: Run the Application
Still in the project root, launch the app with:

`python run.py`

🟢 You should see a message like:
✅ Database connected successfully!

## 🔍 Step 4: Test It Out in Your Browser
Once the app is running:

Open your browser

Navigate to the local addresshttp://localhost:5000 

Explore all the routes!

All of the pages using render_template() should display properly (look through ___📁routes/___ )

