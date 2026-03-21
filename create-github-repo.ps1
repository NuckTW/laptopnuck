$GITHUB_USER = "NuckTW"
$REPO_NAME = "laptopnuck"

Write-Host ""
Write-Host "需要 GitHub Personal Access Token (PAT)" -ForegroundColor Cyan
Write-Host "前往: https://github.com/settings/tokens/new" -ForegroundColor White
Write-Host "勾選 repo 權限，產生後貼在下方" -ForegroundColor White
Write-Host ""

$tokenPlain = Read-Host "請輸入 GitHub PAT"

$headers = @{
    Authorization = "Bearer $tokenPlain"
    Accept = "application/vnd.github+json"
}

$body = '{"name":"' + $REPO_NAME + '","description":"nuck001 - LAPTOP-Nuck OpenClaw Agent","private":false,"auto_init":false}'

Write-Host "`n建立 GitHub repo..." -ForegroundColor Yellow
try {
    $result = Invoke-RestMethod -Uri "https://api.github.com/user/repos" -Method Post -Headers $headers -Body $body -ContentType "application/json"
    Write-Host "  [OK] Repo 建立: $($result.html_url)" -ForegroundColor Green
} catch {
    $code = $_.Exception.Response.StatusCode.value__
    if ($code -eq 422) {
        Write-Host "  [!!] Repo 已存在，繼續推送..." -ForegroundColor Yellow
    } else {
        Write-Host "  [XX] 失敗: $_" -ForegroundColor Red
        exit 1
    }
}

Write-Host "`n推送 main branch..." -ForegroundColor Yellow
$repoUrl = "https://" + $GITHUB_USER + ":" + $tokenPlain + "@github.com/" + $GITHUB_USER + "/" + $REPO_NAME + ".git"
git remote set-url origin $repoUrl
git push -u origin main

if ($LASTEXITCODE -eq 0) {
    Write-Host "`n  [OK] 推送成功!" -ForegroundColor Green
    Write-Host "  https://github.com/$GITHUB_USER/$REPO_NAME" -ForegroundColor Cyan
    git remote set-url origin "https://github.com/$GITHUB_USER/$REPO_NAME.git"
} else {
    Write-Host "  [XX] 推送失敗" -ForegroundColor Red
}
