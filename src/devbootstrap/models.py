from dataclasses import dataclass

@dataclass
class Repo:
    name: str
    url: str
    provider: str  # "GitHub" or "GitLab"