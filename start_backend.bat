@echo off
title SafeRoad AI Backend Server
echo Starting SafeRoad AI Machine Learning Backend...
cd /d "%~dp0"
py backend\app.py
pause
