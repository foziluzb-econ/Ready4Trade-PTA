"""Ready4Trade PTA public working-code fragment.

Runs two selected key modules from Ready4Trade v6:
1) buyer-enquiry search;
2) ITC international-sale contract generation.

The included buyer records are synthetic and no API key/network access is required.
"""
from pathlib import Path

from ready4trade_buyers.repository import BuyerRepository
from ready4trade_itc_contract.model import ContractData, Party
from ready4trade_itc_contract.renderer import render_both

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data" / "buyer_leads_sample.csv"
OUTPUT = ROOT / "output"


def main() -> None:
    print("Ready4Trade — PTA public working-code fragment")
    print("=" * 52)

    repo = BuyerRepository(DATA)
    df = repo.load()
    matches = repo.search(df, "product", "dried grapes")
    assert len(matches) == 2
    print(f"Buyer search: found {len(matches)} synthetic 'dried grapes' enquiries")
    for _, row in matches.iterrows():
        print(f"- {row['Buyer From']} | HS {row['ENTUM_HS6']} | {row['Quantity Required']}")

    contract = ContractData(
        seller=Party(
            name="DEMO Exporter LLC",
            legal_form="LLC",
            country_and_register="Uzbekistan / DEMO-REG-001",
            address="Tashkent, Uzbekistan",
            represented_by="PTA Demo Seller",
        ),
        buyer=Party(
            name="DEMO Importer GmbH",
            legal_form="GmbH",
            country_and_register="Germany / DEMO-REG-002",
            address="Berlin, Germany",
            represented_by="PTA Demo Buyer",
        ),
        goods_description="Dried grapes (raisins), HS 080620 — synthetic evaluator example",
        total_quantity="20 metric tonnes",
        packaging="10 kg cartons",
        incoterm_rule="FCA",
        delivery_place="Tashkent, Uzbekistan",
        delivery_date_or_period="Within 30 days after contract signature",
        total_price="USD 30,000",
        amount_numbers="30,000",
        amount_letters="Thirty thousand US dollars",
        currency="USD",
        payment_time="Within 5 banking days after invoice",
        nonconformity_notice_days="10 calendar days",
        national_law="the Republic of Uzbekistan",
        contract_date="18 August 2026",
        seller_signatory_name="PTA Demo Seller",
        buyer_signatory_name="PTA Demo Buyer",
    )
    contract.validate()
    OUTPUT.mkdir(exist_ok=True)
    docx, pdf = render_both(contract, OUTPUT, "pta_demo_international_sale_contract")
    assert docx.exists() and docx.stat().st_size > 1000
    assert pdf.exists() and pdf.stat().st_size > 1000
    print(f"Contract generation: {docx.name}")
    print(f"Contract generation: {pdf.name}")
    print("\nPASS — selected Ready4Trade v6 working code executed successfully.")
    print("All buyer/company data in this repository are synthetic evaluator data.")


if __name__ == "__main__":
    main()
