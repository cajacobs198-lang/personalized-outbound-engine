import json
import yaml
import pandas as pd
import click
from pathlib import Path
from .research import gather
from .generate import generate
from .exporters import to_generic_csv, to_smartlead_csv, to_apollo_csv


@click.command()
@click.option("--prospects", required=True, type=click.Path(exists=True))
@click.option("--offer", "offer_path", required=True, type=click.Path(exists=True))
@click.option("--variants", default=3, show_default=True)
@click.option("--out", "out_path", default="emails.csv", show_default=True)
@click.option("--format", "fmt", type=click.Choice(["generic", "smartlead", "apollo"]), default="generic")
def generate_cmd(prospects: str, offer_path: str, variants: int, out_path: str, fmt: str):
    offer = yaml.safe_load(Path(offer_path).read_text())
    df = pd.read_csv(prospects).fillna("")
    # JSON-decode the optional mock signals if present
    for col in ("_mock_blog_posts", "_mock_jobs", "_mock_news"):
        if col in df.columns:
            df[col] = df[col].apply(lambda s: json.loads(s) if s else [])
    variant_labels = ["A", "B", "C"][:variants]
    all_emails = []
    for prospect in df.to_dict(orient="records"):
        bundle = gather(prospect, offer.get("sources", ["blog_rss", "jobs_page", "news"]))
        all_emails.extend(generate(bundle, offer, variant_labels))
    {"smartlead": to_smartlead_csv, "apollo": to_apollo_csv, "generic": to_generic_csv}[fmt](
        all_emails, out_path,
    )
    click.echo(f"wrote {len(all_emails)} emails to {out_path} ({fmt} format)")


cli = click.Group()
cli.add_command(generate_cmd, name="generate")

if __name__ == "__main__":
    cli()
