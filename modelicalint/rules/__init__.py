from .annotations import InlineAnnotationRule
from .structure import WithinRule, SingleModelRule
from .sections import SectionOrderRule
from .parameters import ParameterAnnotationRule
from .connects import ConnectPlacementRule

ALL_RULES = [
    InlineAnnotationRule(),      # ML201 (fixable)
    ParameterAnnotationRule(),   # ML401
    WithinRule(),
    SingleModelRule(),
    SectionOrderRule(),
    ConnectPlacementRule(),
]
