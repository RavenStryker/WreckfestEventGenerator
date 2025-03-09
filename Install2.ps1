Set-ExecutionPolicy Bypass -Scope Process -Force
$WarningPreference = "SilentlyContinue"

# Function to run a command and handle errors
function Run-Command {
    param (
        [string]$Command
    )
    Write-Host "Running: $Command"
    try {
        Invoke-Expression $Command
    } catch {
        Write-Host "Error occurred while executing: $Command"
        Write-Host "Error details: $_"
    }
}

# Check Python Version
Write-Host "Checking Python Version..."
Run-Command "python --version"
Start-Sleep -Seconds 3

# Install pip 
Write-Host "Downloading pip and upgrading to latest version..."
Run-Command "py -m ensurepip --upgrade"
Run-Command "py -m pip install --upgrade pip"
Write-Host "Download & Upgrade Complete!"
Start-Sleep -Seconds 3

# Check pip Version
Write-Host "Checking pip Version..."
Run-Command "pip --version"
Start-Sleep -Seconds 3

# Install pywin32
Write-Host "Downloading pywin32"
Run-Command "pip install pywin32"
Write-Host "Download Complete!"
Start-Sleep -Seconds 3

# Check pywin32 Version
Write-Host "Checking Pywin32 Version..."
Run-Command "python -m pip show pywin32"
Start-Sleep -Seconds 3

# Install Pillow
Write-Host "Downloading Pillow..."
Run-Command "pip install Pillow"
Write-Host "Download Complete!"
Start-Sleep -Seconds 3

# Check Pillow Version
Write-Host "Checking Pillow Version..."
Run-Command "pip show pillow"
Start-Sleep -Seconds 5

# Pause to allow user to read final messages
Write-Host "Installation Complete! Please check for any errors above if they exist..."
Pause