# Setup Instructions

## Prerequisites
- Python 3.11 or higher
- Node.js 18 or higher

## Backend Setup

```bash
cd backend
python -m venv venv
```

**Activate (Windows):**
```bash
venv\Scripts\activate
```

**Activate (Linux/macOS):**
```bash
source venv/bin/activate
```

**Install dependencies:**
```bash
pip install -r requirements.txt
```

## Frontend Setup

```bash
cd frontend
npm install
```

## Running the Application

**Terminal 1 - Backend:**
```bash
cd backend
source venv/bin/activate  # or venv\Scripts\activate on Windows
uvicorn app.main:app --reload --port 8000
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

Open: **http://localhost:3000**

API docs: **http://127.0.0.1:8000/docs**

## Running Tests

```bash
cd backend
pytest test_apis.py -v
```

Expected: 14 tests pass

## Troubleshooting

**Port 8000 in use:**
```bash
uvicorn app.main:app --reload --port 8001
```

**Missing dependencies:**
```bash
pip install -r requirements.txt
npm install
```

**Database issues:**
Delete `app.db` in backend folder and restart backend.
