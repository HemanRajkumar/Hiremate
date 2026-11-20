# Windows setup notes

## 1. Install Python dependencies

The pinned Starlette version must remain compatible with FastAPI. This project uses:

- `fastapi==0.128.2`
- `starlette==0.50.0` (FastAPI requires Starlette >=0.40.0 and <0.51.0)

From the repository root, in PowerShell:

```powershell
python -m pip install -r requirements.txt
```

## 2. Start the backend

If PowerShell reports that `uvicorn.exe` is blocked by Windows Application Control, start Uvicorn as a Python module instead:

```powershell
python -m uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000
```

This avoids directly launching the `uvicorn.exe` console-script executable. If your organization's App Control policy also blocks Python module execution, ask the device administrator to approve the Python environment or executable; do not try to bypass the policy.

## 3. Start the frontend

In a second PowerShell window:

```powershell
cd frontend
npm install
npm run dev
```

Open http://localhost:5173.

## 4. Check the API

Open http://127.0.0.1:8000/api/health. FastAPI's interactive API documentation is at http://127.0.0.1:8000/docs.
