Jaalee API Integration for Home Assistant
This is a custom integration for Home Assistant to retrieve data from Jaalee sensors via their cloud API.

Installation
HACS (Recommended)
Add this repository as a custom repository in HACS.

Go to HACS > Integrations > Click the 3 dots in the top right.

Select "Custom repositories".

Paste the URL of this GitHub repository.

Select "Integration" as the category.

Click "Add".

The "Jaalee API" integration will now be available in HACS. Click "Install".

Restart Home Assistant.

Manual Installation
Create a jaalee_api directory inside your custom_components directory.

Copy all the files from this repository (__init__.py, manifest.json, sensor.py, etc.) into the new custom_components/jaalee_api/ directory.

Restart Home Assistant.

Configuration
Go to Settings > Devices & Services.

Click + Add Integration.

Search for "Jaalee API" and select it.

Follow the on-screen instructions:

Enter the email address associated with your Jaalee account.

You will receive a verification code via email. Enter this code in the next step.

The integration will be set up, and sensors for your devices will be added automatically.

How It Works
This integration polls the Jaalee cloud API every 2 minutes to fetch the latest data from all your registered sensors. It uses a permanent token obtained during the initial configuration, so you only need to enter your credentials once.
