"""Ready4Trade ITC international-sale contract generator."""

from .model import ContractData, Party
from .renderer import build_contract_blocks, render_both, render_docx, render_pdf


def build_contract_sale_handler(**kwargs):
    """Import Telegram dependencies only when the bot handler is requested."""
    from .bot import build_contract_sale_handler as _build

    return _build(**kwargs)

__all__ = [
    "ContractData",
    "Party",
    "build_contract_blocks",
    "build_contract_sale_handler",
    "render_both",
    "render_docx",
    "render_pdf",
]
