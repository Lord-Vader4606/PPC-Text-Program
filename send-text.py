from requests import get
from os import system
from twilio.rest import Client

VERSION = "0.0.1"
ACCOUNT_SID = ""
AUTH_TOKEN = ""
PHONE_NUMBER = ""

system("cls")
system("clear")

print(f"Text Program v{VERSION}\nFetching Database...")

# FETCH DATABASE
try:
    text_database = get("FETCH_API_HERE").json()
except:
    print("Error - Stopping")
    SystemExit()

# GET USER COUNT
count = 0
for user in text_database["data"]:
    count += 1

print(f"Fetched {count} users")

# CONNECT TO TWILIO
try:
    client = Client(ACCOUNT_SID, AUTH_TOKEN)
except:
    print("Error - Stopping")
    SystemExit()

# READ MESSAGE
def get_message():
    message = open("message.txt", "w")
    message.write("TEXT MESSAGE HERE, USE {@user} TO REPLACE WITH THEIR NAME\nDELETE ALL CONTENTS OF FILE FIRST!")
    message.close()

    system("cls")
    system("clear")

    print("Open the file 'message.txt' and put the text in this file. Be sure to delete all contents of file.")
    input("Press enter when ready...")

    message = open("message.txt", "r")
    print("Your message:\n---\n")
    output = message.read()
    message.close()

    print(output)
    print("\n--\n")
    
    check = input("Enter the number '1' if this is the message you want to use, otherwise, enter anything to update it.")
    if check == "1":
        return output
    else:
        return get_message()

# SECONDARY MENU
def message_menu():
    check = input("[3] Send as test (to steve and Erik)\n[4] Send officially (to everyone)\n")
    if check == "3":
        return "test"
    elif check == "4":
        return "everyone"
    else:
        print("Huh, I am not sure what you meant. Maybe try again?")
        return message_menu()

# SEND TEXT
def text(message, to, name="Test"):
    try:
        msg = client.messages.create(
            body = message,
            from_ = PHONE_NUMBER,
            to = "+1" + to
        )
        print (f"Sent text to {name} at {to}")
        return msg
    except:
        print("Error - Stopping")

# SHOW MENU
request = input("Enter the number of the command:\n[1] Send Text\n[2] Quit\n")
while not request == "2":
    if request == "1":
        print("Send Text")
        
        message = get_message()
        option = message_menu()

        if option == "test":
            msg = text(message.replace("{@user}", "Erik"), "", "Erik") # Send to Erik
            msg = text(message.replace("{@user}", "Steve"), "", "Steve") # Send to Steve
            print("Done!")
        elif option == "everyone":
            sent = 0
            for user in text_database["data"]:
                msg = text(message.replace("{@user}", user['name']), user['phone'], user['name'])
                
                system("cls")
                system("clear")
                
                to_percent = round((sent / count), 2) * 100
                print(f"Sending...\n{to_percent}% Complete")
                
                sent += 1
            print("Done!")
            
    else:
        print(f"Command '{request}' not recognized")
    request = input("Enter the number of the command:\n[1] Send Text\n[2] Quit\n")

print("Goodbye!")
