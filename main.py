from dotenv import load_dotenv
import requests
import csv
import os

load_dotenv()

file_path = "DriverFobs.csv"
temp_file_path = "DriverFobs_temp.csv"
VZ_APP_ID = os.getenv("VZ_APP_ID")
VZ_AUTH_TOKEN = os.getenv("VZ_AUTH_TOKEN")


def main():
    token = get_token()

    if not token:
        print("Failed to get token. Exiting...")
        return

    app_id = VZ_APP_ID
    headers = {
        "Authorization": f"Atmosphere atmosphere_app_id={app_id}, Bearer {token}",
        "Accept": "application/json",
    }

    unsuccessful_rows = []

    with open(file_path, mode="r", encoding="utf-8-sig") as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            first_name = row["First Name"].strip()
            last_name = row["Last Name"].strip()
            keyfob = row["Key Fob"].upper()
            driver_number = f"{first_name}.{last_name}"

            response = requests.post(
                f"https://fim.api.us.fleetmatics.com/cmd/v1/drivers/",
                headers=headers,
                json={
                    "DriverNumber": driver_number,
                    "FirstName": first_name,
                    "LastName": last_name,
                },
            )

            if response.status_code != 201:
                print(f"Error creating driver for {driver_number}: {response.text}")
                unsuccessful_rows.append(row)
                continue

            response2 = requests.post(
                f"https://fim.api.us.fleetmatics.com/cmd/v1/drivers/{driver_number}/keys/",
                headers=headers,
                json=[keyfob],
            )

            if response2.status_code != 201:
                print(f"Error assigning key fob for {driver_number}: {response2.text}")
                unsuccessful_rows.append(row)
            else:
                print(f"Driver and key fob successfully processed for {driver_number}")

    if unsuccessful_rows:
        with open(
            temp_file_path, mode="w", newline="", encoding="utf-8-sig"
        ) as temp_file:
            fieldnames = ["First Name", "Last Name", "Key Fob"]
            writer = csv.DictWriter(temp_file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(unsuccessful_rows)

        import os

        os.replace(temp_file_path, file_path)
        print("Unsuccessful rows saved back to the CSV.")

    return "Success"


def get_token():
    headers = {
        "Authorization": VZ_AUTH_TOKEN,
        "Accept": "application/json",
    }

    response = requests.get(
        "https://fim.api.us.fleetmatics.com:443/token/", headers=headers
    )
    if response.status_code != 200:
        print(f"Error: HTTP Status Code Returned {response.status_code}")
        return None

    return response.text


if __name__ == "__main__":
    main()
