import time
import yaml
from pathlib import Path
from rich.console import Console
from rich.progress import Progress
import random
import torch

console = Console()

class LTXRunner:
    def __init__(self, config: dict, dry_run: bool = False):
        self.config = config
        self.dry_run = dry_run
        self.pipeline = None

    def initialize(self):
        """Load the model pipeline."""
        if self.dry_run:
            console.print("[yellow]Dry run: Skipping model load...[/yellow]")
            return

        precision_str = self.config.get('precision', 'bf16')
        torch_dtype = torch.bfloat16 if precision_str == 'bf16' else torch.float16
        
        console.print(f"[bold green]Loading LTX-2 model with precision {precision_str}...[/bold green]")
        
        try:
            from diffusers import LTXPipeline
        except ImportError:
            console.print("[bold red]Error: diffusers not installed. Please install it with `pip install diffusers`[/bold red]")
            raise

        # Load the pipeline
        # Using the official Lightricks/LTX-Video model ID
        self.pipeline = LTXPipeline.from_pretrained(
            "Lightricks/LTX-Video", 
            torch_dtype=torch_dtype
        ).to("cuda")

        # Optimization for lower VRAM if needed (optional)
        # self.pipeline.enable_model_cpu_offload()

    def generate(self, prompt: str, output_path: Path):
        """Run the generation process."""
        if self.dry_run:
            self._print_dry_run_stats(prompt, output_path)
            return

        console.print(f"[bold cyan]Generating video for prompt:[/bold cyan] '{prompt}'")
        
        if not self.pipeline:
             raise RuntimeError("Pipeline not initialized. Call initialize() first.")

        from diffusers.utils import export_to_video

        # Extract params
        steps = self.config.get("scheduler", {}).get("num_inference_steps", 30)
        guidance_scale = self.config.get("scheduler", {}).get("guidance_scale", 3.0)
        height = self.config.get("height", 720)
        width = self.config.get("width", 1280)
        frames_count = self.config.get("frames_per_chunk", 161) # 161 is often default for LTX, but let's use user config
        if frames_count < 8: frames_count = 16 # sanitize small defaults for testing
        
        # Run generation
        # Note: Depending on diffusers version, num_frames might be inferred or explicit.
        # Ideally we pass it if supported.
        output = self.pipeline(
            prompt=prompt,
            negative_prompt="low quality, worst quality",
            width=width,
            height=height,
            num_frames=frames_count,
            num_inference_steps=steps,
            guidance_scale=guidance_scale,
        )
        
        video_frames = output.frames[0]
        
        # Save output
        # Ensure output directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)
        export_to_video(video_frames, str(output_path), fps=24)
        
        # Save output metadata
        self._save_metadata(prompt, output_path)
        console.print(f"[bold green]Video saved to {output_path}[/bold green]")

    def _print_dry_run_stats(self, prompt: str, output_path: Path):
        """Display estimated resources and resolved config."""
        console.print("\n[bold]🧪 Dry Run Analysis[/bold]")
        console.print(f"Prompt: {prompt}")
        console.print(f"Output: {output_path}")
        
        # Estimate VRAM based on config (heuristic)
        width = self.config.get("width", 512)
        height = self.config.get("height", 512)
        frames = self.config.get("frames_per_chunk", 16)
        estimated_vram = (width * height * frames * 8) / (1024**3) # Rough estimate
        console.print(f"Estimated VRAM: ~{estimated_vram:.2f} GB")
        
        console.print("\n[bold]Resolved Configuration:[/bold]")
        console.print(yaml.dump(self.config))

    def _save_metadata(self, prompt: str, output_path: Path):
        """Save run metadata for reproducibility."""
        metadata = {
            "prompt": prompt,
            "preset": self.config.get("preset_name", "custom"),
            "timestamp": time.time(),
            "config": self.config
        }
        meta_path = output_path.with_suffix(".yaml")
        with open(meta_path, "w") as f:
            yaml.dump(metadata, f)
        console.print(f"[dim]Metadata saved to {meta_path}[/dim]")
