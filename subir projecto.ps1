# ========================================
# SUBIR PROYECTO A GITHUB
# ========================================

$ErrorActionPreference = "Continue"

# ========================================
# Configuración UTF-8
# ========================================

[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8

# ========================================
# Carpeta del proyecto
# ========================================

Set-Location "G:\twitch\bot"

Write-Host ""
Write-Host "========================================"
Write-Host "       SUBIENDO PROYECTO A GITHUB"
Write-Host "========================================"
Write-Host ""

# ========================================
# Comprobar Git
# ========================================

Write-Host "[1/5] Comprobando repositorio..."
git status

if ($LASTEXITCODE -ne 0) {

    Write-Host ""
    Write-Host "ERROR: No se ha encontrado un repositorio Git."
    Write-Host ""

    Read-Host "Pulsa Enter para cerrar"
    exit
}

# ========================================
# Añadir cambios
# ========================================

Write-Host ""
Write-Host "[2/5] Añadiendo cambios..."
git add .

if ($LASTEXITCODE -ne 0) {

    Write-Host ""
    Write-Host "ERROR: No se pudieron añadir los archivos."
    Write-Host ""

    Read-Host "Pulsa Enter para cerrar"
    exit
}

# ========================================
# Comprobar si hay cambios
# ========================================

Write-Host ""
Write-Host "[3/5] Comprobando cambios..."

git diff --cached --quiet

if ($LASTEXITCODE -eq 0) {

    Write-Host ""
    Write-Host "No hay cambios nuevos para guardar."

}
else {

    # ========================================
    # Commit
    # ========================================

    Write-Host ""
    Write-Host "Creando commit..."

    git commit -m "Actualizacion del proyecto"

    if ($LASTEXITCODE -ne 0) {

        Write-Host ""
        Write-Host "ERROR: No se pudo crear el commit."
        Write-Host ""

        Read-Host "Pulsa Enter para cerrar"
        exit
    }
}

# ========================================
# Comprobar remoto
# ========================================

Write-Host ""
Write-Host "[4/5] Comprobando GitHub..."

$Remoto = git remote get-url origin 2>$null

if (-not $Remoto) {

    Write-Host ""
    Write-Host "No existe el remoto origin."
    Write-Host "Añadiendo repositorio de KolmoGPT..."

    git remote add origin "https://github.com/yinyjulia/KolmoGPT.git"

    if ($LASTEXITCODE -ne 0) {

        Write-Host ""
        Write-Host "ERROR: No se pudo añadir origin."
        Write-Host ""

        Read-Host "Pulsa Enter para cerrar"
        exit
    }
}

# ========================================
# Subir a GitHub
# ========================================

Write-Host ""
Write-Host "[5/5] Subiendo a GitHub..."
Write-Host ""

git push -u origin main

if ($LASTEXITCODE -eq 0) {

    Write-Host ""
    Write-Host "========================================"
    Write-Host "       SUBIDA CORRECTAMENTE"
    Write-Host "========================================"

}
else {

    Write-Host ""
    Write-Host "========================================"
    Write-Host "          ERROR AL HACER PUSH"
    Write-Host "========================================"

}

# ========================================
# Estado final
# ========================================

Write-Host ""
Write-Host "Estado final:"
Write-Host ""

git status

Write-Host ""
Write-Host "========================================"
Write-Host "              TERMINADO"
Write-Host "========================================"
Write-Host ""

Read-Host "Pulsa Enter para cerrar"
