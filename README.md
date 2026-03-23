# ⚡ QR Code Generator

A simple Flask web application that converts any URL or text into a downloadable QR code — runnable both locally and via Docker.

---

## 🗂️ Project Structure

```
QR-Generator/
├── app.py              # Flask application
├── templates/
│   └── index.html      # Frontend UI
├── requirements.txt    # Python dependencies
├── Dockerfile          # Docker configuration
├── .gitignore
├── LICENSE
└── README.md
```

---

## 🚀 Running WITHOUT Docker (local Python)

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

## 🐳 Running WITH Docker

### Prerequisites
- Docker Desktop installed and running

### Steps

```bash
# 1. Clone the repository
git clone https://github.com/vaishnavipatil-10/QR-Generator.git
cd QR-Generator

# 2. Build the Docker image
docker build -t qr-generator .

# 3. Run the container
docker run -p 5000:5000 qr-generator
```

Visit: **http://localhost:5000**

### Stop the container

```bash
docker ps                         # Find the container ID
docker stop <container-id>
```

---

## 🔍 Without Docker vs With Docker

| Aspect | Without Docker | With Docker |
|---|---|---|
| Setup | Install Python + pip manually | Just need Docker |
| Dependencies | Installed on your machine | Isolated inside container |
| Conflicts | May clash with other projects | Zero conflicts |
| Portability | "Works on my machine" | Works everywhere |
| Command | `python app.py` | `docker run -p 5000:5000 qr-generator` |

---

## 🛠️ Tech Stack

- **Python 3.11**
- **Flask** — lightweight web framework
- **qrcode** — QR code generation
- **Pillow** — image processing
- **Docker** — containerization

---

## 👩‍💻 Contributors

- [@vaishnavipatil-10](https://github.com/vaishnavipatil-10) — Project creator
- [@prachi-satbhai0741](https://github.com/prachi-satbhai0741) — Docker integration & app improvements

---

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.