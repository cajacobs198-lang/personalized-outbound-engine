SYSTEM = """You write cold outbound emails for B2B sales reps.
Rules:
1. Open with a concrete reference to the prospect (a specific job posting, blog
   post, news item, or quote). Never use vague flattery.
2. State the reason you're writing in one sentence.
3. Make a single, specific ask. No "thoughts?" or "interested?".
4. Maximum 90 words in the body.
5. If no concrete reference is available in RESEARCH, output exactly:
   {"error": "insufficient research"}.
Return JSON only: {"subject": "...", "body": "...", "reference_used": "..."}.
"""

VARIANT_STYLES = {
    "A": "Tight, professional, 3-4 sentence body.",
    "B": "Conversational, slightly playful, may include one rhetorical question.",
    "C": "Question-led: open with a thoughtful question tied to the reference.",
}


def build_user_prompt(offer: dict, bundle, variant: str) -> str:
    refs = "\n".join(
        f"- [{r.kind}] {r.summary}" + (f" ({r.url})" if r.url else "")
        for r in bundle.references
    ) or "(none)"
    return f"""PROSPECT:
name: {bundle.prospect.get('first_name', '')} {bundle.prospect.get('last_name', '')}
title: {bundle.prospect.get('title', '')}
company: {bundle.prospect.get('company', '')}

OFFER:
{offer.get('one_liner', '')}
Proof: {'; '.join(offer.get('proof_points', []))}

RESEARCH:
{refs}

STYLE FOR THIS VARIANT ({variant}): {VARIANT_STYLES[variant]}

Return JSON only."""
