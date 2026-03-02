# Webhook Repository Activity Monitor

This project receives GitHub webhook events and displays repository activity in a live UI.

It tracks:
- Push events
- Pull request opened
- Pull request closed
- Pull request merged
- Pull request reopened

The backend stores events and the frontend displays them in a human-readable activity log and raw data table.

---

## 🚀 Features

- Webhook endpoint to receive GitHub events
- Stores structured activity data in MongoDB
- Live activity feed UI
- Toggle between activity log and raw table view
- Supports full pull request lifecycle
- Auto-refresh every 15 seconds

---

## 📦 Tech Stack

- Python (Flask)
- MongoDB
- HTML + CSS + JavaScript

---

## 🌐 Live UI

You can view the live repository activity here:

👉 https://webhook-app-ncsq.onrender.com
