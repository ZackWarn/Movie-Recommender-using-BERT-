# Local Development Setup

## Quick Start

### Option 1: Use Lightweight Mock API (Fastest)

```bash
# Terminal 1: Start mock Flask API on port 5000
python local_flask_api.py

# Terminal 2: Start Next dev server on port 3001
$env:PORT=3001
npm run dev
```

Then open: **http://localhost:3001**

### Option 2: Use Full Production API

```bash
# Terminal 1: Start Flask API on port 5000
python flask_api.py

# Terminal 2: Start Next dev server on port 3001
$env:PORT=3001
npm run dev
```

Then open: **http://localhost:3001**

## Environment Variables

Create `.env.local` in the cinematch directory:

```env
API_URL=http://localhost:5000
NEXT_PUBLIC_API_URL=http://localhost:5000
```

## Testing the API

### Test Flask directly:

```powershell
$body = '{"query":"Inception","top_k":3}'
Invoke-RestMethod -Uri "http://localhost:5000/api/recommendations/query" `
  -Method Post `
  -ContentType "application/json" `
  -Body $body
```

### Test Next proxy:

```powershell
$body = '{"query":"Inception","top_k":3}'
Invoke-RestMethod -Uri "http://localhost:3001/api/recommendations/query" `
  -Method Post `
  -ContentType "application/json" `
  -Body $body
```

### Health check:

```powershell
Invoke-RestMethod -Uri "http://localhost:5000/health"
```

## Troubleshooting

### Next still on port 3000?

- Kill the process on 3000: `Get-Process node | Stop-Process -Force`
- Then use `$env:PORT=3001; npm run dev`

### Port already in use?

```powershell
# Find process on port 5000
netstat -ano | findstr :5000
# Kill it
taskkill /PID <PID> /F
```

### API not responding?

1. Check Flask is running: `Test-NetConnection -ComputerName localhost -Port 5000`
2. Check .env.local has `API_URL=http://localhost:5000`
3. Check browser console for CORS errors
4. Try health endpoint: `http://localhost:5000/health`

## Features

### local_flask_api.py

- ✅ Lightweight, loads faster than production flask_api.py
- ✅ Graceful degradation: uses mock data if real engine unavailable
- ✅ Same API endpoints as production
- ✅ Hot reload enabled
- ✅ Debug mode on

### .env.local

- ✅ Tells Next to proxy to localhost:5000
- ✅ Overrides default production values
- ✅ Not committed to git (already in .gitignore)
