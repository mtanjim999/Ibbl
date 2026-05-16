# IBBL Web ATM Demo

This repository now includes a browser-based demo for the ATM project.

## What changed

- `index.html` — a static web ATM demo built with HTML/CSS/JavaScript.
- `style.css` — styling for the browser version.
- `script.js` — login, deposit, withdraw, history, and admin account creation logic.
- `ibbl.py` remains the original desktop Tkinter application.

## How to open the web demo

1. Open `index.html` in your browser.
2. Use the demo credentials:
   - Account: `1001`
   - PIN: `1234`

## Browser demo features

- User login and logout
- Deposit and withdrawal transactions
- Mini statement sorted by amount
- Login history
- Admin panel to create new accounts

## Note

This web demo stores data in your browser's local storage. It is a static client-side version only and does not require a server.
