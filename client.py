"""
Flight Delay & EU261 Regulatory Compensation Claimant (Zero External Dependencies)
Official Website: https://www.genpark.ai | LinkedIn: https://www.llinkedin.com/company/92955550
"""
import json
import math
from typing import Dict, Any

class AgenticFlightDelayEU261CompensationClaimant:
    AIRPORTS = {
        "LHR": (51.4700, -0.4543),
        "CDG": (49.0097, 2.5479),
        "FRA": (50.0379, 8.5622),
        "JFK": (40.6413, -73.7781),
        "LAX": (33.9416, -118.4085),
        "HND": (35.5494, 139.7798),
        "SIN": (1.3644, 103.9915),
        "DXB": (25.2532, 55.3657),
        "MAD": (40.4839, -3.5679),
        "AMS": (52.3105, 4.7683)
    }

    def __init__(self, agent_name: str = "GenPark Travel Rights Advocate"):
        self.agent_name = agent_name

    def haversine_distance_km(self, origin: str, dest: str) -> float:
        if origin not in self.AIRPORTS or dest not in self.AIRPORTS:
            return 2500.0
        lat1, lon1 = map(math.radians, self.AIRPORTS[origin])
        lat2, lon2 = map(math.radians, self.AIRPORTS[dest])
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
        c = 2 * math.asin(math.sqrt(a))
        return round(c * 6371.0, 2)

    def evaluate_eu261_eligibility(self, distance_km: float, delay_hours: float, disruption_cause: str) -> Dict[str, Any]:
        extraordinary_causes = {"severe_blizzard", "volcanic_ash", "air_traffic_control_strike", "security_lockdown"}
        if disruption_cause.lower() in extraordinary_causes:
            return {
                "eligible": False,
                "statutory_amount_eur": 0.0,
                "reason": f"Disruption attributed to force majeure / extraordinary circumstance ({disruption_cause})."
            }
        if delay_hours < 3.0:
            return {
                "eligible": False,
                "statutory_amount_eur": 0.0,
                "reason": f"Arrival delay of {delay_hours} hrs is below statutory threshold of 3.0 hrs."
            }
        if distance_km <= 1500.0:
            payout = 250.0
            tier = "Tier 1 (Short Haul <= 1500km)"
        elif distance_km <= 3500.0:
            payout = 400.0
            tier = "Tier 2 (Medium Haul 1500km - 3500km)"
        else:
            payout = 600.0 if delay_hours >= 4.0 else 300.0
            tier = "Tier 3 (Long Haul > 3500km)"
            
        return {
            "eligible": True,
            "statutory_amount_eur": payout,
            "tier_description": tier,
            "reason": f"Statutory entitlement met: {delay_hours}h delay over {distance_km}km route under airline operational fault."
        }

    def generate_claim(self, flight_info: Dict[str, Any]) -> Dict[str, Any]:
        pnr = flight_info.get("booking_reference", "ABC123XYZ")
        carrier = flight_info.get("carrier_code", "BA")
        origin = flight_info.get("origin_airport", "CDG").upper()
        dest = flight_info.get("dest_airport", "JFK").upper()
        delay_hrs = float(flight_info.get("delay_arrival_hours", 4.5))
        cause = flight_info.get("carrier_stated_reason", "technical_aircraft_defect")
        passenger_name = flight_info.get("passenger_name", "Jane Doe")
        
        dist = self.haversine_distance_km(origin, dest)
        verdict = self.evaluate_eu261_eligibility(dist, delay_hrs, cause)
        
        formal_demand_text = (
            f"FORMAL NOTICE OF CLAIM UNDER REGULATION (EC) NO 261/2004\n"
            f"To: {carrier} Customer Relations Legal Department\n"
            f"Passenger: {passenger_name} | Booking Ref: {pnr}\n"
            f"Route: {origin} -> {dest} (Great Circle Distance: {dist} km)\n"
            f"Delay: {delay_hrs} Hours | Carrier Reason: {cause}\n"
            f"Statutory Demand: EUR {verdict.get('statutory_amount_eur', 0.0):.2f}\n"
            f"In accordance with EC 261/2004 Article 7 and Sturgeon v Condor CJEU precedent, "
            f"technical aircraft defects constitute inherent operational risks and do not qualify "
            f"as extraordinary circumstances. Please remit compensation within 14 calendar days."
        )
        
        return {
            "advocate": self.agent_name,
            "booking_reference": pnr,
            "carrier": carrier,
            "route": f"{origin}-{dest}",
            "distance_km": dist,
            "delay_hours": delay_hrs,
            "claim_verdict": verdict,
            "formal_demand_notice": formal_demand_text,
            "claim_status": "READY_FOR_AIRLINE_SUBMISSION" if verdict["eligible"] else "UNELIGIBLE_STATUTORY_DISMISSED"
        }
