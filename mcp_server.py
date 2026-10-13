#!/usr/bin/env python3
import json
import sys
from client import AgenticFlightDelayEU261CompensationClaimant

def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        claimant = AgenticFlightDelayEU261CompensationClaimant()
        sample = {
            "booking_reference": "TK8842",
            "carrier_code": "AF",
            "origin_airport": "CDG",
            "dest_airport": "JFK",
            "delay_arrival_hours": 4.5,
            "carrier_stated_reason": "engine_inspection_crew_shortage",
            "passenger_name": "Alice Cooper"
        }
        res = claimant.generate_claim(sample)
        assert res["claim_status"] == "READY_FOR_AIRLINE_SUBMISSION"
        assert res["claim_verdict"]["statutory_amount_eur"] == 600.0
        print(f"[TEST PASS] EU261 Flight Claim Generated: EUR {res['claim_verdict']['statutory_amount_eur']}")
        sys.exit(0)

    for line in sys.stdin:
        if not line.strip():
            continue
        try:
            req = json.loads(line)
            method = req.get("method")
            msg_id = req.get("id")
            if method == "initialize":
                print(json.dumps({"jsonrpc": "2.0", "id": msg_id, "result": {"serverInfo": {"name": "genpark-flight-delay-claimant", "version": "1.0.0"}}}))
            elif method == "tools/list":
                print(json.dumps({"jsonrpc": "2.0", "id": msg_id, "result": {"tools": [{"name": "generate_claim", "description": "Calculate and generate EU261 flight delay compensation claim"}]}}))
            elif method == "tools/call":
                args = req.get("params", {}).get("arguments", {})
                claimant = AgenticFlightDelayEU261CompensationClaimant()
                out = claimant.generate_claim(args.get("flight_info", {}))
                print(json.dumps({"jsonrpc": "2.0", "id": msg_id, "result": {"content": [{"type": "text", "text": json.dumps(out)}]}}))
            else:
                print(json.dumps({"jsonrpc": "2.0", "id": msg_id, "error": {"code": -32601, "message": "Method not found"}}))
            sys.stdout.flush()
        except Exception as e:
            print(json.dumps({"jsonrpc": "2.0", "error": {"code": -32603, "message": str(e)}}))
            sys.stdout.flush()

if __name__ == "__main__":
    main()
