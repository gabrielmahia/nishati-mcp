"""NishatiMCP — Kenya Energy Access Tools (5 tools). All data DEMO."""
from __future__ import annotations

from importlib.metadata import PackageNotFoundError
from importlib.metadata import version as _pkg_version
from typing import Annotated, Optional

from fastmcp import FastMCP
from pydantic import Field

# Annotations tell clients which tools are safe to auto-approve (read-only, no side effects).
READ_ONLY = {"readOnlyHint": True, "idempotentHint": True, "openWorldHint": False}

try:
    _VERSION = _pkg_version("nishati-mcp")
except PackageNotFoundError:  # a source tree that was never installed
    _VERSION = "0+unknown"


mcp = FastMCP(name="nishati-mcp", instructions="Kenya energy access navigation. DEMO data only.", version=_VERSION)

KPLC_TARIFFS = {
    "domestic_low": "KES 2.90/kWh (0–50 units/month). Lifeline tariff for low-income households.",
    "domestic_mid":  "KES 15.80/kWh (51–100 units). Standard residential tariff.",
    "domestic_high": "KES 21.32/kWh (100+ units). Premium residential.",
    "small_commercial": "KES 18.14/kWh + standing charge.",
    "large_commercial": "Time-of-use tariff. KES 14–20/kWh off-peak/peak.",
}

@mcp.tool(name="kplc_connection_guide", description="Step-by-step guide to getting a new electricity connection from Kenya Power (KPLC): application documents, site survey, quotation, payment, installation and meter. Use when someone asks how to get connected or what it costs. The steps are the same for every county and connection type: both arguments are only echoed back. Returns the source label, county, type, the numbered steps, a note on rural electrification subsidies and KPLC contact details. A static summary labelled DEMO with indicative costs: confirm the process and fees at kplc.co.ke. Read-only; no side effects.", annotations=READ_ONLY)
def kplc_connection_guide(county: Annotated[str | None, Field(description="Optional county; only echoed back.")] = None, connection_type: Annotated[str | None, Field(description="Connection type such as residential; only echoed back (default residential).")] = "residential") -> dict:
    return {"source": "DEMO — kplc.co.ke for official process", "county": county, "type": connection_type,
            "steps": ["1. Application: kplc.co.ke or any KPLC office. Documents: ID, plot number, KRA PIN.",
                      "2. Site survey by KPLC engineer (1–2 weeks)",
                      "3. Quotation issued — residential: KES 35,000–80,000 typical",
                      "4. Pay via M-PESA Paybill 888880",
                      "5. Installation within 30 days of payment",
                      "6. Smart meter installation. Token-based prepay or postpay."],
            "rural_subsidy": "KETRACO/REREC rural electrification may subsidise connection in off-grid areas.",
            "kplc_contacts": "kplc.co.ke | 0703070707"}

@mcp.tool(name="tariff_calculator", description="Estimate a monthly Kenya Power electricity bill in KES from units consumed. Use when someone asks roughly what a given number of kWh will cost. Applies a simple domestic tariff band by units (up to 50, up to 100, above), adds a fuel levy estimate, a forex estimate and a fixed charge. customer_type is accepted but ignored: only the units decide the band. Returns the category, energy charge, fuel levy estimate, fixed charges, estimated total and a reminder to add 16% VAT. Constants are illustrative and not checked against the current KPLC or EPRA tariff: labelled DEMO, confirm at kplc.co.ke. Read-only; no side effects.", annotations=READ_ONLY)
def tariff_calculator(monthly_units_kwh: Annotated[float, Field(description="Electricity used in a month in kilowatt-hours.")], customer_type: Annotated[str | None, Field(description="Accepted but ignored; only monthly_units_kwh sets the band (default residential).")] = "residential") -> dict:
    if monthly_units_kwh <= 50: rate = 2.90; category = "domestic_low"
    elif monthly_units_kwh <= 100: rate = 15.80; category = "domestic_mid"
    else: rate = 21.32; category = "domestic_high"
    fuel_levy = monthly_units_kwh * 3.30
    forex = monthly_units_kwh * 1.85
    fixed = 200.0
    total = round(monthly_units_kwh * rate + fuel_levy + forex + fixed, 2)
    return {"source": "DEMO — approximate only. Check kplc.co.ke for current rates.",
            "monthly_units": monthly_units_kwh, "category": category, "energy_charge": round(monthly_units_kwh * rate, 2),
            "fuel_levy_estimate": round(fuel_levy, 2), "fixed_charges": fixed,
            "estimated_total_kes": total, "note": "Add VAT 16% to total. Rates change quarterly."}

