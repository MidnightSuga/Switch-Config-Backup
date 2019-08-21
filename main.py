import os
import time
import csv
import getpass
import netmiko.cisco.cisco_ios as cisco
from sendEmail import Email

commands = [
    "show running-config"
]

uname = input("Enter Username: ")
pwd = getpass.getpass()
emailaddress = input("Enter email to notify once finished (if empty, no email will be sent): ")

outvar = os.path.join(os.environ['USERPROFILE'], "Desktop\Config Backups")
if not os.path.isdir(outvar):
    os.mkdir(outvar)

finished = 0
with open("switches.csv", newline='') as csvfile:
    switches = csv.DictReader(csvfile, delimiter=',', )
    for row in switches:
        print(row['name'])
        try:
            with open(outvar + "\\" + row['name'] + '.txt', "w") as f:
                f.write(row['name'])
                f.write("\n")
                net_connect = cisco.CiscoIosSSH(ip=row['ip'], username=uname, password=pwd)
                for command in commands:
                    output = net_connect.send_command(command)
                    f.write(output)
                f.close()
        except Exception as error:
            with open(outvar + "\\error.log", "a") as errorfile:
                errorfile.write(time.strftime("%m/%d/%y %H:%M") + " Error Occurred: {0}".format(str(error), str(error)))
                errorfile.write("\n")
                errorfile.close()
            print("Error Occurred.  Check Error log in Config Backup folder")
    csvfile.close()
    finished = 1

if not emailaddress:
    pass
else:
    while True:
        if finished == 1:
            try:
                Email.sendemail(emailaddress)
                break
            except Exception as error:
                with open(outvar + "\\error.log", "a") as errorfile:
                    errorfile.write(
                        time.strftime("%m/%d/%y %H:%M") + " Error Occurred: {0}".format(str(error), str(error)))
                    errorfile.write("\n")
                    errorfile.close()
                    print("Error Occurred.  Check Error log in Config Backup folder")
                break
        time.sleep(3)
