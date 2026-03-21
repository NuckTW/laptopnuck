$GITHUB_USER = "NuckTW"
$REPO_NAME = "laptopnuck"

Write-Host ""
Write-Host "GitHub Personal Access Token (PAT) required" -ForegroundColor Cyan
Write-Host "Go to: https://github.com/settings/tokens/new" -ForegroundColor White
Write-Host "Check 'repo' scope, generate token, paste below" -ForegroundColor White
Write-Host ""

$tokenPlain = Read-Host "Enter GitHub PAT"

$headers = @{
    Authorization = "Bearer $tokenPlain"
    Accept = "application/vnd.github+json"
}

$body = "{`"name`":`"$REPO_NAME`",`"description`":`"nuck001 - LAPTOP-Nuck OpenClaw Agent`",`"private`":false,`"auto_init`":false}"

Write-Host "`nCreating GitHub repo..." -ForegroundColor Yellow
try {
    $result = Invoke-RestMethod -Uri "https://api.github.com/user/repos" -Method Post -Headers $headers -Body $body -ContentType "application/json"
    Write-Host "  [OK] Repo created: $($result.html_url)" -ForegroundColor Green
} catch {
    $code = $_.Exception.Response.StatusCode.value__
    if ($code -eq 422) {
        Write-Host "  [!!] Repo already exists, continuing push..." -ForegroundColor Yellow
    } else {
        Write-Host "  [XX] Failed: $_" -ForegroundColor Red
        exit 1
    }
}

Write-Host "`nPushing main branch..." -ForegroundColor Yellow
$repoUrl = "https://" + $GITHUB_USER + ":" + $tokenPlain + "@github.com/" + $GITHUB_USER + "/" + $REPO_NAME + ".git"
git remote set-url origin $repoUrl
git push -u origin main

if ($LASTEXITCODE -eq 0) {
    Write-Host "`n  [OK] Push successful!" -ForegroundColor Green
    Write-Host "  https://github.com/$GITHUB_USER/$REPO_NAME" -ForegroundColor Cyan
    git remote set-url origin "https://github.com/$GITHUB_USER/$REPO_NAME.git"
} else {
    Write-Host "  [XX] Push failed" -ForegroundColor Red
}
