# Description: This script will install all the dependencies for the project

# check if python is installed else install it
if (Get-Command python -ErrorAction SilentlyContinue) {
    Write-Host "Python is installed"
} else {
    Write-Host "Python is not installed"
    Write-Host "Installing Python"
    # install python
    choco install python -y   
}

# check if pip is installed else install it
if (Get-Command pip -ErrorAction SilentlyContinue) {
    Write-Host "Pip is installed"
} else {
    Write-Host "Pip is not installed"
    Write-Host "Installing Pip"
    # install pip
    choco install pip -y
}

# check if discord.py is installed else install it
if (Get-Command discord -ErrorAction SilentlyContinue) {
    Write-Host "Discord.py is installed"
} else {
    Write-Host "Discord.py is not installed"
    Write-Host "Installing Discord.py"
    # install discord.py
    pip install discord.py
}

# check if python-dotenv is installed else install it
if (Get-Command python-dotenv -ErrorAction SilentlyContinue) {
    Write-Host "Python-dotenv is installed"
} else {
    Write-Host "Python-dotenv is not installed"
    Write-Host "Installing Python-dotenv"
    # install python-dotenv
    pip install python-dotenv
}

# check if selenium is installed else install it
if (Get-Command selenium -ErrorAction SilentlyContinue) {
    Write-Host "Selenium is installed"
} else {
    Write-Host "Selenium is not installed"
    Write-Host "Installing Selenium"
    # install selenium
    pip install selenium
}

# check if bs4 is installed else install it
if (Get-Command bs4 -ErrorAction SilentlyContinue) {
    Write-Host "BeautifulSoup4 is installed"
} else {
    Write-Host "BeautifulSoup4 is not installed"
    Write-Host "Installing BeautifulSoup4"
    # install bs4
    pip install bs4
}

# check if requests is installed else install it
if (Get-Command requests -ErrorAction SilentlyContinue) {
    Write-Host "Requests is installed"
} else {
    Write-Host "Requests is not installed"
    Write-Host "Installing Requests"
    # install requests
    pip install requests
}