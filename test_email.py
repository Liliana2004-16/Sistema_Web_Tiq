import smtplib
from email.mime.text import MIMEText

mensaje = MIMEText("Prueba SMTP")
mensaje["Subject"] = "Prueba"
mensaje["From"] = "lilianamartinezdiaz2044@gmail.com"
mensaje["To"] = "16012004md@gmail.com"

server = smtplib.SMTP("smtp.gmail.com", 587)
server.starttls()
server.login("lilianamartinezdiaz2044@gmail.com", "ovucspbddxbdbtgu")
server.send_message(mensaje)
server.quit()

print("Correo enviado correctamente")
