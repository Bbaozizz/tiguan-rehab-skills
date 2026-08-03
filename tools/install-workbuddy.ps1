[CmdletBinding()]
param(
    [string]$WorkBuddyHome = (Join-Path $HOME ".workbuddy"),
    [string]$SourceDir = "",
    [string]$Repository = "Bbaozizz/tiguan-rehab-skills",
    [string]$Ref = "main"
)

$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

$SkillNames = @(
    "tiguan-rehab",
    "tiguan-assessment-session-design",
    "tiguan-source-to-practice",
    "tiguan-practice-knowledge-base",
    "tiguan-service-ops",
    "tiguan-post-session-questioning",
    "tiguan-business-review"
)
$TempSource = $null
$StageDir = $null

function Remove-InstallerPath {
    param([string]$Path)

    if ($Path -and (Test-Path -LiteralPath $Path)) {
        Remove-Item -LiteralPath $Path -Recurse -Force
    }
}

try {
    if ($SourceDir) {
        if (-not (Test-Path -LiteralPath $SourceDir -PathType Container)) {
            throw "Source directory does not exist: $SourceDir"
        }
        $RepoRoot = (Resolve-Path -LiteralPath $SourceDir).Path
    }
    else {
        $TempSource = Join-Path ([System.IO.Path]::GetTempPath()) (
            "tiguan-workbuddy-source-" + [System.Guid]::NewGuid().ToString("N")
        )
        $Archive = Join-Path $TempSource "source.zip"
        $Extracted = Join-Path $TempSource "extracted"
        New-Item -ItemType Directory -Path $Extracted -Force | Out-Null

        Write-Host "Downloading $Repository@$Ref ..."
        Invoke-WebRequest `
            -UseBasicParsing `
            -Uri "https://codeload.github.com/$Repository/zip/$Ref" `
            -OutFile $Archive
        Expand-Archive -LiteralPath $Archive -DestinationPath $Extracted -Force

        $ExtractedRoots = @(Get-ChildItem -LiteralPath $Extracted -Directory)
        if ($ExtractedRoots.Count -ne 1) {
            throw "Downloaded archive has an unexpected layout."
        }
        $RepoRoot = $ExtractedRoots[0].FullName
    }

    foreach ($Name in $SkillNames) {
        $SkillFile = Join-Path $RepoRoot "skills/$Name/SKILL.md"
        if (-not (Test-Path -LiteralPath $SkillFile -PathType Leaf)) {
            throw "Invalid package: missing skills/$Name/SKILL.md"
        }
    }

    $TargetRoot = Join-Path $WorkBuddyHome "skills"
    New-Item -ItemType Directory -Path $TargetRoot -Force | Out-Null
    $StageDir = Join-Path $TargetRoot (
        ".tiguan-install." + [System.Guid]::NewGuid().ToString("N")
    )
    $NewRoot = Join-Path $StageDir "new"
    $BackupRoot = Join-Path $StageDir "backup"
    New-Item -ItemType Directory -Path $NewRoot -Force | Out-Null
    New-Item -ItemType Directory -Path $BackupRoot -Force | Out-Null

    foreach ($Name in $SkillNames) {
        Copy-Item `
            -LiteralPath (Join-Path $RepoRoot "skills/$Name") `
            -Destination (Join-Path $NewRoot $Name) `
            -Recurse `
            -Force
    }

    $InstalledNames = [System.Collections.Generic.List[string]]::new()
    try {
        foreach ($Name in $SkillNames) {
            $Target = Join-Path $TargetRoot $Name
            $Backup = Join-Path $BackupRoot $Name
            if (Test-Path -LiteralPath $Target) {
                Move-Item -LiteralPath $Target -Destination $Backup
            }
            Move-Item -LiteralPath (Join-Path $NewRoot $Name) -Destination $Target
            $InstalledNames.Add($Name)
        }

        foreach ($Name in $SkillNames) {
            $InstalledSkill = Join-Path $TargetRoot "$Name/SKILL.md"
            if (-not (Test-Path -LiteralPath $InstalledSkill -PathType Leaf)) {
                throw "Installation verification failed: $Name"
            }
        }
    }
    catch {
        Write-Warning "Installation failed. Restoring the previous WorkBuddy Skills."
        foreach ($Name in $InstalledNames) {
            $Target = Join-Path $TargetRoot $Name
            if (Test-Path -LiteralPath $Target) {
                Remove-Item -LiteralPath $Target -Recurse -Force
            }
        }
        foreach ($Name in $SkillNames) {
            $Backup = Join-Path $BackupRoot $Name
            if (Test-Path -LiteralPath $Backup) {
                Move-Item -LiteralPath $Backup -Destination (Join-Path $TargetRoot $Name)
            }
        }
        throw
    }

    Write-Host ""
    Write-Host "Installed Tguan Rehabilitation Skills for WorkBuddy:"
    foreach ($Name in $SkillNames) {
        Write-Host "- $Name"
    }
    Write-Host "Location: $TargetRoot"
    Write-Host "Next: refresh or restart WorkBuddy, then run /tiguan-rehab new user guide"
}
finally {
    Remove-InstallerPath -Path $StageDir
    Remove-InstallerPath -Path $TempSource
}
