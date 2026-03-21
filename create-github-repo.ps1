# ============================================================
# 建立 GitHub repo "laptopnuck" 並推送
# 只需執行一次
# ============================================================

$GITHUB_USER = "NuckTW"
$REPO_NAME   = "laptopnuck"

Write-Host ""
Write-Host "需要 GitHub Personal Access Token (PAT)" -ForegroundColor Cyan
Write-Host "前往：https://github.com/settings/tokens/new" -ForegroundColor White
Write-Host "勾選 'repo' 權限，產生 token 後貼在下方" -ForegroundColor White
Write-Host ""

$token = Read-Host "請輸入 GitHub PAT" -AsSecureString
$tokenPlain = [Runtime.InteropServices.Marshal]::PtrToStringAuto(
    [Runtime.InteropServices.Marshal]::SecureStringToBSTR($token)
)

$headers = @{
    Authorization = "Bearer $tokenPlain"
    Accept        = "application/vnd.github+json"
    "X-GitHub-Api-Version" = "2022-11-28"
}

$body = @{
    name        = $REPO_NAME
    description = "nuck001 — LAPTOP-Nuck OpenClaw Agent"
    private     = $false
    auto_init   = $false
} | ConvertTo-Json

Write-Host "`n建立 GitHub repo..." -ForegroundColor Yellow
try {
    $result = Invoke-RestMethod -Uri "https://api.github.com/user/repos" `
        -Method Post -Headers $headers -Body $body -ContentType "application/json"
    Write-Host "  [OK] Repo 建立成功：$($result.html_url)" -ForegroundColor Green
} catch {
    $statusCode = $_.Exception.Response.StatusCode.value__
    if ($statusCode -eq 422) {
        Write-Host "  [!!] Repo 已存在，繼續推送..." -ForegroundColor Yellow
    } else {
        Write-Host "  [XX] 建立失敗：$_" -ForegroundColor Red
        exit 1
    }
}

# 設定 credential 並推送
Write-Host "`n推送 main branch..." -ForegroundColor Yellow
$env:GIT_ASKPASS = "echo"
$repoUrl = "https://${GITHUB_USER}:${tokenPlain}@github.com/${GITHUB_USER}/${REPO_NAME}.git"

git remote set-url origin $repoUrl
git push -u origin main

if ($LASTEXITCODE -eq 0) {
    Write-Host "`n  [OK] 推送成功！" -ForegroundColor Green
    Write-Host "  Repo URL: https://github.com/$GITHUB_USER/$REPO_NAME" -ForegroundColor Cyan
    # 還原 remote URL（移除 token）
    git remote set-url origin "https://github.com/$GITHUB_USER/$REPO_NAME.git"
} else {
    Write-Host "  [XX] 推送失敗" -ForegroundColor Red
}

# 清除 token
$tokenPlain = $null
