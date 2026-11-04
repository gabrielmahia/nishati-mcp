"""solar_yield_estimate: parsing, provenance, validation and failure behaviour, with the network mocked (CI never depends on PVGIS)."""
import urllib.error

from nishati_mcp import server

FAKE = {"outputs": {"totals": {"fixed": {"E_y": 1521.4, "E_d": 4.17}}, "monthly": {"fixed": [{"month": m, "E_m": 120.0 + m} for m in range(1, 13)]}}}


def test_a_live_answer_has_the_yield_and_says_where_it_came_from(monkeypatch):
    seen = {}
    monkeypatch.setattr(server, "_fetch_pvgis", lambda params, timeout=20.0: seen.update(params) or FAKE)
    r = server.solar_yield_estimate(-1.29, 36.82, 2.0, 14.0)
    assert r["annual_kwh"] == 1521.4 and len(r["monthly"]) == 12 and r["monthly"][0] == {"month": 1, "kwh": 121.0}
    assert r["source"].startswith("LIVE") and "European Union" in r["attribution"] and r["retrieved_at"]
    assert seen == {"lat": -1.29, "lon": 36.82, "peakpower": 2.0, "loss": 14.0, "outputformat": "json"}


def test_a_service_failure_returns_an_error_and_never_a_number(monkeypatch):
    def boom(params, timeout=20.0):
        raise urllib.error.URLError("down")
    monkeypatch.setattr(server, "_fetch_pvgis", boom)
    r = server.solar_yield_estimate(-1.29, 36.82)
    assert "error" in r and "annual_kwh" not in r and r["source"].startswith("LIVE")
    monkeypatch.setattr(server, "_fetch_pvgis", lambda params, timeout=20.0: {"unexpected": True})
    assert "annual_kwh" not in server.solar_yield_estimate(-1.29, 36.82)


def test_impossible_inputs_are_refused_before_any_request(monkeypatch):
    def never(params, timeout=20.0):
        raise AssertionError("no request should be made")
    monkeypatch.setattr(server, "_fetch_pvgis", never)
    assert "error" in server.solar_yield_estimate(95, 36.8) and "error" in server.solar_yield_estimate(-1.3, 36.8, system_kwp=0)
    assert "error" in server.solar_yield_estimate(-1.3, 36.8, system_losses_pct=80)
