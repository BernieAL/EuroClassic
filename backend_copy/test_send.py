import smtplib, ssl,os
from simple_chalk import chalk
from dotenv import load_dotenv,find_dotenv
load_dotenv(find_dotenv())     


port = 465  # For SSL
app_password = os.getenv("GOOGLE_APP_PW")
sender_email = os.getenv("GOOGLE_SENDER_EMAIL") # Enter your address
#test

message = """\
Subject: Hi there

This message is sent from Python."""



def send_email(reciever_email,veh):

    # Create a secure SSL context
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        try:
            server.login(sender_email, app_password)
            server.sendmail(sender_email, receiver_email, message)
            print(chalk.green(f"SUCCESSFULLY SENT MESSAGE TO EMAIL: {receiver_email} - FOR VEH: {veh}"))
        except Exception as e:
            print(chalk.red(f"There was an error with sending the email {e}"))



if __name__ == "__main__":
    
    receiver_email = "balmanzar883@gmail.com"  # Enter receiver address
    veh = "Audi R8"
    send_email(receiver_email,veh)