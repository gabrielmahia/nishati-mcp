"""NishatiMCP — Kenya Energy Access Tools (5 tools). All data DEMO."""
from __future__ import annotations
from typing import Optional
from fastmcp import FastMCP
mcp = FastMCP(name="nishati-mcp", instructions="Kenya energy access navigation. DEMO data only.")

KPLC_TARIFFS = {
    "domestic_low": "KES 2.90/kWh (0–50 units/month). Lifeline tariff for low-income households.",
    "domestic_mid":  "KES 15.80/kWh (51–100 units). Standard residential tariff.",
    "domestic_high": "KES 21.32/kWh (100+ units). Premium residential.",
    "small_commercial": "KES 18.14/kWh + standing charge.",
    "large_commercial": "Time-of-use tariff. KES 14–20/kWh off-peak/peak.",
}

@mcp.tool(name="kplc_connection_guide", description="Guide to new KPLC electricity connection in Kenya. DEMO.")
def kplc_connection_guide(county: Optional[str] = None, connection_type: Optional[str] = "residential") -> dict:
    return {"source": "DEMO — kplc.co.ke for official process", "county": county, "type": connection_type,
            "steps": ["1. Application: kplc.co.ke or any KPLC office. Documents: ID, plot number, KRA PIN.",
                      "2. Site survey by KPLC engineer (1–2 weeks)",
                      "3. Quotation issued — residential: KES 35,000–80,000 typical",
                      "4. Pay via M-PESA Paybill 888880",
                      "5. Installation within 30 days of payment",
                      "6. Smart meter installation. Token-based prepay or postpay."],
            "rural_subsidy": "KETRACO/REREC rural electrification may subsidise connection in off-grid areas.",
            "kplc_contacts": "kplc.co.ke | 0703070707"}

@mcp.tool(name="tariff_calculator", description="Estimate monthly KPLC electricity cost for Kenya household. DEMO.")
def tariff_calculator(monthly_units_kwh: float, customer_type: Optional[str] = "residential") -> dict:
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

@mcp.tool(name="solar_options_guide", description="Off-grid solar options for Kenya households. DEMO.")
def solar_options_guide(budget_kes: Optional[float] = None, use_case: Optional[str] = "basic_lighting") -> dict:
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

@mcp.tool(name="energy_subsidy_programs", description="Kenya energy subsidy and access programs. DEMO.")
def energy_subsidy_programs(county: Optional[str] = None) -> dict:
    return {"source": "DEMO — verify at epra.go.ke, rerec.go.ke", "county": county,
            "programs": [
                {"name": "Last Mile Connectivity", "provider": "KPLC/Kenya Power", "benefit": "Subsidised connection for rural households"},
                {"name": "REREC Rural Electrification", "provider": "REREC", "benefit": "Grid extension to unelectrified areas"},
                {"name": "Affordable Solar (KOSAP)", "provider": "World Bank/GoK", "benefit": "Subsidised SHS for Northern/ASAL counties"},
                {"name": "Lifeline Tariff", "provider": "KPLC/ERC", "benefit": "Reduced rate for 0–50 kWh/month"},
                {"name": "Stima Loan", "provider": "KCB/KPLC", "benefit": "Loan for wiring + connection fee"},
            ]}

@mcp.tool(name="energy_rights_query", description="Consumer rights for electricity in Kenya. DEMO.")
def energy_rights_query(topic: str) -> dict:
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
