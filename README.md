# FuelIQ
Tracking and building analytics based on fuel usage

## 📌 What FuelIQ Does
(1–2 lines on problem + value)

## 🚀 Active Features (Live / Stable)
- Features currently available to users

## 🛠 In Progress
- Actively being developed

## 📦 Testing
- Code complete, testing in progress

## 🗂 Backlog
- Initial Build
- Connect to MongoDB
- Calculation Logic
- UI
- Analytics
- Report Generator/Data fetcher
- Alert Notification


## Learning
# Initialize project metadata
uv init --bare

# Install dependencies
uv add fastapi "uvicorn[standard]"
uv add --dev pytest httpx ruff

# Create environment and install dependencies
uv sync

# Initialize Moon
moon setup

# Verify project discovery
moon project root

# Run tests
just test