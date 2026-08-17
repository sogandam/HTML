from flask import Flask, render_template, request, redirect, url_for, flash
from datetime import datetime
import os
import json
import gspread
from google.oauth2.service_account import Credentials


app = Flask(__name__)

# Secret key for Flask messages
app.secret_key = os.environ.get(
    "SECRET_KEY",
    "attendance-secret-key"
)


# ============================================================
# GOOGLE SHEETS SETTINGS
# ============================================================

# Your Google Sheet ID
SPREADSHEET_ID = "1tSXOGdLg-RUyYNcCejUwS0O_UU1EC-95zzbYzSxhwl8"


# Google API permissions
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets"
]


def get_google_sheet():
    """
    Connect to Google Sheets using the Google Cloud
    service account credentials stored in Render.
    """

    credentials_json = os.environ.get(
        "GOOGLE_SERVICE_ACCOUNT_JSON"
    )

    if not credentials_json:
        raise Exception(
            "GOOGLE_SERVICE_ACCOUNT_JSON environment variable is missing."
        )

    credentials_info = json.loads(credentials_json)

    credentials = Credentials.from_service_account_info(
        credentials_info,
        scopes=SCOPES
    )

    client = gspread.authorize(credentials)

    spreadsheet = client.open_by_key(
        SPREADSHEET_ID
    )

    # Use the first worksheet
    worksheet = spreadsheet.sheet1

    return worksheet


# ============================================================
# CREATE / CHECK HEADERS
# ============================================================

def setup_sheet():
    """
    Make sure the Google Sheet has the correct headers.
    """

    worksheet = get_google_sheet()

    headers = [
        "No",
        "Adı Soyadı",
        "Fakülte",
        "Bölüm",
        "Katılım Durumu",
        "Tarih/Saat"
    ]

    first_row = worksheet.row_values(1)

    if first_row != headers:
        worksheet.update(
            "A1:F1",
            [headers]
        )


# ============================================================
# ADD ATTENDANCE
# ============================================================

def add_attendance(name, faculty, department):
    """
    Add a new attendance record to Google Sheets.

    Returns:
        True       -> successful
        False      -> duplicate
        "error"    -> error
    """

    try:

        worksheet = get_google_sheet()

        # Get all existing records
        records = worksheet.get_all_values()

        # ----------------------------------------------------
        # CHECK DUPLICATES
        # ----------------------------------------------------

        for row in records[1:]:

            if len(row) < 4:
                continue

            existing_name = row[1].strip().lower()
            existing_faculty = row[2].strip().lower()
            existing_department = row[3].strip().lower()

            if (
                existing_name == name.strip().lower()
                and existing_faculty == faculty.strip().lower()
                and existing_department == department.strip().lower()
            ):

                return False

        # ----------------------------------------------------
        # REGISTRATION NUMBER
        # ----------------------------------------------------

        registration_number = len(records)

        # ----------------------------------------------------
        # DATE AND TIME
        # ----------------------------------------------------

        now = datetime.now()

        date_time = now.strftime(
            "%d.%m.%Y %H:%M:%S"
        )

        # ----------------------------------------------------
        # ADD NEW ROW
        # ----------------------------------------------------

        worksheet.append_row(
            [
                registration_number,
                name,
                faculty,
                department,
                "KATILDI",
                date_time
            ],
            value_input_option="USER_ENTERED"
        )

        return True

    except Exception as error:

        print(
            "Google Sheets error:",
            error
        )

        return "error"


# ============================================================
# HOME PAGE
# ============================================================

@app.route("/", methods=["GET", "POST"])
def index():

    if request.method == "POST":

        # ----------------------------------------------------
        # GET FORM DATA
        # ----------------------------------------------------

        name = request.form.get(
            "name",
            ""
        ).strip()

        faculty = request.form.get(
            "faculty",
            ""
        ).strip()

        department = request.form.get(
            "department",
            ""
        ).strip()

        # ----------------------------------------------------
        # CHECK EMPTY FIELDS
        # ----------------------------------------------------

        if not name or not faculty or not department:

            flash(
                "Lütfen tüm alanları doldurunuz.",
                "error"
            )

            return redirect(
                url_for("index")
            )

        # ----------------------------------------------------
        # SAVE TO GOOGLE SHEETS
        # ----------------------------------------------------

        result = add_attendance(
            name,
            faculty,
            department
        )

        # ----------------------------------------------------
        # SUCCESS
        # ----------------------------------------------------

        if result is True:

            return render_template(
                "success.html",
                name=name
            )

        # ----------------------------------------------------
        # DUPLICATE
        # ----------------------------------------------------

        elif result is False:

            flash(
                "Bu kişi daha önce katılım kaydı oluşturmuştur.",
                "error"
            )

            return redirect(
                url_for("index")
            )

        # ----------------------------------------------------
        # ERROR
        # ----------------------------------------------------

        else:

            flash(
                "Kayıt sırasında bir hata oluştu. "
                "Lütfen tekrar deneyiniz.",
                "error"
            )

            return redirect(
                url_for("index")
            )

    return render_template(
        "index.html"
    )


# ============================================================
# START APPLICATION
# ============================================================

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )