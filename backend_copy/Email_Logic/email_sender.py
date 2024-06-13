import smtplib,ssl,os,sys
from simple_chalk import chalk


#from dotenv import load_dotenv,find_dotenv
#load_dotenv(find_dotenv())     

#get parent dir'backend_copy' from current script dir - append to sys.path to be searched for modules we import
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

if parent_dir not in sys.path:
    sys.path.append(parent_dir)

from config import GOOGLE_APP_PW,GOOGLE_SENDER_EMAIL

port = 465  # For SSL
app_password = GOOGLE_APP_PW
sender_email = GOOGLE_SENDER_EMAIL
#test

message = """\
Subject: Hi there

This message is sent from Python."""



def send_email(receiver_email,veh):

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