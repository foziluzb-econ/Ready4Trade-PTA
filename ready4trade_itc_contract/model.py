"""Data model and validation for the Ready4Trade ITC sale-contract wizard.

The legal prose is deliberately kept out of this module.  User answers are data;
they never become Python/Jinja templates and are never evaluated.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from decimal import Decimal, InvalidOperation
import re
from typing import Any


MAX_TEXT = 2_000
MAX_LONG_TEXT = 8_000
CONTROL_CHARS = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]")
INCOTERMS_2020 = ("EXW", "FCA", "CPT", "CIP", "DAP", "DPU", "DDP", "FAS", "FOB", "CFR", "CIF")
PAYMENT_ARRANGEMENTS = ("advance", "collection", "credit", "guarantee", "other")
DISPUTE_METHODS = ("institutional", "ad_hoc", "courts")
DOCUMENT_KEYS = (
    "commercial_invoice",
    "transport_documents",
    "packing_list",
    "insurance_documents",
    "certificate_of_origin",
    "certificate_of_inspection",
    "customs_documents",
    "other_documents",
)


def clean_text(value: Any, *, limit: int = MAX_TEXT, required: bool = False) -> str:
    """Normalize a Telegram answer and reject control characters/oversized data."""
    text = CONTROL_CHARS.sub("", str(value or "")).strip()
    text = re.sub(r"[ \t]+", " ", text)
    if required and not text:
        raise ValueError("This field is required.")
    if len(text) > limit:
        raise ValueError(f"Maximum length is {limit} characters.")
    return text


def clean_percentage(value: Any, *, allow_blank: bool = True) -> str:
    text = clean_text(value)
    if not text and allow_blank:
        return ""
    try:
        number = Decimal(text.replace(",", ".").replace("%", "").strip())
    except InvalidOperation as exc:
        raise ValueError("Enter a number, for example 0.1 or 5.") from exc
    if number < 0 or number > 100:
        raise ValueError("Percentage must be between 0 and 100.")
    return format(number.normalize(), "f")


@dataclass(slots=True)
class Party:
    name: str = ""
    legal_form: str = ""
    country_and_register: str = ""
    address: str = ""
    represented_by: str = ""


@dataclass(slots=True)
class ContractData:
    seller: Party = field(default_factory=Party)
    buyer: Party = field(default_factory=Party)

    goods_description: str = ""
    total_quantity: str = ""
    instalment_quantity: str = ""
    tolerance_percentage: str = ""
    inspection: str = ""
    packaging: str = ""
    other_specification: str = ""

    incoterm_rule: str = "FCA"
    delivery_place: str = ""
    delivery_date_or_period: str = ""
    carrier: str = ""
    other_delivery_terms: str = ""

    total_price: str = ""
    price_per_unit: str = ""
    amount_numbers: str = ""
    amount_letters: str = ""
    currency: str = "USD"
    price_method: str = ""

    means_of_payment: str = "bank transfer"
    seller_bank_account: str = ""
    payment_time: str = ""
    payment_arrangement: str = "advance"
    payment_details: str = ""

    documents: list[str] = field(default_factory=lambda: ["commercial_invoice", "packing_list"])
    transport_document_details: str = ""
    document_copies: str = ""
    other_document_details: str = ""

    buyer_payment_additional_period: str = "10 calendar days"
    late_interest_rate: str = ""
    seller_delivery_additional_period: str = "10 calendar days"

    include_delay_liquidated_damages: bool = False
    delay_daily_rate: str = "0.5"
    delay_notice_days: str = ""
    delay_cap: str = ""

    nonconformity_notice_days: str = ""
    nonconformity_long_stop: str = "two years"
    liability_limit: str = ""

    retain_title: bool = False
    additional_fundamental_breaches: str = ""
    general_breach_additional_period: str = "10 calendar days"

    force_majeure_months: str = "three"
    force_majeure_negotiation_first: bool = False
    force_majeure_negotiation_days: str = "30"

    supersedes_previous: bool = True
    seller_notice_details: str = ""
    buyer_notice_details: str = ""

    dispute_method: str = "institutional"
    arbitration_institution: str = "Tashkent International Arbitration Centre (TIAC)"
    arbitration_rules: str = "TIAC Rules of Arbitration"
    arbitrators: str = "a sole arbitrator"
    appointing_authority: str = ""
    arbitration_place: str = "Tashkent, Uzbekistan"
    arbitration_language: str = "English"
    court_place_country: str = ""

    national_law: str = "the Republic of Uzbekistan"
    contract_date: str = ""
    seller_signatory_name: str = ""
    buyer_signatory_name: str = ""

    def validate(self) -> None:
        required = {
            "seller name": self.seller.name,
            "seller address": self.seller.address,
            "buyer name": self.buyer.name,
            "buyer address": self.buyer.address,
            "goods description": self.goods_description,
            "total quantity": self.total_quantity,
            "delivery place": self.delivery_place,
            "delivery date/period": self.delivery_date_or_period,
            "total price": self.total_price,
            "currency": self.currency,
            "payment time": self.payment_time,
            "non-conformity notice period": self.nonconformity_notice_days,
            "national law": self.national_law,
        }
        missing = [label for label, value in required.items() if not clean_text(value)]
        if missing:
            raise ValueError("Missing required fields: " + ", ".join(missing))
        if self.incoterm_rule not in INCOTERMS_2020:
            raise ValueError("Unknown Incoterms 2020 rule.")
        if self.payment_arrangement not in PAYMENT_ARRANGEMENTS:
            raise ValueError("Unknown payment arrangement.")
        if self.dispute_method not in DISPUTE_METHODS:
            raise ValueError("Unknown dispute method.")
        unknown_docs = set(self.documents) - set(DOCUMENT_KEYS)
        if unknown_docs:
            raise ValueError(f"Unknown document keys: {sorted(unknown_docs)}")
        if self.delay_daily_rate:
            clean_percentage(self.delay_daily_rate)
        if self.delay_cap:
            clean_percentage(self.delay_cap)
        if self.late_interest_rate:
            clean_percentage(self.late_interest_rate)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, raw: dict[str, Any]) -> "ContractData":
        data = dict(raw)
        data["seller"] = Party(**data.get("seller", {}))
        data["buyer"] = Party(**data.get("buyer", {}))
        return cls(**data)


def set_nested_value(contract: ContractData, path: str, value: Any) -> None:
    """Set a whitelisted dataclass attribute such as ``seller.name``."""
    target: Any = contract
    parts = path.split(".")
    for part in parts[:-1]:
        if not hasattr(target, part):
            raise AttributeError(path)
        target = getattr(target, part)
    final = parts[-1]
    if not hasattr(target, final):
        raise AttributeError(path)
    setattr(target, final, value)
