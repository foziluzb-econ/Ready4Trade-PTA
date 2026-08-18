# Ready4Trade — PTA Working-Code Fragment

This **public evaluation repository** contains a small, runnable fragment of the
Ready4Trade project for President Tech Award technical review.

It follows the PTA GitHub guidance for projects whose main production code is
private or commercially sensitive: a separate public repository may contain
**1–2 key modules** that demonstrate the product's real business logic.

## What is included

This repository exposes two selected Ready4Trade v6 modules:

1. **Buyer-enquiry search** — loads structured buyer enquiries and performs
   literal product/country/HS6 searches.
2. **International-sale contract generation** — validates structured contract
   data and generates an editable DOCX and a PDF based on the Ready4Trade ITC
   contract workflow.

The Python module files were taken from the current Ready4Trade v6 application.
The buyer dataset in this public repository is **synthetic evaluator data** and
does not contain real buyer/user personal data.

## Technology stack

- Python 3.10+
- pandas
- python-docx
- ReportLab

## Run

```bash
git clone https://github.com/foziluzb-econ/Ready4Trade-PTA.git
cd Ready4Trade-PTA

python -m venv .venv
# Windows:
.venv\Scripts\activate
# Linux/macOS:
# source .venv/bin/activate

python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python run_demo.py
```

Expected final message:

```text
PASS — selected Ready4Trade v6 working code executed successfully.
```

The demo also creates:

```text
output/pta_demo_international_sale_contract.docx
output/pta_demo_international_sale_contract.pdf
```

## Repository structure

```text
Ready4Trade-PTA/
├── ready4trade_buyers/
│   └── repository.py
├── ready4trade_itc_contract/
│   ├── model.py
│   └── renderer.py
├── data/
│   └── buyer_leads_sample.csv
├── output/
├── run_demo.py
├── requirements.txt
├── .gitignore
├── LICENSE.md
└── README.md
```

## Relationship to the full Ready4Trade project

This repository is an **evaluation fragment**, not the complete production
deployment. The main project is documented at:

- https://github.com/foziluzb-econ/Ready4Trade
- https://t.me/Ready4Trade_bot
- https://ready4trade.pages.dev/

Production datasets, Telegram/API credentials, server configuration, operational
state, private integrations and other proprietary modules are intentionally not
included here.

## Security and data policy

This repository contains **no** `.env` file, Telegram token, API key, password,
payment-system credential, real user database export or private server key.

The records under `data/` are synthetic and exist only so evaluators can execute
the genuine search logic safely.

## Provenance

This public fragment was prepared on 18 August 2026 from the current
`Ready4Trade_v6_update.zip` source package supplied by the project team.
Creating this evaluation repository does not imply that development began on
that date; it is a separately prepared public fragment of the existing project.

## Intellectual property

Copyright © 2026 Ready4Trade / Foziljon Rustamov. All rights reserved.

This repository is public for technical evaluation. It is not released under an
open-source licence. See `LICENSE.md`.

## Disclaimer

Sample buyers and contract parties are fictional. HS codes and generated
commercial/legal documents must be independently verified before real customs,
legal or commercial use.
