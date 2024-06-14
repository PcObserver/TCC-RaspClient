TCC-RaspClient
Overview
TCC-RaspClient is a Python-based project designed to run on a Raspberry Pi. It serves as a client application for a larger system, handling various tasks such as data collection, processing, and communication with a central server.

Features
Data Collection: Gathers data from connected sensors.
Data Processing: Processes the collected data for analysis.
Communication: Sends processed data to a central server.
Web Interface: Provides a web-based interface for monitoring and control.
Installation
Prerequisites
Python 3.7 or higher
Raspberry Pi with Raspbian OS
Steps
Clone the Repository

bash
Copy code
git clone https://github.com/PcObserver/TCC-RaspClient.git
cd TCC-RaspClient
Create and Activate Virtual Environment

bash
Copy code
python -m venv venv
source venv/bin/activate
Install Requirements

bash
Copy code
pip install -r requirements.txt
Database Setup
Initialize the Database
bash
Copy code
flask --app application db init
Apply Migrations
bash
Copy code
flask --app application db migrate -m "Initial migration."
Running the Server
Start the Flask server with the following command:

bash
Copy code
flask --app application run
Running as a Service
To run the TCC-RaspClient as a service on your Raspberry Pi, follow these steps:

Create a Systemd Service File

bash
Copy code
sudo nano /etc/systemd/system/tcc-raspclient.service
Add the following content to the file:

ini
Copy code
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
Reload Systemd and Start the Service

bash
Copy code
sudo systemctl daemon-reload
sudo systemctl start tcc-raspclient.service
sudo systemctl enable tcc-raspclient.service
Check the Status of the Service

bash
Copy code
sudo systemctl status tcc-raspclient.service
Project Structure
api/: Contains API endpoints.
data/: Stores data files.
migrations/: Database migration scripts.
models/: Database models.
static/: Static files (CSS, JS, images).
templates/: HTML templates.
utils/: Utility functions.
views/: View functions for the web interface.
Contributing
Contributions are welcome! Please follow these steps:

Fork the repository.
Create a new branch (git checkout -b feature-branch).
Make your changes and commit (git commit -m 'Add some feature').
Push to the branch (git push origin feature-branch).
Create a new Pull Request.
License
This project is licensed under the MIT License - see the LICENSE file for details.

Contact
For any inquiries or issues, please open an issue on GitHub.