@mcp.tool(name="solar_options_guide", description="Compare solar options in Kenya from a lantern to a productive-use system, with indicative cost ranges, capacity, what each covers and example providers. Use when someone asks what solar they can get for a budget or purpose. With budget_kes, tiers whose lowest listed price is above the budget are removed; use_case is only echoed back. Returns the matching options, a note on pay-as-you-go via M-PESA and the REREC site. Indicative 2025 prices labelled DEMO: confirm with providers. Read-only; no side effects.", annotations=READ_ONLY)
def solar_options_guide(budget_kes: Annotated[float | None, Field(description="Optional budget in KES; removes tiers whose lowest listed price is above it.")] = None, use_case: Annotated[str | None, Field(description="Use case such as basic_lighting; only echoed back.")] = "basic_lighting") -> dict:
    OPTIONS = [
        {"tier": "Solar lantern", "cost": "KES 1,500–4,000", "capacity": "3–6W", "covers": "Lighting + phone charging", "providers": ["M-KOPA","SunKing","d.light"]},
        {"tier": "Solar home system (SHS) basic", "cost": "KES 8,000–25,000", "capacity": "20–40W", "covers": "4 lights + TV + charging", "providers": ["M-KOPA","BBOXX","SunKing"]},
        {"tier": "SHS mid-range", "cost": "KES 40,000–100,000", "capacity": "100–300W", "covers": "Full home + small fridge", "providers": ["BBOXX","Mobisol","Azuri"]},
        {"tier": "SHS productive use", "cost": "KES 150,000+", "capacity": "500W+", "covers": "Business: pump, mill, cold storage", "providers": ["Off-Grid Electric","PowerGen"]},
    ]
    if budget_kes:
        OPTIONS = [o for o in OPTIONS if float(o["cost"].split("–")[0].replace("KES ","").replace(",","")) <= budget_kes]
    return {"source": "DEMO — prices indicative 2025", "use_case": use_case, "options": OPTIONS,
            "pay_as_you_go": "M-KOPA and BBOXX offer PAYG via M-PESA. No upfront cost option.",
            "rerec": "Rural Electrification and Renewable Energy Corporation: rerec.go.ke"}

@mcp.tool(name="energy_subsidy_programs", description="List Kenyan energy access programmes: last-mile connectivity, REREC rural electrification, KOSAP subsidised solar, the lifeline tariff and Stima Loan. Use when someone asks what support exists to get electricity or solar. Takes an optional county that is only echoed back: the same list is returned for every county. Returns the source label, the county and the programmes with provider and benefit. A static list labelled DEMO: verify eligibility at epra.go.ke and rerec.go.ke. Read-only; no side effects.", annotations=READ_ONLY)
def energy_subsidy_programs(county: Annotated[str | None, Field(description="Optional county; only echoed back.")] = None) -> dict:
    return {"source": "DEMO — verify at epra.go.ke, rerec.go.ke", "county": county,
            "programs": [
                {"name": "Last Mile Connectivity", "provider": "KPLC/Kenya Power", "benefit": "Subsidised connection for rural households"},
                {"name": "REREC Rural Electrification", "provider": "REREC", "benefit": "Grid extension to unelectrified areas"},
                {"name": "Affordable Solar (KOSAP)", "provider": "World Bank/GoK", "benefit": "Subsidised SHS for Northern/ASAL counties"},
                {"name": "Lifeline Tariff", "provider": "KPLC/ERC", "benefit": "Reduced rate for 0–50 kWh/month"},
                {"name": "Stima Loan", "provider": "KCB/KPLC", "benefit": "Loan for wiring + connection fee"},
            ]}

@mcp.tool(name="energy_rights_query", description="Explain consumer rights on electricity in Kenya: disconnection notice, billing disputes, damage from surges, connection delays and rural access under the Energy Act 2019. Use when someone asks whether the utility acted correctly or where to complain. Keywords in topic select entries; if none match, ALL rights are returned. Returns the source label, the topic, the rights, EPRA's contact details and a not-legal-advice disclaimer. Static summary labelled DEMO: verify with EPRA. Read-only; no side effects.", annotations=READ_ONLY)
def energy_rights_query(topic: Annotated[str, Field(description="Rights topic such as disconnection, billing_dispute, quality, connection_delay or rural_access.")]) -> dict:
    RIGHTS = {
        "disconnection": "KPLC must give 7 days notice before disconnection. No disconnection on weekends/public holidays.",
        "billing_dispute": "Dispute bill: KPLC customer care → Energy & Petroleum Regulatory Authority (EPRA) if unresolved.",
        "quality": "KPLC liable for damage caused by power surges. Report via kplc.co.ke within 24 hours.",
        "connection_delay": "KPLC must connect within 30 days of full payment. Report delays to EPRA: epra.go.ke",
        "rural_access": "Right to affordable energy access under Energy Act 2019.",
    }
    t = topic.lower()
    matched = {k: v for k, v in RIGHTS.items() if k in t or any(w in t for w in k.split("_"))}
    return {"source": "DEMO — Energy Act 2019, EPRA", "topic": topic,
            "rights": matched or RIGHTS, "epra": "epra.go.ke | 0703070707", "disclaimer": "Not legal advice."}

def main() -> None:
    """Console entry point."""
    mcp.run()
