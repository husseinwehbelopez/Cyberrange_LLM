# Simple example runner for Atomic Red Team in the lab
# Run inside the 'redteam' container.

Import-Module Invoke-AtomicRedTeam

# Use your local cloned atomics if desired:
$env:PathToAtomicsFolder = "/opt/redteam/atomic-red-team/atomics"

Write-Host "Checking prerequisites for a small sample of techniques..." -ForegroundColor Cyan

# Example technique IDs *for lab only* – you should choose ones appropriate to your OS
$techniques = @(
    "T1059.003", # Command and Scripting Interpreter: Windows Command Shell (if you target Windows lab hosts)
    "T1047"      # Windows Management Instrumentation (again, if using Windows hosts)
)

foreach ($t in $techniques) {
    Write-Host "=== Technique $t ===" -ForegroundColor Yellow
    try {
        Invoke-AtomicTest $t -CheckPrereqs
    } catch {
        Write-Warning "Failed CheckPrereqs for $t : $_"
    }
}

Write-Host "`nTo execute tests locally on a lab endpoint, you can run for example:" -ForegroundColor Cyan
Write-Host "Invoke-AtomicTest T1059.003 -ShowDetailsBrief" -ForegroundColor Green
Write-Host "`nMake sure you *only* run tests on systems you own and fully control."

