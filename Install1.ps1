Set-ExecutionPolicy Bypass -Scope Process -Force
$WarningPreference = "SilentlyContinue"

# Downloading Python Notification
Write-Host "Downloading Python..."
Start-Sleep -Seconds 2

# Define the download URL and the destination
$pythonUrl = "https://www.python.org/ftp/python/3.11.9/python-3.11.9-amd64.exe"
$destination = "$env:TEMP\python_installer.exe"

# Download Python installer
Invoke-WebRequest -Uri $pythonUrl -OutFile $destination

# Installing Python Notification
Write-Host "Download Complete! Installing Python..."
Start-Sleep -Seconds 2

# Start installation
$process = Start-Process -FilePath "$destination" -ArgumentList "/quiet PrependPath=1" -PassThru

# Wait for the process to exit
$process.WaitForExit()

# Check the exit code to determine if the installation was successful
if ($process.ExitCode -eq 0) {
    Write-Host "Python installed successfully."
} else {
    Write-Host "Python installation failed with exit code: $($process.ExitCode)"
}

# Clean up the installer
Remove-Item -Path $destination -Force

# Installation Complete Notification
Write-Host "Installation Complete! Please run Install2.ps1 to complete installation process."

# Closes the Current Window
Start-Sleep -Seconds 5
