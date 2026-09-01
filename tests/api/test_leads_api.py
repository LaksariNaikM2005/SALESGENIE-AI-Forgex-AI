def test_create_and_list_leads(client, auth_headers):
    create_res = client.post("/api/leads", json={
        "company": "Nexus Cybernetics",
        "contact_name": "Dr. Alex Vance",
        "email": "a.vance@nexus.example.com",
        "value": 75000.0,
        "stage": "New Lead"
    }, headers=auth_headers)
    assert create_res.status_code == 201
    lead_data = create_res.json.get("lead", create_res.json)
    lead_id = lead_data["id"]

    list_res = client.get("/api/leads", headers=auth_headers)
    assert list_res.status_code == 200

    get_res = client.get(f"/api/leads/{lead_id}", headers=auth_headers)
    assert get_res.status_code == 200
    fetched = get_res.json.get("lead", get_res.json)
    assert fetched["company"] == "Nexus Cybernetics"

def test_score_lead_endpoint(client, auth_headers):
    create_res = client.post("/api/leads", json={
        "company": "CyberDyne Systems",
        "contact_name": "Miles Dyson",
        "email": "mdyson@cyberdyne.example.com",
        "value": 120000.0
    }, headers=auth_headers)
    lead_data = create_res.json.get("lead", create_res.json)
    lead_id = lead_data["id"]

    score_res = client.post(f"/api/leads/{lead_id}/score", headers=auth_headers)
    assert score_res.status_code == 200
    assert "lead_score" in score_res.json or "lead" in score_res.json
