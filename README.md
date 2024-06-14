
## Overview

TCC-RaspClient is a Python-based project designed to run on a Raspberry Pi. It serves as a client application for a larger system.

## Features

- **Data Collection:** Gathers data from connected sensors.
- **Data Processing:** Processes the collected data for analysis.
- **Communication:** Sends processed data to a central server.
- **Web Interface:** Provides a web-based interface for monitoring and control.

## Installation

### Prerequisites

- Python 3.7 or higher
- Raspberry Pi with Raspbian OS

### Steps

1. **Clone the Repository**

  ```
   git clone https://github.com/PcObserver/TCC-RaspClient.git
   cd TCC-RaspClient
```
2. **Create and Activate Virtual Environment**

 ```
  Copy code
  python -m venv venv
  source venv/bin/activate
 ```
3. **Install Requirements**
 ```
  pip install -r requirements.txt
 ```

## Database Setup
### Initialize the Database
```
flask --app application db init
```
### Apply Migrations
```
flask --app application db migrate -m "Initial migration."
```
## Running the Server
Start the Flask server with the following command:
```
flask --app application run
```
### Running as a Service
To run the TCC-RaspClient as a service on your Raspberry Pi, follow these steps:

### Create a Systemd Service File
 ```
sudo nano /etc/systemd/system/tcc-raspclient.service
 ```
### Add the following content to the file:

 ```
[Unit]
Description=TCC-RaspClient Service
After=network.target

[Service]
User=pi
WorkingDirectory=/home/pi/TCC-RaspClient
Environment="PATH=/home/pi/TCC-RaspClient/venv/bin"
ExecStart=/home/pi/TCC-RaspClient/venv/bin/flask --app application run --host=0.0.0.0

[Install]
WantedBy=multi-user.target
 ```
### Reload Systemd and Start the Service
 ```
sudo systemctl daemon-reload
sudo systemctl start tcc-raspclient.service
sudo systemctl enable tcc-raspclient.service
 ```
### Check the Status of the Service
 ```
sudo systemctl status tcc-raspclient.service
 ```
## Project Structure
* api/: Contains API wrapper for remote api endpoints.
* data/: Stores sqlite data files.
* migrations/: Database migration scripts.
* models/: Database models.
* static/: Static files (CSS, JS, images).
* templates/: HTML templates.
* utils/: Utility functions.
* views/: View functions for the web interface.

## Contact
For any inquiries or issues, please open an issue on GitHub.
