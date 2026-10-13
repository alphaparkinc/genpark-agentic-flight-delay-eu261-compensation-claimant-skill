from client import AgenticFlightDelayEU261CompensationClaimant

def main():
    claimant = AgenticFlightDelayEU261CompensationClaimant()
    flight = {
        "booking_reference": "BA9921",
        "carrier_code": "BA",
        "origin_airport": "LHR",
        "dest_airport": "FRA",
        "delay_arrival_hours": 3.5,
        "carrier_stated_reason": "maintenance_hydraulic_check",
        "passenger_name": "Marcus Aurelius"
    }
    claim = claimant.generate_claim(flight)
    print(f"Route: {claim['route']} | Distance: {claim['distance_km']} km")
    print(f"Statutory Compensation: EUR {claim['claim_verdict']['statutory_amount_eur']}")
    print(f"Verdict: {claim['claim_verdict']['reason']}")
    print("\n--- Formal Demand Notice Draft ---")
    print(claim['formal_demand_notice'])

if __name__ == "__main__":
    main()
