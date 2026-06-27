# 📝 Real-Time Text Sync (Offline Network Tool)

A lightweight web application built with Flask that allows **real-time text sharing between devices on the same local network**, using a polling-based synchronization mechanism.

---

## 📌 Overview

This project is designed to quickly share text between devices (such as laptop and mobile) without requiring internet access.

It is especially useful in situations where:

* Internet is unavailable or restricted
* You need to transfer VPN configurations or proxy links
* You want a simple, fast, and local solution

---

## 🎯 Use Case (Why This Project Exists)

I built this tool for situations where the internet is unstable or completely قطع (offline).

The main goal was:

* Easily transfer **VPN configs**
* Send **Telegram proxy links**
* Share any text from **laptop → mobile** instantly

Without:

* Messaging apps
* Internet connection
* External services

---

## ✨ Features

* 🔄 Text synchronization between multiple devices
* 🌐 Works over Local Network (WiFi / Hotspot)
* ⌛ Auto-update every 2 seconds (Polling)
* 📋 One-click Copy button
* ♻️ Reset shared text globally
* 🌙 Clean Dark Mode UI
* ⚡ No installation required for client devices

---

## 🧠 How It Works

### Backend (Flask)

* A global variable stores the shared text
* Thread-safe access using a lock
* API endpoints:

  * `/get_text` → returns current text
  * `/update_text` → updates text
  * `/reset_text` → clears text

### Frontend

* Sends updates when user types
* Polls server every 2 seconds
* Updates UI only if text has changed

---

## 📱💻 How to Use (Laptop + Mobile)

### 🖥 Step 1 — Run Server on Laptop

```bash
python main.py
```

You will see something like:

```text
Running on http://127.0.0.1:5000
Running on http://192.168.1.5:5000
```

👉 The important one is:

```text
http://192.168.X.X:5000
```

---

### 📱 Step 2 — Connect Mobile

1. Connect your phone to the **same WiFi or hotspot**
2. Open browser on your phone
3. Enter the IP address shown in terminal:

```text
http://192.168.1.5:5000
```

---

### 🔄 Step 3 — Start Sync

* Type text on laptop → appears on phone
* Type on phone → appears on laptop
* Click **Copy** → copy text instantly
* Click **Reset** → clears text for all devices

---

## 🌐 Network Requirements

* Both devices must be on the **same network**
* Works with:

  * WiFi
  * Mobile hotspot
  * Local LAN

❌ Does NOT require internet

---

## ⚙️ Technologies Used

* Python
* Flask
* HTML / CSS / JavaScript
* Fetch API (Polling)

---

## 📂 Project Structure

```bash
.
├── main.py
├── index.html
└── README.md
```

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/USERNAME/REPO.git
cd REPO
```

### 2. Install dependencies

```bash
pip install flask
```

### 3. Run the app

```bash
python main.py
```

---

## ⚠️ Notes

* This is a simple development server (not production-ready)
* Data is stored in memory (resets when server restarts)
* Polling interval is 2 seconds (can be optimized)

---

## 🔮 Future Improvements

* WebSocket (real-time without polling)
* Multi-room support
* Authentication
* Save history

---

## ⭐ Support

If you found this useful, consider giving it a ⭐ on GitHub!
