#Requires -Version 5.1
# install.ps1 — Install the AI SDLC Toolkit on Windows (PowerShell native).
# Idempotent: safe to re-run.  Does not overwrite user content outside managed blocks.
# Usage: .\install.ps1  (optionally set $env:TOOLKIT_HOME before running)
Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$DefaultHome = if ($env:TOOLKIT_HOME) { $env:TOOLKIT_HOME } `
               else { Join-Path $env:USERPROFILE '.copilot\ai-sdlc-toolkit' }
$ToolkitHome  = $DefaultHome
$CopilotHome  = Join-Path $env:USERPROFILE '.copilot'
$VersionFile  = Join-Path $ScriptDir 'VERSION'
$Version      = if (Test-Path $VersionFile) { Get-Content $VersionFile -Raw } else { 'unknown' }
$Version      = $Version.Trim()

Write-Host "==> Installing AI SDLC Toolkit v$Version -> $ToolkitHome"

# Create directories.
@($ToolkitHome, (Join-Path $CopilotHome '.github')) | ForEach-Object {
    New-Item -ItemType Directory -Force -Path $_ | Out-Null
}

# Copy toolkit files (exclude .git, node_modules, .DS_Store).
$exclude = @('.git', 'node_modules', '.DS_Store', 'install.ps1')
Get-ChildItem -Path $ScriptDir | Where-Object { $_.Name -notin $exclude } | ForEach-Object {
    $dest = Join-Path $ToolkitHome $_.Name
    if ($_.PSIsContainer) {
        Copy-Item -Path $_.FullName -Destination $dest -Recurse -Force
    } else {
        Copy-Item -Path $_.FullName -Destination $dest -Force
    }
}

# Resolve manifest template.
$tpl = Join-Path $ToolkitHome 'manifest.json.tpl'
if (Test-Path $tpl) {
    (Get-Content $tpl -Raw) -replace '__TOOLKIT_HOME__', $ToolkitHome |
        Set-Content (Join-Path $ToolkitHome 'manifest.json')
}

# Managed-block helper.
function Write-ManagedBlock {
    param([string]$Target, [string]$Body)
    $begin = "<!-- AI-SDLC-TOOLKIT:BEGIN version=`"$Version`" -->"
    $end   = '<!-- AI-SDLC-TOOLKIT:END -->'
    $block = "$begin`n$Body`n$end"
    if (-not (Test-Path $Target)) {
        Set-Content -Path $Target -Value $block -Encoding UTF8
        return
    }
    $content = Get-Content $Target -Raw
    if ($content -match 'AI-SDLC-TOOLKIT:BEGIN') {
        $pattern = '(?s)<!-- AI-SDLC-TOOLKIT:BEGIN[^>]*-->.*?<!-- AI-SDLC-TOOLKIT:END -->'
        $content = [regex]::Replace($content, $pattern, $block)
        Set-Content -Path $Target -Value $content -Encoding UTF8
    } else {
        Add-Content -Path $Target -Value "`n$block" -Encoding UTF8
    }
}

# Detect installed AI CLIs.
function Test-Cli { param([string]$Name); return [bool](Get-Command $Name -ErrorAction SilentlyContinue) }
$HasClaude = Test-Cli 'claude'
$HasGemini = Test-Cli 'gemini'
$HasCodex  = Test-Cli 'codex'

Write-Host "==> Detected AI CLIs:"
Write-Host ("    [{0}] claude (Claude Code){1}" -f $(if ($HasClaude) {'yes'} else {' no'}), $(if (-not $HasClaude) {' — CLAUDE.md will be skipped'} else {''}))
Write-Host ("    [{0}] gemini (Gemini CLI){1}"  -f $(if ($HasGemini) {'yes'} else {' no'}), $(if (-not $HasGemini) {' — GEMINI.md will be skipped'} else {''}))
Write-Host ("    [{0}] codex  (Codex CLI){1}"   -f $(if ($HasCodex)  {'yes'} else {' no'}), $(if (-not $HasCodex)  {' — CODEX.md will be skipped'}  else {''}))
Write-Host "    [yes] copilot-instructions — always included"

$AgentsBody = @"
# AI SDLC Toolkit Agent Guidance

The toolkit is installed at `$env:TOOLKIT_HOME (default: $ToolkitHome).

For project work, link a repo with:
  $ToolkitHome\link-to-project.ps1 C:\path\to\repo

Then start every task by checking:
1. .ai-sdlc/project-profile.yaml
2. .ai-sdlc/project-context.md
3. .github/skills/using-agent-skills/SKILL.md
4. The task-specific skill under .github/skills/
5. The relevant persona under .github/agents/

Do not mutate the toolkit directory from a project task. Use override folders.
"@

$CopilotBody = @"
# AI SDLC Toolkit

Global toolkit installed at `$env:TOOLKIT_HOME (default: ~\.copilot\ai-sdlc-toolkit).

Discovery paths (when linked to a project):
- Agents: .github/agents/
- Skills: .github/skills/
- Prompts: .github/prompts/
- Instructions: .github/instructions/

Run link-to-project.ps1 from your toolkit install to wire a repo.
"@

Write-ManagedBlock (Join-Path $CopilotHome 'AGENTS.md') $AgentsBody
if ($HasClaude) { Write-ManagedBlock (Join-Path $CopilotHome 'CLAUDE.md') $AgentsBody }
if ($HasGemini) { Write-ManagedBlock (Join-Path $CopilotHome 'GEMINI.md') $AgentsBody }
if ($HasCodex)  { Write-ManagedBlock (Join-Path $CopilotHome 'CODEX.md')  $AgentsBody }
Write-ManagedBlock (Join-Path $CopilotHome '.github\copilot-instructions.md') $CopilotBody

# Wire up agents/skills/prompts/instructions under ~/.copilot/.github/ via junctions/copies.
$domains = @(
    @{ Active = '.github\agents';       Source = 'agents' },
    @{ Active = '.github\skills';       Source = 'skills' },
    @{ Active = '.github\prompts';      Source = 'prompts' },
    @{ Active = '.github\instructions'; Source = 'instructions' }
)

# Prefer directory junctions (no elevation needed on Windows).
function Install-Link {
    param([string]$Source, [string]$Dest)
    if (Test-Path $Dest) { Remove-Item $Dest -Recurse -Force }
    try {
        # Directory junction — no admin required.
        New-Item -ItemType Junction -Path $Dest -Target $Source | Out-Null
    } catch {
        Copy-Item -Path $Source -Destination $Dest -Recurse -Force
    }
}

foreach ($d in $domains) {
    $src  = Join-Path $ToolkitHome $d.Source
    $dest = Join-Path $CopilotHome $d.Active
    if (Test-Path $src) {
        New-Item -ItemType Directory -Force -Path (Split-Path $dest) | Out-Null
        Install-Link $src $dest
        Write-Host "  linked $($d.Active)"
    }
}

Write-Host "==> Install complete."
Write-Host "    Toolkit:      $ToolkitHome"
Write-Host "    Link a project:  $ToolkitHome\link-to-project.ps1 C:\path\to\repo"
