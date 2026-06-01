#Requires -Version 5.1
# link-to-project.ps1 — Wire a target repo to the AI SDLC Toolkit (Windows PowerShell).
# Usage: .\link-to-project.ps1 C:\path\to\repo
Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$ScriptDir   = Split-Path -Parent $MyInvocation.MyCommand.Path
$ToolkitHome = if ($env:TOOLKIT_HOME) { $env:TOOLKIT_HOME } else { $ScriptDir }
$Target      = if ($args.Count -gt 0) { $args[0] } else { Get-Location }
$Target      = (Resolve-Path $Target).Path
$Version     = (Get-Content (Join-Path $ToolkitHome 'VERSION') -Raw -ErrorAction SilentlyContinue) ?? 'unknown'
$Version     = $Version.Trim()

Write-Host "==> Linking $Target -> toolkit $ToolkitHome"

# Detect installed AI CLIs.
function Test-Cli { param([string]$Name); return [bool](Get-Command $Name -ErrorAction SilentlyContinue) }
$HasClaude = Test-Cli 'claude'
$HasGemini = Test-Cli 'gemini'
$HasCodex  = Test-Cli 'codex'

Write-Host "==> Detected AI CLIs:"
Write-Host ("    [{0}] claude (Claude Code){1}" -f $(if ($HasClaude) {'yes'} else {' no'}), $(if (-not $HasClaude) {' — CLAUDE.md / .claude/ will be skipped'} else {''}))
Write-Host ("    [{0}] gemini (Gemini CLI){1}"  -f $(if ($HasGemini) {'yes'} else {' no'}), $(if (-not $HasGemini) {' — GEMINI.md / .gemini/ will be skipped'} else {''}))
Write-Host ("    [{0}] codex  (Codex CLI){1}"   -f $(if ($HasCodex)  {'yes'} else {' no'}), $(if (-not $HasCodex)  {' — CODEX.md will be skipped'}             else {''}))
Write-Host "    [yes] copilot-instructions — always included"

# Create directory structure.
$dirs = @('.ai-sdlc', '.github', '.github\agents-overrides', '.github\skills-overrides',
          '.github\prompts-overrides', '.github\instructions-overrides')
foreach ($d in $dirs) {
    New-Item -ItemType Directory -Force -Path (Join-Path $Target $d) | Out-Null
}
if ($HasClaude) { New-Item -ItemType Directory -Force -Path (Join-Path $Target '.claude\commands') | Out-Null }
if ($HasGemini) { New-Item -ItemType Directory -Force -Path (Join-Path $Target '.gemini\commands') | Out-Null }

# Keep override folders non-empty for git.
foreach ($d in @('agents-overrides','skills-overrides','prompts-overrides','instructions-overrides')) {
    $keep = Join-Path $Target ".github\$d\.gitkeep"
    if (-not (Test-Path $keep)) { New-Item -ItemType File -Force -Path $keep | Out-Null }
}

# Managed-block helper.
function Write-ManagedBlock {
    param([string]$TargetFile, [string]$Body)
    $begin = "<!-- AI-SDLC-TOOLKIT:BEGIN version=`"$Version`" -->"
    $end   = '<!-- AI-SDLC-TOOLKIT:END -->'
    $block = "$begin`n$Body`n$end"
    New-Item -ItemType Directory -Force -Path (Split-Path $TargetFile) | Out-Null
    if (-not (Test-Path $TargetFile)) {
        Set-Content -Path $TargetFile -Value $block -Encoding UTF8
        return
    }
    $content = Get-Content $TargetFile -Raw
    if ($content -match 'AI-SDLC-TOOLKIT:BEGIN') {
        $pattern = '(?s)<!-- AI-SDLC-TOOLKIT:BEGIN[^>]*-->.*?<!-- AI-SDLC-TOOLKIT:END -->'
        $content = [regex]::Replace($content, $pattern, $block)
        Set-Content -Path $TargetFile -Value $content -Encoding UTF8
    } else {
        Add-Content -Path $TargetFile -Value "`n$block" -Encoding UTF8
    }
}

# Awareness file bodies — use generic paths, not machine-specific expansions.
$AgentsBody = @'
# AI SDLC Toolkit Agent Guidance

This repo is linked to the AI SDLC Toolkit
(default: ~/.copilot/ai-sdlc-toolkit; override: $TOOLKIT_HOME env var).

