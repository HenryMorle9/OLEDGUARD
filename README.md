# 🛡️ OLEDGUARD

**OLEDGUARD** is a lightweight utility that displays a black screen overlay after a period of inactivity — a simple and effective solution for preventing OLED screen burn-in, especially in situations where games or apps block standard screensaver behavior.

## 🚀 Features

- 🔒 **Black overlay screen** triggered after inactivity timeout
- 🕶️ **Hides mouse cursor** and fades in/out smoothly
- ⌨️ **Instant exit** on any mouse or keyboard input
- 📦 **Runs silently in background**
- 🪟 Optional **popup alert** confirming activation
- 🖥️ **Works even when games suppress screensaver/screens-off events**
- 🔁 Compatible with **Windows auto-start on boot**

## 🛠️ How It Works

OLEDGUARD monitors keyboard and mouse activity. If no input is detected for a user-defined period (default: 5 minutes), it:

1. Launches a full-screen black overlay using `tkinter`
2. Fades the screen to black gradually
3. Hides the cursor
4. Exits instantly on any user input

## 📦 Usage

## TODO

- make a installer
- maybe make a website so people can install it or make it open source for download

### ▶️ Running the Script (Python)

```bash
python burnin_prevention.py --enable --timeout 300

