# Aethera release checksums

Use PowerShell to verify an archive before extracting it:

```powershell
Get-FileHash <archive-path> -Algorithm SHA256
```

| Archive | SHA-256 |
|---|---|
| `06_code/dist/aethera-deployment-0.1.0.zip` | `B8A4400AD34363070979FE515C18A8BA66BAA4C04767E3F676691BB3F71588D3` |
| `06_code/dist/aethera-complete-handoff-0.1.0.zip` | `9D93F1E06420EDEEAF9B1F7930E2C0D060274CD5C50BE2CCC5AB20694799E66A` |

The complete handoff archive includes the code, tests, Docker materials, project documentation, release lock and the separate execution-and-study centre.
