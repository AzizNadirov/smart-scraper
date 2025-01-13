from dataclasses import dataclass
from pathlib import Path


@dataclass
class Configs:
    """
    Parameters:
        SCRAPYCLOUD_STATUSES: tuple[int] - for these statuses cloudflare-solver will be used
        TMP_DIR: Path
        TMP_PAGES_DIR: Path
    """
    SCRAPYCLOUD_STATUSES: tuple[int]
    TMP_DIR: Path
    TMP_PAGES_DIR: Path
    

configs = Configs(
    SCRAPYCLOUD_STATUSES = (403, 503),
    TMP_DIR = Path(__file__).parent.parent / "tmp/",
    TMP_PAGES_DIR = Path(__file__).parent.parent / "tmp/" / 'pages'
)