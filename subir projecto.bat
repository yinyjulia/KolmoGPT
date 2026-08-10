@echo off
title Subir proyecto a GitHub

cd /d G:\twitch\bot

echo ========================================
echo       SUBIENDO PROYECTO A GITHUB
echo ========================================
echo.

echo [1/4] Comprobando cambios...
git status

echo.
echo [2/4] Añadiendo archivos...
git add .

echo.
echo [3/4] Creando commit...
git commit -m "Actualizacion del proyecto"

echo.
echo [4/4] Subiendo a GitHub...
git push

echo.
echo ========================================
echo              TERMINADO
echo ========================================
echo.

pause