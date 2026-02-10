import typer
import yaml
import sys
from pathlib import Path
from rich.console import Console
from rich.table import Table
from typing import Optional

from .utils import load_presets, detect_vram, detect_gpu_name, recommend_preset, merge_configs
from .runner import LTXRunner

app = typer.Typer(
    help="LTX-2 CLI: Reproducible video generation made easy.",
    add_completion=False
)
console = Console()

PRESETS_PATH = Path(__file__).parent / "presets.yaml"

@app.command()
def generate(
    prompt: str = typer.Option(..., help="Text prompt for video generation"),
    preset: str = typer.Option(None, help="Preset configuration name (e.g., fast, balanced)"),
    frames: int = typer.Option(None, help="Number of frames to generate"),
    output: Path = typer.Option(Path("./output.mp4"), help="Output video path"),
    config: Path = typer.Option(None, help="Path to custom YAML config file"),
    dry_run: bool = typer.Option(False, "--dry-run", help="Simulate run without GPU usage"),
):
    """
    Generate video from text prompt using LTX-2.
    """
    presets = load_presets(PRESETS_PATH)
    
    # Auto-detect preset if not specified
    if not preset and not config:
        vram = detect_vram()
        recommended = recommend_preset(vram, presets)
        
        vram_display = f"{vram / (1024**3):.1f}GB" if vram else "N/A"
        console.print(f"[yellow]Auto-detected GPU VRAM: {vram_display}. Using recommended preset: {recommended}[/yellow]")
        preset = recommended
    
    # Load base config
    run_config = {}
    preset_name = "custom"
    
    if preset:
        if preset not in presets:
            console.print(f"[red]Error: Preset '{preset}' not found. Available: {', '.join(presets.keys())}[/red]")
            raise typer.Exit(code=1)
        run_config = presets[preset]["config"].copy()
        preset_name = preset

    # Override with custom config file
    if config:
        if not config.exists():
            console.print(f"[red]Error: Config file {config} not found.[/red]")
            raise typer.Exit(code=1)
        with open(config) as f:
            custom_conf = yaml.safe_load(f)
            run_config = merge_configs(run_config, custom_conf)
            preset_name = "custom_file"

    # Command line overrides
    if frames:
        run_config["frames_per_chunk"] = frames # Simplified mapping
    
    run_config["prompt"] = prompt
    run_config["preset_name"] = preset_name

    # Initialize Runner
    runner = LTXRunner(run_config, dry_run=dry_run)
    runner.initialize()
    runner.generate(prompt, output)

@app.command()
def presets():
    """
    List available configuration presets.
    """
    data = load_presets(PRESETS_PATH)
    table = Table(title="Available LTX-2 Presets")
    table.add_column("Name", style="cyan")
    table.add_column("VRAM Target", style="magenta")
    table.add_column("Description", style="green")
    
    for name, info in data.items():
        table.add_row(name, info.get("vram_target", "N/A"), info.get("description", ""))
    
    console.print(table)

@app.command()
def info():
    """
    Show system info and GPU capabilities.
    """
    console.print("[bold]System Information[/bold]")
    gpu_name = detect_gpu_name()
    vram = detect_vram()
    
    console.print(f"GPU: {gpu_name}")
    if vram:
        console.print(f"VRAM: {vram / (1024**3):.2f} GB")
        presets = load_presets(PRESETS_PATH)
        rec = recommend_preset(vram, presets)
        console.print(f"Recommended Preset: [green]{rec}[/green]")
    else:
        console.print("[yellow]No CUDA GPU detected.[/yellow]")

@app.command()
def export_config(
    preset: str = typer.Option(..., help="Preset to export"),
    output: Path = typer.Option(None, help="Output file path (default: stdout)")
):
    """
    Export a preset configuration to YAML.
    """
    presets = load_presets(PRESETS_PATH)
    if preset not in presets:
        console.print(f"[red]Error: Preset '{preset}' not found.[/red]")
        raise typer.Exit(code=1)
    
    config = presets[preset]["config"]
    yaml_str = yaml.dump(config, sort_keys=False)
    
    if output:
        with open(output, "w") as f:
            f.write(yaml_str)
        console.print(f"Config exported to {output}")
    else:
        print(yaml_str)

if __name__ == "__main__":
    app()
