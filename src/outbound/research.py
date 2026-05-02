from dataclasses import dataclass, field
from typing import Iterable


@dataclass
class Reference:
    """A single concrete fact about a prospect that an email can cite."""
    kind: str           # 'blog_post' | 'job_posting' | 'news' | 'funding'
    summary: str
    url: str | None = None
    quote: str | None = None


@dataclass
class ResearchBundle:
    prospect: dict
    references: list[Reference] = field(default_factory=list)


def gather(prospect: dict, sources: Iterable[str]) -> ResearchBundle:
    """Dispatch to the right fetcher per source. Failures are silent and skipped."""
    refs: list[Reference] = []
    for s in sources:
        try:
            if s == "blog_rss":
                refs.extend(_fetch_blog_rss(prospect))
            elif s == "jobs_page":
                refs.extend(_fetch_jobs(prospect))
            elif s == "news":
                refs.extend(_fetch_news(prospect))
        except Exception:  # noqa: BLE001
            continue
    return ResearchBundle(prospect=prospect, references=refs)


def _fetch_blog_rss(prospect: dict) -> list[Reference]:
    # Stubbed for repo demo; real impl uses feedparser on prospect['blog_rss']
    posts = prospect.get("_mock_blog_posts", [])
    return [
        Reference(kind="blog_post", summary=p["title"], url=p.get("url"), quote=p.get("quote"))
        for p in posts
    ]


def _fetch_jobs(prospect: dict) -> list[Reference]:
    return [
        Reference(kind="job_posting", summary=j["title"], url=j.get("url"))
        for j in prospect.get("_mock_jobs", [])
    ]


def _fetch_news(prospect: dict) -> list[Reference]:
    return [
        Reference(kind="news", summary=n["headline"], url=n.get("url"))
        for n in prospect.get("_mock_news", [])
    ]
