$ErrorActionPreference = 'Stop'

$rootDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Push-Location $rootDir

try {
  $env:POETRY_KEYRING_ENABLED = 'false'

  if (-not (Get-Command npm -ErrorAction SilentlyContinue)) {
    throw 'npm is required but was not found in PATH.'
  }

  if (-not (Get-Command poetry -ErrorAction SilentlyContinue)) {
    throw 'poetry is required but was not found in PATH.'
  }

  if (Test-Path './nx.bat') {
    $useLocalNx = $true
  } else {
    $useLocalNx = $false
  }

  function Invoke-Nx {
    param([string[]] $Arguments)

    if ($useLocalNx) {
      & './nx.bat' @Arguments
      return
    }

    & npx nx @Arguments
  }

  Write-Host '[1/5] Installing Node dependencies...'
  npm install

  Write-Host '[2/5] Installing api-http Python dependencies...'
  Invoke-Nx @('run', 'api-http:install')

  Write-Host '[3/5] Running api-http tests...'
  Invoke-Nx @('run', 'api-http:test')

  Write-Host '[4/5] Installing API Python dependencies...'
  Invoke-Nx @('run', 'api:install')

  Write-Host '[5/5] Applying API migrations...'
  Invoke-Nx @('run', 'api:migrate')

  Write-Host ''
  Write-Host 'Setup completed successfully.'
  if ($useLocalNx) {
    Write-Host 'Start API server: ./nx.bat run api:runserver'
  } else {
    Write-Host 'Start API server: npx nx run api:runserver'
  }
}
finally {
  Pop-Location
}
