import os
import json
from dataclasses import dataclass
from typing import Optional
from .prompt import SYSTEM, build_user_prompt
from .research import ResearchBundle


@dataclass
class GeneratedEmail:
    prospect_email: str
    variant: str
    subject: str
    body: str
    reference: str
    model: str


def _stub_email(bundle: ResearchBundle, variant: str) -> dict:
    ref = bundle.references[0] if bundle.references else None
    if not ref:
        return {"error": "insufficient research"}
    return {
        "subject": f"Re: {ref.summary[:40]}",
        "body": (
            f"Hi {bundle.prospect.get('first_name', '')} — saw "
            f"{ref.summary.lower()}. We help teams like yours ship outbound at scale. "
            "Open to a 15-min look at how Acme Co handled this?"
        ),
        "reference_used": f"{ref.kind}:{ref.summary}",
    }


def _claude_email(prompt: str, model: str) -> dict:
    from anthropic import Anthropic  # noqa: WPS433
    client = Anthropic()
    msg = client.messages.create(
        model=model, max_tokens=400, system=SYSTEM,
        messages=[{"role": "user", "content": prompt}],
    )
    text = msg.content[0].text.strip()
    s, e = text.find("{"), text.rfind("}")
    return json.loads(text[s:e + 1])


def generate(
    bundle: ResearchBundle,
    offer: dict,
    variants: list[str],
    model: Optional[str] = None,
    classify_fn=None,
) -> list[GeneratedEmail]:
    model = model or os.environ.get("LLM_MODEL", "claude-haiku-4-5-20251001")
    out: list[GeneratedEmail] = []
    for v in variants:
        prompt = build_user_prompt(offer, bundle, v)
        if classify_fn is not None:
            d = classify_fn(prompt, model)
        elif os.environ.get("ANTHROPIC_API_KEY"):
            d = _claude_email(prompt, model)
        else:
            d = _stub_email(bundle, v)
        if d.get("error"):
            continue
        out.append(GeneratedEmail(
            prospect_email=bundle.prospect.get("email", ""),
            variant=v,
            subject=d.get("subject", ""),
            body=d.get("body", ""),
            reference=d.get("reference_used", ""),
            model=model,
        ))
    return out
