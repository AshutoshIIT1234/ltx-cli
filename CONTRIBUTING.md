# Contributing to LTX CLI

Thanks for your interest in contributing! 🎉

## How to Contribute

### 1. Fork & Clone
```bash
git clone https://github.com/AshutoshIIT1234/ltx-cli.git
cd ltx-cli
```

### 2. Set Up Development Environment
```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

pip install -e ".[dev]"
```

### 3. Make Your Changes
- Create a new branch: `git checkout -b feature/my-feature`
- Write clean, readable code
- Add comments where non-obvious

### 4. Submit a Pull Request
- Push your branch and open a PR against `main`
- Describe **what** you changed and **why**
- Link any related issues

## What We're Looking For

- 🐛 **Bug fixes** — always welcome
- 📝 **Documentation** — README, docstrings, examples
- ⚡ **New presets** — tested on real hardware
- 🧪 **Tests** — unit tests for utils, config merging, etc.
- 🔧 **CLI improvements** — new flags, better error messages

## Code Style

- Follow [PEP 8](https://peps.python.org/pep-0008/)
- Use type hints where possible
- Keep functions small and focused

## Reporting Issues

Please include:
- Your OS and Python version
- GPU model and VRAM (if relevant)
- Full error traceback
- Steps to reproduce

## Code of Conduct

Be respectful. Be constructive. We're all here to build something useful.
