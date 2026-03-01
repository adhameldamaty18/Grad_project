# ZeinaGuard
## Graduation Project: Wireless Intrusion Prevention System (WIPS)

<p align="center">
  <img src="https://i0.wp.com/cliqist.com/wp-content/uploads/2014/07/underdevelopmentlogo.jpg?w=1126&ssl=1" width="600" alt="Project Under Development">
</p>

## Project Overview
This repository contains the administrative backend and defensive logic for **ZeinaGuard Pro**, an advanced platform designed to monitor, detect, and mitigate wireless threats. The system also includes a **Rogue Server** module for simulating and analyzing malicious access point behaviors in a controlled research environment.

## Key Components
* **ZeinaGuard Pro:** The primary defense engine and real-time administrator dashboard.
* **Rogue Server:** A specialized environment for threat simulation and vulnerability analysis.
* **Threat Analyzer:** A custom engine that audits network integrity based on SSID, encryption, and signal strength.

## Tech Stack
* **Backend:** Python (Flask Framework)
* **Infrastructure:** Docker & Docker Compose
* **Database:** SQLite3
* **Frontend:** Bootstrap 5, JavaScript (Chart.js, FontAwesome)

## Repository Structure
```text
G_ADMIN/
├── ZeinaGuard_Pro/       # Main WIPS Application
│   ├── api/              # RESTful API Endpoints
│   ├── database/         # DB Manager and Schema
│   ├── engine/           # Threat Detection Logic
│   └── templates/        # Dashboard UI (HTML/JS)
├── Rogue_Server/         # Simulation and Research Module
└── README.md             # Project Documentation
```

## Deployment Guide

### Integrity Check
The system includes a secure deployment script (`run_zeina.sh`) that verifies the presence of all critical files before starting the environment. This ensures the system is healthy and prevents runtime errors.

### Quick Start

**Navigate to the core project:**
```bash
   cd ZeinaGuard_Pro
```

### Assign permissions and run:

```bash
chmod +x run_zeina.sh
./run_zeina.sh
```

### Access the Console:
Open your browser and go to: `http://localhost:5000`

## System Monitoring
* **Live Signal Analysis:** Real-time tracking of nearby access points and their risk scores.
* **Spectrum Density:** Visual feedback of channel usage.
* **Automated Mitigation:** Policy enforcement (e.g., auto-blocking rogue APs).
* **Sensor Heartbeat:** Status monitoring for all distributed security sensors.

