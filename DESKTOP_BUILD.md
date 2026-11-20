# Windows downloadable build

This branch creates a normal **one-folder** Windows build for itch.io instead of a self-extracting one-file executable.

## Why this layout

The downloadable build intentionally uses:

- PyInstaller **one-folder** mode
- **UPX disabled**
- a separate desktop entry point
- Windows version metadata
- a clean Python 3.12 virtual environment
- a ZIP containing the entire application folder

This does not guarantee that Microsoft Defender SmartScreen will never warn. Unsigned new executables can still have little or no reputation. For public Windows distribution, Authenticode signing is the strongest next step.

## Build locally on Windows

Requirements:

- Windows 10 or 11
- Python 3.12 x64
- PowerShell

From the repository root:

```powershell
powershell -ExecutionPolicy Bypass -File .\build_windows.ps1
```

The script creates:

```text
release/
  Deathdream-Windows.zip
  SHA256SUMS.txt
```

Upload **Deathdream-Windows.zip** to itch.io. Do not upload only `Deathdream.exe`; the executable needs the rest of its folder.

## Test before publishing

1. Extract `Deathdream-Windows.zip` into a new empty folder.
2. Run `Deathdream.exe`.
3. Play through the interactions that previously caused browser-specific issues.
4. Scan the extracted folder with Microsoft Defender.
5. Test the exact ZIP you plan to upload.

## If Defender reports a false positive

Submit the specific detected file to Microsoft's Security Intelligence file submission portal as a **software developer** and mark it as incorrectly detected:

https://www.microsoft.com/wdsi/filesubmission

Keep the submission ID and wait for Microsoft's determination before replacing the public download.

## Code signing

For a public itch.io download, a trusted Authenticode certificate is the best way to establish a consistent publisher identity across releases.

After obtaining a trusted code-signing certificate, sign the final executable **after building and before creating the ZIP**. Do not modify the executable after signing.

A typical SignTool command looks like:

```powershell
signtool sign /fd SHA256 /td SHA256 /tr http://timestamp.digicert.com /sha1 YOUR_CERTIFICATE_THUMBPRINT .\dist\Deathdream\Deathdream.exe
```

Then recreate the ZIP from the signed folder.

A self-signed certificate is useful for local testing but does not provide public SmartScreen reputation.