Start every task by checking:
1. .ai-sdlc/project-profile.yaml
2. .ai-sdlc/project-context.md
3. .github/skills/using-agent-skills/SKILL.md
4. The task-specific skill under .github/skills/
5. The relevant persona under .github/agents/

Load only what you need for the task. Do not load all agents and skills at once.

Project overrides under .github/*-overrides/ take precedence over global defaults.
Never edit toolkit files from a project task.
'@

$CopilotBody = @'
# AI SDLC Toolkit

This repository is linked to the global AI SDLC Toolkit.

Toolkit root: $TOOLKIT_HOME (default: ~/.copilot/ai-sdlc-toolkit)

## What Copilot Reads Automatically

- Global instructions: .github/copilot-instructions.md
- Slash commands (/spec, /plan, /build, ...): .github/prompts/
- Scoped instructions: .github/instructions/
- Project profile: .ai-sdlc/project-profile.yaml
- Project context: .ai-sdlc/project-context.md

## Agent and Skill Files

Agent personas (.github/agents/) and skill playbooks (.github/skills/) are
available but must be attached manually as context:
  #file:.github/agents/tech-lead.md
  #file:.github/skills/backend-engineering/SKILL.md

Note: @agent-name mentions are NOT supported — Copilot @ participants are
VS Code extensions, not file-based definitions.

## Rules

1. Follow the relevant skill before acting (attach as #file context).
2. Use the relevant agent persona for perspective (attach as #file context).
3. Project overrides under .github/*-overrides/ beat global defaults.
4. Do not edit global toolkit files from a project task.
'@

Write-ManagedBlock (Join-Path $Target 'AGENTS.md') $AgentsBody
if ($HasClaude) { Write-ManagedBlock (Join-Path $Target 'CLAUDE.md') $AgentsBody }
if ($HasGemini) { Write-ManagedBlock (Join-Path $Target 'GEMINI.md') $AgentsBody }
if ($HasCodex)  { Write-ManagedBlock (Join-Path $Target 'CODEX.md')  $AgentsBody }
Write-ManagedBlock (Join-Path $Target '.github\copilot-instructions.md') $CopilotBody

# Build link farms (directory junctions; copy fallback on failure).
function Install-Link {
    param([string]$Source, [string]$Dest)
    if (Test-Path $Dest) { Remove-Item $Dest -Recurse -Force }
    try {
        New-Item -ItemType Junction -Path $Dest -Target $Source | Out-Null
        return 'junction'
    } catch {
        Copy-Item -Path $Source -Destination $Dest -Recurse -Force
        return 'copy'
    }
}

$domains = @(
    @{ Active = '.github\agents';       Override = '.github\agents-overrides';       Source = 'agents' },
    @{ Active = '.github\skills';       Override = '.github\skills-overrides';       Source = 'skills' },
    @{ Active = '.github\prompts';      Override = '.github\prompts-overrides';      Source = 'prompts' },
    @{ Active = '.github\instructions'; Override = '.github\instructions-overrides'; Source = 'instructions' }
)

foreach ($d in $domains) {
    $activeDir   = Join-Path $Target $d.Active
    $overrideDir = Join-Path $Target $d.Override
    $globalDir   = Join-Path $ToolkitHome $d.Source
    New-Item -ItemType Directory -Force -Path $activeDir   | Out-Null
    New-Item -ItemType Directory -Force -Path $overrideDir | Out-Null

    # Collect names; override wins on collision.
    $names = @{}
    if (Test-Path $globalDir) {
        Get-ChildItem $globalDir | Where-Object { $_.Name -notlike '.*' } | ForEach-Object {
            $names[$_.Name] = $_.FullName
        }
    }
    if (Test-Path $overrideDir) {
        Get-ChildItem $overrideDir | Where-Object { $_.Name -ne '.gitkeep' -and $_.Name -notlike '.*' } | ForEach-Object {
            $names[$_.Name] = $_.FullName
        }
    }

    foreach ($entry in $names.GetEnumerator()) {
        $dest = Join-Path $activeDir $entry.Key
        $mode = Install-Link $entry.Value $dest
        Write-Host "  $($d.Active)\$($entry.Key) [$mode]"
    }
}

Write-Host "==> Link complete."
Write-Host "    Next: run $ToolkitHome\tune-project.ps1 $Target from inside your AI CLI."
