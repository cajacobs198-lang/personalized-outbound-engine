from outbound.research import ResearchBundle, Reference
from outbound.generate import generate
from outbound.prompt import build_user_prompt

OFFER = {"one_liner": "We help X.", "proof_points": ["a", "b"], "sources": []}


def _stub_classifier(prompt, model):
    return {
        "subject": "Re: thing",
        "body": "Saw your job posting. We help. Open to 15 min?",
        "reference_used": "job_posting:Sales Engineer",
    }


def test_generate_returns_one_per_variant():
    bundle = ResearchBundle(
        prospect={"email": "a@b.com", "first_name": "Sara", "company": "Notion"},
        references=[Reference(kind="job_posting", summary="Sales Engineer")],
    )
    out = generate(bundle, OFFER, ["A", "B", "C"], classify_fn=_stub_classifier)
    assert len(out) == 3
    assert {e.variant for e in out} == {"A", "B", "C"}
    for e in out:
        assert e.prospect_email == "a@b.com"


def test_generate_skips_when_research_empty():
    def err_classifier(prompt, model):
        return {"error": "insufficient research"}
    bundle = ResearchBundle(prospect={"email": "a@b.com"}, references=[])
    out = generate(bundle, OFFER, ["A"], classify_fn=err_classifier)
    assert out == []


def test_prompt_includes_research():
    bundle = ResearchBundle(
        prospect={"first_name": "Sara", "company": "Notion"},
        references=[Reference(kind="job_posting", summary="Sales Engineer")],
    )
    prompt = build_user_prompt(OFFER, bundle, "A")
    assert "Sales Engineer" in prompt
    assert "Sara" in prompt
