
:: Generate with default settings
ltx generate --prompt "A futuristic city in the clouds"

:: Generate with 'fast' preset for quick preview
ltx generate --preset fast --prompt "A red apple on a table" --output preview.mp4

:: Generate with custom config file
ltx generate --config examples/example.yaml --prompt "Sunset over mountains"

:: check recommended preset
ltx info

:: Dry run to check VRAM usage
ltx generate --dry-run --preset quality --prompt "Test quality"
