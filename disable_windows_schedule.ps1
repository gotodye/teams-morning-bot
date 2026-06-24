# Remove local Windows scheduled task (use cloud schedule instead)
$taskName = "Teams Morning Bot Schedule"
$existing = Get-ScheduledTask -TaskName $taskName -ErrorAction SilentlyContinue
if ($existing) {
    Unregister-ScheduledTask -TaskName $taskName -Confirm:$false
    Write-Host "[OK] Removed: $taskName" -ForegroundColor Green
}
else {
    Write-Host "[INFO] Task not found: $taskName" -ForegroundColor Yellow
}
Write-Host "Cloud schedule: see docs/cloud_schedule.md" -ForegroundColor Gray
