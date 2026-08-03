[CmdletBinding()]
param(
    [string]$WorkBuddyHome = (Join-Path $HOME ".workbuddy"),
    [string]$SourceDir = "",
    [string]$Repository = "Bbaozizz/tiguan-rehab-skills",
    [string]$Ref = "main"
)

$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

$TempSource = $null
$StageDir = $null

function Remove-InstallerPath {
    param([string]$Path)

    if ($Path -and (Test-Path -LiteralPath $Path)) {
        Remove-Item -LiteralPath $Path -Recurse -Force
    }
}

function Assert-TargetWithinSkillsRoot {
    param([string]$Root, [string]$Target)

    $ResolvedRoot = (Resolve-Path -LiteralPath $Root).Path.TrimEnd('\', '/')
    if (Test-Path -LiteralPath $Target) {
        $ResolvedTarget = (Resolve-Path -LiteralPath $Target).Path
    }
    else {
        $ResolvedTarget = [System.IO.Path]::GetFullPath($Target)
    }
    $Prefix = $ResolvedRoot + [System.IO.Path]::DirectorySeparatorChar
    if (-not $ResolvedTarget.StartsWith($Prefix, [System.StringComparison]::OrdinalIgnoreCase)) {
        throw "Refusing target outside Skills root: $ResolvedTarget"
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

    $ManifestPath = Join-Path $RepoRoot ".claude-plugin/plugin.json"
    if (-not (Test-Path -LiteralPath $ManifestPath -PathType Leaf)) {
        throw "Invalid package: missing .claude-plugin/plugin.json"
    }
    $Manifest = Get-Content -LiteralPath $ManifestPath -Raw | ConvertFrom-Json
    $SkillNames = @($Manifest.skills)
    if ($SkillNames.Count -eq 0) {
        throw "Invalid package: .claude-plugin/plugin.json declares no skills"
    }
    foreach ($Name in $SkillNames) {
        if ($Name -isnot [string] -or $Name -notmatch '^\./skills/[a-z0-9]+(?:-[a-z0-9]+)*$') {
            throw "Invalid package: malformed published Skill path"
        }
    }
    $SkillNames = @($SkillNames | ForEach-Object { $_.Substring("./skills/".Length) })
    if (@($SkillNames | Select-Object -Unique).Count -ne $SkillNames.Count) {
        throw "Invalid package: duplicate published Skill ID"
    }
    $PrimaryRoutes = @($Manifest.primaryRoutes)
    if ($PrimaryRoutes.Count -ne 5 -or @($PrimaryRoutes | Select-Object -Unique).Count -ne 5) {
        throw "Invalid package: primaryRoutes must contain exactly five unique IDs"
    }
    foreach ($Route in $PrimaryRoutes) {
        if ($Route -notin $SkillNames) {
            throw "Invalid package: undeclared primaryRoutes ID: $Route"
        }
    }

    foreach ($Name in $SkillNames) {
        $SkillFile = Join-Path $RepoRoot "skills/$Name/SKILL.md"
        if (-not (Test-Path -LiteralPath $SkillFile -PathType Leaf)) {
            throw "Invalid package: missing skills/$Name/SKILL.md"
        }
    }

    $TargetRoot = Join-Path $WorkBuddyHome "skills"
    New-Item -ItemType Directory -Path $TargetRoot -Force | Out-Null
    $TargetRoot = (Resolve-Path -LiteralPath $TargetRoot).Path
    $StageDir = Join-Path $TargetRoot (
        ".tiguan-install." + [System.Guid]::NewGuid().ToString("N")
    )
    $NewRoot = Join-Path $StageDir "new"
    $BackupRoot = Join-Path $StageDir "backup"
    New-Item -ItemType Directory -Path $NewRoot -Force | Out-Null
    New-Item -ItemType Directory -Path $BackupRoot -Force | Out-Null

    foreach ($Name in $SkillNames) {
        Assert-TargetWithinSkillsRoot -Root $TargetRoot -Target (Join-Path $TargetRoot $Name)
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
            Assert-TargetWithinSkillsRoot -Root $TargetRoot -Target $Target
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
