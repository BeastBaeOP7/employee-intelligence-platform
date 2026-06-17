import requests


def find_employee_by_name(name: str):

    try:

        response = requests.get(
            f"http://127.0.0.1:8001/employee/{name}",
            timeout=5
        )

        if response.status_code != 200:
            return None

        data = response.json()

        if "error" in data:
            return None

        return data

    except Exception:
        return None