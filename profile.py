import requests
from typing import Any

def fetch_profiles(token: str):
    url = "https://api.gologin.com/browser/v2"
    headers = {
        "Authorization": f"Bearer {token}",
    }
    resp = requests.get(url, headers=headers, timeout=30)

    if resp.status_code != 200:
        raise RuntimeError(f"Error {resp.status_code}: {resp.text}")

    data = resp.json()

    if isinstance(data, dict) and "profiles" in data:
        return data["profiles"]
    elif isinstance(data, list):
        return data
    else:
        raise RuntimeError(f"Unexpected response shape: {data}")


def choose_profile_interactive(profiles: list[dict[str, Any]]) -> dict[str, Any]:
    """
    Print profiles list and let the user choose by number or by ID.
    Returns the selected profile dict.
    """
    print("Select from the following profiles, by writing the number OR the ID.")
    for index, profile in enumerate(profiles, start=1):
        print(
            f"{index}. "
            f"Name: {profile.get('name')} | "
            f"Location: {profile.get('proxy', {}).get('customName')} | "
            f"ID: {profile.get('id')}"
        )

    choice = input("\nEnter profile number or profile ID: ").strip()

    selected_profile = None

    # If they typed a number
    if choice.isdigit():
        idx = int(choice) - 1
        if 0 <= idx < len(profiles):
            selected_profile = profiles[idx]
        else:
            raise ValueError("No profile with that number.")

    # If not found yet, try treat input as ID
    if selected_profile is None:
        for p in profiles:
            if p.get("id") == choice:
                selected_profile = p
                break

    if selected_profile is None:
        raise ValueError("Could not match that input to any profile by number or id.")

    return selected_profile