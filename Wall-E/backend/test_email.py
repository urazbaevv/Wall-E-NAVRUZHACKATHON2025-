import sqlite3
import smtplib
from email.message import EmailMessage
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# 📌 Email sozlamalari
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_ADDRESS = "orazbaevqudaybergen0@gmail.com"  # O'zingizning email manzilingiz
EMAIL_PASSWORD = "jwig ssky uiuy djli"  # Google App Password

# 📌 Ma'lumotlar bazasi joylashuvi
DATABASE_PATH = "data/containers.db"
def send_email_notification():
    send_alert_email()
def get_full_containers():
    """To‘lib ketgan konteynerlarni bazadan olish"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT name, weight, max_weight, lat, lon FROM containers WHERE weight >= max_weight")
    full_containers = cursor.fetchall()
    conn.close()
    return full_containers

def send_alert_email():
    """To‘lib ketgan konteynerlar haqida email xabarnoma yuborish"""
    full_containers = get_full_containers()

    if not full_containers:
        print("✅ All containers are in normal condition, no email was sent.")
        return

    # 📌 Xabar tarkibi
    subject = "🚨 Warning: There is(are) a full container(s)!"
    body = "The following container(s) is(are) full:\n\n"

    for container in full_containers:
        name, weight, max_weight, lat, lon = container
        google_maps_link = f"https://www.google.com/maps?q={lat},{lon}"
        body += f"🔹 {name}: {weight}/{max_weight} kg\n📍 Position: {google_maps_link}\n\n"

    body += "It must be taken away immediately!🚛"

    # 📌 Email jo‘natish
    msg = MIMEMultipart()
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = "iskandarovasilbek70@gmail.com"  # Qabul qiluvchi email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)  # ✅ Use SMTP (not SMTP_SSL)
        server.starttls()  # ✅ Upgrade connection to TLS
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.sendmail(EMAIL_ADDRESS, msg["To"], msg.as_string())
        server.quit()
        print("✅ Email was sent successfully!")
    except Exception as e:
        print(f"❌ Error while sending email: {e}")

# 📌 Skriptni ishga tushirish
if __name__ == "__main__":
    send_alert_email()


