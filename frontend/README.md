This folder contains the frontend static files for the Exam Cell project.

Run a simple static server from the repository root to serve it during development:

Windows PowerShell:

```powershell
cd c:\workspace\exam-cell-automation-\frontend
python -m http.server 3000
```

Open http://localhost:3000 in your browser.

Files:
- `index.html` - the single-page frontend entry.
- `src/` - source files for pages (Login, Dashboard, Halltickets, Register).
