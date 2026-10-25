param(
    [string]$SourceDir = "F:\DEV\ethereal-desktop\dist\ETHEREAL-win32-x64",
    [string]$TargetDir = "C:\Users\hp\OneDrive\Desktop\ETHEREAL"
)

Write-Host "Deploying packaged Electron app to Desktop ($TargetDir)..."
if (Test-Path $TargetDir) {
    Remove-Item -Recurse -Force $TargetDir
}
Copy-Item -Recurse -Force $SourceDir $TargetDir

$exePath = Join-Path $TargetDir "ETHEREAL.exe"

# Copy logo branding files for easy user access
Copy-Item "F:\DEV\ethereal-desktop\build\icon.ico" (Join-Path $TargetDir "icon.ico")
Copy-Item "F:\DEV\ethereal-desktop\build\icon.png" (Join-Path $TargetDir "icon.png")
Copy-Item "F:\DEV\ethereal-desktop\build\icon.svg" (Join-Path $TargetDir "icon.svg")

$desktops = @(
    [Environment]::GetFolderPath("Desktop"),
    "C:\Users\hp\Desktop"
) | Select-Object -Unique

$wsh = New-Object -ComObject WScript.Shell

foreach ($d in $desktops) {
    if (Test-Path $d) {
        $lnkPath = Join-Path $d "ETHEREAL.lnk"
        Write-Host "Creating desktop shortcut at $lnkPath"
        $shortcut = $wsh.CreateShortcut($lnkPath)
        $shortcut.TargetPath = $exePath
        $shortcut.WorkingDirectory = $TargetDir
        $shortcut.IconLocation = "$exePath,0"
        $shortcut.Description = "ETHEREAL // Sleeper Build Protocol"
        $shortcut.Save()
    }
}

Write-Host "Desktop app deployed successfully!"
