# G-500 Macro Index: OSRS Economy Tracker

The G-500 Macro Index is a Bloomberg-terminal-style dashboard designed to track, analyze, and visualize the Old School RuneScape (OSRS) economy. Rather than looking at individual item prices, this tool groups items into broader economic sectors (like "PvM Blue-Chips" and "Consumables") to calculate a stable, benchmark index score, giving you a macro-level view of the market's health.

## Features

- Dynamic Sector Tracking: Flawlessly swap between custom market baskets (PvM Gear, Consumables, Third Age, etc.) to view sector-specific performance.

- Automated Data Pipeline: A self-sustaining Python background scheduler scrapes live Grand Exchange data from the OSRS Wiki API every 5 minutes.

- Quantitative Analytics: Features a 1-Hour Simple Moving Average (SMA) trendline layered over raw data to filter out market noise.

- Interactive Data Visualization: Sleek, responsive charts with adjustable timeframes (1H, 24H, 7D) and custom hover tooltips.

- 24-Hour Market Indicators: Automatically calculates percentage changes against historical data to display real-time positive/negative market momentum badges.

- Self-Maintaining Database: Built-in data lifecycle management automatically prunes records older than 30 days to prevent server bloat.

- Demo Data Generator: Includes a custom randomization script to simulate 7 days of realistic market volatility for immediate dashboard visualization.

- Containerized Architecture: Fully Dockerized environment for instant, reliable setup across any machine without local dependency conflicts.

## Tech Stack

### Frontend

- React (via Vite)

- Tailwind CSS (Styling & Layout)

- Recharts (Interactive SVG Charting)

- Lucide React (UI Icons)

### Backend

- Python 3

- FastAPI (High-performance API routing)

- APScheduler (Background task automation)

- SQLite (Local database storage)

- Requests & Python-Dotenv

### DevOps & Infrastructure

- Docker & Docker Compose

## Setup Instructions

### Clone the Repository

```bash
git clone https://github.com/YourUsername/g-500-dashboard.git
cd g-500-dashboard
```

You can run this project using Docker (Recommended) or via a manual local installation.

## Method 1: Docker Setup (Recommended)

Prerequisites: Docker and Docker Compose installed on your system.

### Start the Containers

From the root directory of the project, build and start the application:

```bash
docker-compose up --build
```

### Generate Demo Data

Because Docker uses an isolated database volume, you need to populate it to see historical charts immediately. Open a second terminal window, navigate to the project root, and run the generator script inside the backend container:

```bash
docker-compose exec backend python generate_demo_data.py
```

### View the Dashboard (Dockerized)

Open your browser and navigate to [http://localhost:5173](http://localhost:5173).

## Method 2: Local Setup Instructions

Follow these steps to get the G-500 Macro Index running on your local machine.

### Prerequisites

- Node.js installed (for the React frontend)

- Python 3.8+ installed (for the FastAPI backend)

### Backend Setup (Python / FastAPI)

### Open a terminal and navigate to the backend directory

```bash
cd backend
```

### Create and activate a virtual environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

### Install the required dependencies

```bash
pip install fastapi uvicorn requests apscheduler python-dotenv
```

### Configure Backend Environment Variables

Create a .env file inside the backend folder and add the following:

```code
FRONTEND_URL=http://localhost:5173
WIKI_USER_AGENT=G500-Dashboard - @YourGitHubUsername
```

Start the Backend Server:

```bash
uvicorn main:app --reload
```

Note: Upon first boot, the backend will automatically generate the g500.db SQLite file and immediately scrape the first batch of market data.

### Frontend Setup (React / Vite)

Open a second terminal window and navigate to the frontend directory.

```bash
cd frontend
```

Install Node modules

```bash
npm install
```

### Configure Frontend Environment Variables

Create a .env file inside the frontend folder and add the following:

```code
VITE_API_BASE_URL=http://127.0.0.1:8000
```

### Generate Demo Data (Optional but recommended)

Run this script to inject 7 days of simulated market history into your local database so your charts populate instantly.

```bash
python generate_demo_data.py
```

### Start the Frontend Server

```bash
npm run dev
```

### View the Dashboard (Locally)

Open your browser and navigate to ```http://localhost:5173```.
(Note: The 1-Hour Moving Average line and the 24H Percentage Change indicators will populate once the server has been running long enough to collect historical data).
