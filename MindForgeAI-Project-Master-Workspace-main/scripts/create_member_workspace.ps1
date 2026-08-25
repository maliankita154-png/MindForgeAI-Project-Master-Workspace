param([Parameter(Mandatory=$true)][string]$StudentId)
$safeId = $StudentId.Trim().ToUpper() -replace '[^A-Z0-9_-]', ''
if (-not $safeId) { throw "Enter a valid student ID." }
$root = Split-Path -Parent $PSScriptRoot
$target = Join-Path $root "04_active_workspaces/${safeId}_current_working_folder"
New-Item -ItemType Directory -Force -Path $target | Out-Null
@("notes", "notebooks", "code", "evidence", "scratch") | ForEach-Object { New-Item -ItemType Directory -Force -Path (Join-Path $target $_) | Out-Null }
Write-Host "Member workspace ready: $target"
Write-Host "Copy the student's current working folder contents here, then create a member branch before editing shared work."
