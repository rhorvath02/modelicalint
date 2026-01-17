from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional

from modelicalint.context import Context
from modelicalint.message import LintMessage


@dataclass
class Rule(ABC):
    code: str
    description: str
    default_enabled: bool = True
    severity: str = "warning"
    fixable: bool = False

    @abstractmethod
    def check(self, path: Path, lineno: int, line: str, ctx: Context) -> List[LintMessage]:
        pass

    def fix(self, line: str) -> Optional[List[str]]:
        """
        Return a list of replacement lines, or None if not fixable
        """
        return None
