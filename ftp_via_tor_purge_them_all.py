#DISCLAIMER!!! THIS IS ONLY FOR STUDYING AND DEMONSTRATION PURPOSES. I AM NOT RESPONSIBLE FOR THE WAY THIS SCRIPT IS USED!!!
#this script collect and then purge all the files in a FTP server passing the connection through tor
#TOR must run in the local server running this script

import os
import ftplib
import socks
import socket
import time

# FTP config
FTP_HOST = "" #INSERT HOST
FTP_USER = "" #INSERT USER
FTP_PASS = "" #INSERT PASS
LOCAL_DIRECTORY = "" #INSERT THE DIRECTORY WHERE TO SAVE THE FILES

# SOCKS configuration for tor
socks.set_default_proxy(socks.SOCKS5, "127.0.0.1", 9050)
socket.socket = socks.socksocket

def download_file(ftp, filename):
    """Download a file from the remote server"""
    local_path = os.path.join(LOCAL_DIRECTORY, filename)
    with open(local_path, "wb") as local_file:
        ftp.retrbinary("RETR " + filename, local_file.write)
        print(f"I am now downloading: {filename}")

def delete_remote_file(ftp, filename):
    """delete the file from the server"""
    ftp.delete(filename)
    print(f"I've deleted: {filename}")

def main():
    while True:
        try:
            ftp = ftplib.FTP(FTP_HOST)
            ftp.login(FTP_USER, FTP_PASS)
            print("FTP connection established")

            filenames = ftp.nlst()  # Obtain files and directories list
            for filename in filenames:
                # Check if it is a file
                try:
                    ftp.size(filename)  # If it fails, it isn't a file
                    download_file(ftp, filename)
                    delete_remote_file(ftp, filename)
                except ftplib.error_perm:
                    print(f"{filename} is a directory, I move forward...")

            ftp.quit()

        except Exception as e:
            print(f"Error: {e}")

        # Wait 10 seconds before rechecking
        time.sleep(10)

if __name__ == "__main__":
    main()
