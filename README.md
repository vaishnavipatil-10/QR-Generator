# QR Code Generator

A simple Flask web application that converts any URL or text into a downloadable QR code — runnable locally with Python.

---

## Project Structure

```
QR-Generator/
├── app.py              # Flask application
├── index.html          # Frontend UI
├── requirements.txt    # Python dependencies
├── .gitignore
├── LICENSE
└── README.md
```

---

## 🚀 Running the App (local Python)

### Prerequisites
- Python 3.10+
- pip

### Steps

```bash
# 1. Clone the repository
git clone https://github.com/vaishnavipatil-10/QR-Generator.git
cd QR-Generator

# 2. Create a virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate        # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the app
python app.py
```

Visit: **http://localhost:5000**

---

## 🛠️ Tech Stack

- **Python 3.11**
- **Flask** — lightweight web framework
- **qrcode** — QR code generation
- **Pillow** — image processing

---

## 👩‍💻 Contributors

- [@vaishnavipatil-10](https://github.com/vaishnavipatil-10) — Project creator
- [@prachi-satbhai0741](https://github.com/prachi-satbhai0741) — App improvements

---

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.