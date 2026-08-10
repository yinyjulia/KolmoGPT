$ErrorActionPreference = "Continue"

Set-Location "G:\twitch\bot"

Write-Host "========================================"
Write-Host "       SUBIENDO PROYECTO A GITHUB"
Write-Host "========================================"
Write-Host ""

Write-Host "[1/4] Estado del repositorio..."
git status

Write-Host ""
Write-Host "[2/4] Añadiendo cambios..."
git add .

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "ERROR: git add fallo."
    Read-Host "Pulsa Enter para cerrar"
    exit
}

Write-Host ""
Write-Host "[3/4] Creando commit..."
git commit -m "Actualizacion del proyecto"

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "AVISO: No se creo un commit nuevo."
    Write-Host "Puede que no haya cambios."
}

Write-Host ""
Write-Host "[4/4] Subiendo a GitHub..."
git push

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

Write-Host ""
Write-Host "Estado final:"
git status

Write-Host ""
Read-Host "Pulsa Enter para cerrar"