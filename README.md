# Odoo Project - Getting Started

## Introduction
This README provides instructions for getting started with Odoo, including installation, setup, and running your Odoo instance. Follow these steps to set up your Odoo environment and begin developing or testing your project.

## Table of Contents
- Requirements
- Getting Started
- Installation
- Configuration
- Running Odoo
- Database Management
- FAQ
- Support

## Requirements
Before you begin, ensure you have the following prerequisites installed on your system:

- Python: Version 3.7 or higher
- PostgreSQL: Version 9.6 or higher
- Node.js: Version 12+ (for web assets)
- NPM/Yarn: For building web assets
- Git: To clone the Odoo repository
- Pip: Python package installer
  
## Getting Started
Step 1: Clone the Odoo Repository
bash
git clone https://github.com/odoo/odoo.git
cd odoo
You can either use the official Odoo repository or your custom project repository if working with a specific project.

Step 2: Create a Python Virtual Environment
It’s a good practice to create a virtual environment to isolate your Odoo environment.

```bash
python -m venv odoo-venv
.\odoo-venv\Scripts\activate
```
Step 3: Install Python
Ensure Python 3.7 or higher is installed and properly added to your system's PATH.

Download Python from Python's official website.
Ensure you check Add Python to PATH during installation.

Step 4: Install Python Dependencies
Install the required Python packages using pip:

```bash
pip install -r requirements.txt
```

Step 5: Install PostgreSQL
Download PostgreSQL from here.
During installation, note down the PostgreSQL superuser password.
Create a new PostgreSQL user for Odoo:

Open pgAdmin or use the SQL Shell (psql).
Run the following command to create a user named odoo with superuser privileges:
```
sql
CREATE USER odoo WITH SUPERUSER PASSWORD 'yourpassword';
```

Step 6: Install Node.js Dependencies
Install Node.js and npm from the official Node.js website.

After installing Node.js, install necessary packages:

```
bash
npm install -g less less-plugin-clean-css
npm install -g rtlcss
```

## Installation
Step 1: Configure Odoo
Create an Odoo configuration file:

```bash
copy odoo.conf.example odoo.conf
```
Modify the following fields in odoo.conf:

```ini

[options]
admin_passwd = admin
db_host = False
db_port = False
db_user = odoo
db_password = False
addons_path = addons,custom_addons
logfile = /var/log/odoo/odoo.log
admin_passwd: The master password for managing databases.
addons_path: Specify the path to your Odoo addons or custom modules.
logfile: The location of the Odoo log file.
```

Step 2: Build Web Assets (Optional)
To build Odoo's web assets, you can use:

```
bash
npm install
```
If you're developing the web front-end, you can run:

```
bash
.\odoo-bin --dev=assets
```

## Running Odoo

To run Odoo, use the following command:
```
bash
.\odoo-bin -c odoo.conf
```
Odoo will now be running at http://localhost:8069.

To specify a different port, modify the odoo.conf file or pass the --xmlrpc-port option:
```
bash
.\odoo-bin -c odoo.conf --xmlrpc-port=8070
```

Accessing Odoo
Open your web browser and navigate to:
```
arduino
http://localhost:8069
```
You will be prompted to create a new database or select an existing one.

### Database Management
Creating a New Database
- Navigate to http://localhost:8069/web/database/manager.
- Click on "Create Database".
- Fill in the required fields:
Master Password: admin (as specified in odoo.conf).
Database Name: Choose a name for your database.
Email: Admin email for login.
Password: Admin password for login.
- Click "Create Database".
Managing Databases
You can manage databases using the Odoo database manager at:

```bash
http://localhost:8069/web/database/manager
```
Here, you can backup, restore, or delete databases.

## FAQ
How do I change the default port?
To change the default port, edit the odoo.conf file or run the following command:

```bash
./odoo-bin -c odoo.conf --xmlrpc-port=<desired_port>
```
How do I install custom modules?
- Place your custom modules in the custom_addons folder (or any folder specified in the addons_path).
- Update the module list:
Go to Apps > Update Apps List.
- Search for your custom module and install it.
How do I enable developer mode?
- To enable developer mode, append ?debug=1 to your URL:

```arduino
http://localhost:8069?debug=1
```
## Support
If you encounter any issues or need help, please refer to the official Odoo documentation:
- Odoo Documentation
- Odoo Community Forum
For custom support, contact the project maintainers.
