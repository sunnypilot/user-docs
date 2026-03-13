# What is Openpilot Toolkit (OPTK)

Openpilot Toolkit is a class library and toolkit for interacting with your openpilot / comma devices. 

Current Features
Windows app:

* Drive video player and raw export of all cameras
* SSH wizard to generate and install SSH keys
* Remote control for common functions
* Fork installer
* Fingerprint V2 viewer
* SSH file explorer (view / edit / delete and upload files)
* SSH terminal with terminal emulation

Android app:

* SSH wizard to generate and install SSH keys
* Fork installer
It's fairly simple to setup and use, so this guide should be short. 

---
# Where to download Openpilot Toolkit

Openpilot Toolkit can be found and downloaded on spektor56's website here: 
https://spektor56.github.io/OpenpilotToolkit/
Or on GitHub here: 
https://github.com/spektor56/OpenpilotToolkit

I'll be walking through how to set it up on windows. 

---
# How to Install Openpilot Toolkit

When you download Openpilot Toolkit, it will be in a .zip file. Inside of that .zip is a folder labeled "OpenpilotToolkit". You can simply drag and drop this folder anywhere you like, or simply extract the zip as it is. There is no install process, just an OpenpilotToolkit.exe that runs inside of the OpenpilotToolkit folder. I place my OpenpilotToolkit folder in my computers Documents folder, and drag the OpenpilotToolkit.exe onto my taskbar so it creates a shortcut for easy access. 

---
# How to use Openpilot Toolkit

I would recommend powering on and connecting your openpilot device (henceforth called a Comma 3X) to the same network your computer is on at this point.

When you first launch OpenpilotToolkit.exe, Windows may ask you if you want to grant OpenpilotToolkit.exe firewall access. I would recommend allowing it so Openpilot Toolkit can connect to your Comma 3X. 

#### Start SSH wizard

Once you allow firewall access, and you Comma 3X is powered on and connected to your network, you may see a prompt from Openpilot Toolkit that says:

> 1 device(s) found but authentication failed, do you want to start the SSH wizard?

Click yes. 

It will now bring you to the SSH wizard tab on the left. 
The first page should be asking you to input your GitHub username and click Login. 
(Note: if you do not have a GitHub account, I would recommend opening up a different browser and creating an account there, since the information on the OPTK browser does not save information and may be harder to use than your default browser)
When you do, it will forward you to the GitHub login page with your username already pre-entered. 
(Note: changing your username in this window will cause an error in Openpilot Toolkit. If you need to correct your username, you will need to correct it in Openpilot Toolkit first, and then click Login to attempt again)

#### Generating an SSH key

Once logged in, you will be moved over to the next page that will ask you what key algorithm you would like to use. If this does not matter to you, then simply click "Generate new SSH key".
Once you do, it will generate an opensshkey file that will be linked to your GitHub account, and the file *should* be placed in both the OpenpilotToolkit folder, as well as you system32 folder. If the file is not in both locations, OPTK will not connect to your Comma 3X.

#### Enable SSH on your Comma 3X

Once you've generated your SSH key on OPTK, your Comma 3X is ready to receive you SSH key.
On your Comma 3X, go into the developer menu in sunnypilot (typically at the very bottom, you may have to scroll), you should see an option to enable SSH and to enter you're GitHub username, do both. If done correctly, you should see your GitHub username near the button clicked to enter your username. The device will let you know if it could not find the username you entered, so if there was no error prompt when you entered your username, then that means it now has your SSH key.
(Note: if you generated a new SSH key, you should remove the GitHub username from the Comma 3X and re-enter it so it grabs the newly generated key)

#### Connecting to your device from OPTK

Now that your opensshkey is on your computer, and your device has SSH enabled with your username entered, you should be able to connect to OPTK to your device. On OPTK, you should see a button on the top right that says "Scan for OP devices". Now, after a few seconds, in the Active Devices drop down menu, you should see it change from "Openpilot Devices" to an IP address with your devices name next to it. You should also see all of your routes populate in the video player if you've driven with the device already. 

# Done
You should be connected at this point. If you have any issues, let us know so we can try to help you. 
Also thanks to @spektor56 ([GitHub](https://github.com/spektor56)) for creating and maintaining OPTK.
