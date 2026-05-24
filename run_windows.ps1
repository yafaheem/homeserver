param(
    [int]$Port = 5000,
    [string]$UploadFolder = "$PSScriptRoot\uploads"
)

if (-not (Test-Path $UploadFolder)) {
    New-Item -ItemType Directory -Path $UploadFolder | Out-Null
}

$env:UPLOAD_FOLDER = $UploadFolder
$env:PORT = $Port

Write-Host "Starting homeserver on http://0.0.0.0:$Port/"
Write-Host "Uploads folder: $UploadFolder"
Write-Host "Press CTRL+C to stop."

python -m waitress --host=0.0.0.0 --port=$Port app:app
