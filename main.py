import os
from dotenv import load_dotenv

from profile import fetch_profiles, choose_profile_interactive
from gologin_ref import init_go_login, close_go_login
from google_sheet_interaction import read_tasks_from_sheet
from rpa_logic import run_task

load_dotenv()

access_token = os.getenv("ACCESS_TOKEN") or "no token"
account_file = os.getenv("GOOGLE_SERVICE_ACCOUNT_FILE") or "no file name"
sheet_name = os.getenv("GOOGLE_SHEET_NAME") or "no sheet name"
sheet_tab = os.getenv("GOOGLE_SHEET_TAB") or "no sheet tab name"

if access_token == "no token":
    raise RuntimeError("Set GOLOGIN_TOKEN env var or edit the script with your real token.")
if account_file == "no file name":
    raise RuntimeError("Set GOOGLE_SERVICE_ACCOUNT_FILE for source reading")
if sheet_tab == "no sheet tab name":
    raise RuntimeError("Set GOOGLE_SHEET_NAME for source reading")
if sheet_tab == "no sheet tab name":
    raise RuntimeError("Set GOLOGIN_SHEET_TAB for source reading")

# --- get all GoLogin profiles
profiles = fetch_profiles(access_token)

# --- ask user which profile they want
selected_profile = choose_profile_interactive(profiles)
selected_profile_id = selected_profile.get("id")
print(f"\nUsing profile_id = {selected_profile_id}")

# --- start GoLogin + Selenium for that profile
gl, driver = init_go_login(access_token, selected_profile_id)
print("Browser attached to selected GoLogin profile.")

try:
    # --- read tasks from Google Sheets
    tasks = read_tasks_from_sheet(account_file, sheet_name, sheet_tab)
    print(f"Loaded {len(tasks)} task(s) from Google Sheets.")

    # --- execute each row as an RPA task
    for i, task in enumerate(tasks, start=1):
        print(f"\n=== Running task #{i} ===")
        print(task)
        run_task(driver, task)

    print("\nAll tasks executed.")

finally:
    # close_go_login(gl, driver)
    print("Closed GoLogin profile and saved session state.")
