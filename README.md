# Wreckfest Event Generator
Summary: A python gui interface that allows you to more easily generate server configurations for Wreckfest.
<br><br>
## Installation
Simply download the code into a .zip as shown in the image below.  
![image](https://github.com/user-attachments/assets/abb96543-bd83-47f4-837c-c7813193a0b4)
<br><br>
Once downloaded, extract it to your desktop, if you want to store it in a different location, you'll need to change the location `%userprofile%\Desktop\WreckfestEventGenerator\corefiles\` in the `Target` and `Start in` of the WEG shortcut to where you want your files to reside.    
```
Target: %localappdata%\Programs\Python\Python311\pythonw.exe "%userprofile%\Desktop\WreckfestEventGenerator\corefiles\WEG.py"
Start in: "%userprofile%\Desktop\WreckfestEventGenerator\corefiles"
```  
Open the folder, then right click on `Install1.ps1` and select Run with PowerShell.
This will install the proper python version (3.11.9) and make sure it is set in your PATH.  
![image](https://github.com/user-attachments/assets/c62e6165-d820-43e8-8cbf-17ea95a06bce)
<br><br>
Once that window closes, preform the exact same steps but on `Install2.ps1`.  
This will install all the other requirements to run this gui properly.  
The time it will take to complete installation will vary based on your internet speed.  
![image](https://github.com/user-attachments/assets/9ced6cf6-3a06-4677-9934-78c7c11d5435)
<br><br>
Once everything above ha been completed, double click on `Event Generator.py` and it will launch after a few seconds.
Modify all the settings in the gui to your needs. All the official tracks have been sorted by time to group them by small, medium and large.
To remove tracks from your random events, navigate to the `track` folder and remove the tracks from the small, medium or large text files.
Once all the settings have been modified, click on the `Generate Config` button.  
![image](https://github.com/user-attachments/assets/8c5ab1c6-3bed-4380-a287-d297c618c172)
<br><br>
This will create a file called `initial_server_config.cfg` in the corefiles folder within the applications directory `WreckfestEventGenerator\corefiles`.  
Simply copy this file to your Wreckfest server location and override the default config that is already there.
Please note, that if you need to edit anything extra like the lobby countdown timer, quickplay settingss or ports, you'll still need to go into the .cfg and do that manually. This is simply to generate events with random lap ranges and some extra ability to adjust the points, and add admins/mods all fom within this config taking out 90% of the work.  
![image](https://github.com/user-attachments/assets/d9937e06-6b61-4bee-ad0c-f2a772e200ea)
