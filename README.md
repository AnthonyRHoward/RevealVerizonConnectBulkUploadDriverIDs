# DriverFobs Uploader

This Python script automates the process of creating drivers and assigning key fobs in Verizon Connect (Fleetmatics) using their API. It reads driver data from a CSV file and utilizes environment variables securely through a `.env` file.

---

## 📦 Features

- Reads driver information from a `DriverFobs.csv` file
- Sends API requests to:
  - Create new drivers
  - Assign key fobs to drivers
- Logs unsuccessful entries and writes them back to the original CSV for retry
- Uses environment variables for sensitive credentials via `.env`

---

## 🔧 Requirements

- Python 3.7+
- `requests`
- `python-dotenv`

Install dependencies with:

```bash
pip install -r requirements.txt
```

**requirements.txt**

```
requests
python-dotenv
```

---

## 📁 .env File

Create a `.env` file in the root of your project directory:

```
VZ_APP_ID=your_verizon_connect_app_id
VZ_AUTH_TOKEN=your_verizon_connect_auth_token
```

---

## 📄 Input CSV File

Place a file named `DriverFobs.csv` in the same directory. It must have the following headers:

```
First Name, Last Name, Key Fob
```

**Example:**

```csv
First Name,Last Name,Key Fob
John,Doe,ABC123
Jane,Smith,DEF456
```

---

## 🚀 Usage

Run the script with:

```bash
python your_script_name.py
```

Successful entries are processed via the Verizon Connect API. Any unsuccessful rows (e.g. due to bad data or API errors) will be written back into `DriverFobs.csv` so you can reprocess them later.

---

## 📤 API Endpoints Used

- **Get Token:**  
  `GET https://fim.api.us.fleetmatics.com:443/token/`

- **Create Driver:**  
  `POST https://fim.api.us.fleetmatics.com/cmd/v1/drivers/`

- **Assign Key Fob to Driver:**  
  `POST https://fim.api.us.fleetmatics.com/cmd/v1/drivers/{driverNumber}/keys/`

---

## 🛡️ Security

⚠️ Never commit your `.env` file to source control.

Add it to your `.gitignore`:

```gitignore
.env
```

---

## 🧼 Cleanup Behavior

If a driver or key fob cannot be successfully created, that row is logged and saved back to the CSV file for later retry.

---

## 🙌 Acknowledgements

Built with ❤️ for internal automation using Verizon Connect (Fleetmatics) APIs.
