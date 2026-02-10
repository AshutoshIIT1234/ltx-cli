import yaml
import sys
import os
from pathlib import Path
from typing import Dict, Any, Optional

try:
    import torch
except ImportError:
    torch = None

def detect_vram() -> Optional[int]:
    """Detect available VRAM in VRAM (bytes). Returns None if no GPU found."""
    if torch and torch.cuda.is_available():
        return torch.cuda.get_device_properties(0).total_memory
    return None

def detect_gpu_name() -> str:
    """Return the name of the detected GPU or 'CPU'."""
    if torch and torch.cuda.is_available():
        return torch.cuda.get_device_name(0)
    return "CPU"

def format_vram(vram_bytes: int) -> str:
    if vram_bytes is None:
        return "N/A"
    gb = vram_bytes / (1024 ** 3)
    return f"{gb:.1f}GB"

def load_presets(presets_path: Path) -> Dict[str, Any]:
    if not presets_path.exists():
        raise FileNotFoundError(f"Presets file not found at {presets_path}")
    
    with open(presets_path, "r") as f:
        data = yaml.safe_load(f)
        return data.get("presets", {})

def recommend_preset(vram_bytes: int, presets: Dict[str, Any]) -> str:
    """Recommend a preset based on available VRAM."""
    if vram_bytes is None:
        return "fast"  # Fallback for CPU/Testing
    
    vram_gb = vram_bytes / (1024 ** 3)
    
    # Simple logic based on user descriptions
    if vram_gb >= 22:
        return "quality"
    elif vram_gb >= 11:
        return "balanced"
    elif vram_gb >= 7:
        return "fast"
    else:
        return "low-vram"

def merge_configs(base_config: Dict, override_config: Dict) -> Dict:
    """Recursively merge dictionary configs."""
    result = base_config.copy()
    for key, value in override_config.items():
        if isinstance(value, dict) and key in result and isinstance(result[key], dict):
            result[key] = merge_configs(result[key], value)
        else:
            result[key] = value
    return result
