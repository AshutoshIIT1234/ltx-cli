<p align="center">
  <h1 align="center">⚡ LTX CLI</h1>
  <p align="center">
    A reproducible command-line interface for running <a href="https://github.com/Lightricks/LTX-Video">LTX-2</a> video generation<br/>
    with presets, configs, and smart defaults.
  </p>
</p>

<p align="center">
  <a href="#installation"><img src="https://img.shields.io/badge/python-3.9+-blue.svg" alt="Python 3.9+"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-green.svg" alt="MIT License"></a>
  <a href="https://github.com/AshutoshIIT1234/ltx-cli/issues"><img src="https://img.shields.io/badge/contributions-welcome-orange.svg" alt="Contributions Welcome"></a>
</p>

---

## Why?

Running LTX-2 currently requires manual config tuning and fragile scripts.
This CLI makes experimentation **fast**, **reproducible**, and **beginner-friendly**.

| Problem | LTX CLI Solution |
| :--- | :--- |
| ❌ Manual config editing | ✅ One-command presets |
| ❌ Reproducibility issues | ✅ Auto-saved run configs |
| ❌ GPU OOM surprises | ✅ VRAM-aware presets |
| ❌ Hard onboarding | ✅ Single `ltx generate` command |

## Features

- 🎬 **One-command video generation** — `ltx generate --prompt "..."`
- 🧠 **VRAM-aware presets** — `fast`, `balanced`, `quality`, `low-vram`
- 💾 **Config export & reuse** — Save and replay exact configurations
- 📋 **Automatic run metadata** — Every run saves a reproducible YAML alongside output
- 🔍 **GPU auto-detection** — Detects your hardware and recommends the best preset
- 🧪 **Dry run mode** — Preview estimated VRAM and resolved config without running

## Installation

### From source (recommended for development)

```bash
git clone https://github.com/AshutoshIIT1234/ltx-cli.git
cd ltx-cli
pip install -e .
```

### From PyPI (coming soon)

```bash
pip install ltx-cli
```

### Requirements

- Python 3.9+
- CUDA-capable GPU (6GB+ VRAM recommended)
- [PyTorch](https://pytorch.org/) with CUDA support

## Quick Start

```bash
# List available presets
ltx presets

# Generate video with a preset
ltx generate \
  --preset balanced \
  --prompt "cinematic shot of rain in tokyo at night" \
  --output ./outputs/tokyo.mp4

# Check your GPU and recommended preset
ltx info

# Dry run — see estimated VRAM and resolved config
ltx generate --dry-run --preset quality --prompt "test prompt"

# Export a preset config to YAML
ltx export-config --preset quality --output myconfig.yaml

# Generate from a saved config
ltx generate --config myconfig.yaml --prompt "reuse this config"
```

## Presets

Presets abstract away complexity. Pick one and go:

| Preset | Use Case | VRAM Target | Speed | Resolution |
| :--- | :--- | :--- | :--- | :--- |
| `fast` | Quick preview | ~8 GB | ⚡⚡⚡ | 854×480 |
| `balanced` | Default / everyday | ~12 GB | ⚡⚡ | 1280×720 |
| `quality` | Best visuals | ~24 GB | ⚡ | 1920×1080 |
| `low-vram` | Laptop GPU | ~6 GB | ⚡⚡ | 640×384 |

Each preset maps to optimized values for:
- Resolution (width × height)
- Precision (`fp16` / `bf16`)
- Frames per chunk
- Inference steps & guidance scale

## Reproducibility

Every `ltx generate` run automatically saves a `.yaml` metadata file alongside your output:

```yaml
prompt: "cinematic shot of rain in tokyo at night"
preset: balanced
timestamp: 1707612345.678
config:
  height: 720
  width: 1280
  precision: bf16
  frames_per_chunk: 16
  scheduler:
    num_inference_steps: 30
    guidance_scale: 3.0
```

To reproduce any previous run:

```bash
ltx generate --config output.yaml
```

## GPU Auto-Detection

```
$ ltx info
System Information
GPU: NVIDIA GeForce RTX 3060
VRAM: 12.00 GB
Recommended Preset: balanced
```

If no preset is specified, LTX CLI automatically selects the best one for your hardware.

## Project Structure

```
ltx-cli/
├── ltx/
│   ├── __init__.py
│   ├── cli.py          # Typer CLI commands
│   ├── runner.py       # Pipeline loading & generation
│   ├── utils.py        # GPU detection, config helpers
│   └── presets.yaml    # Preset definitions
├── configs/            # User custom configs
├── examples/           # Example configs & scripts
├── CONTRIBUTING.md
├── LICENSE
├── README.md
└── pyproject.toml
```

## Contributing

Contributions are welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

Areas we'd love help with:
- 🧪 Unit tests
- ⚡ New presets tested on real hardware
- 📝 Documentation & tutorials
- 🐛 Bug reports with GPU details

## License

[MIT](LICENSE) — use it, fork it, build on it.

---

<p align="center">
  Built with ❤️ for the LTX-2 community
</p>
