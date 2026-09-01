def test_conversation_summarize_endpoint(client, auth_headers):
    transcript_sample = (
        "Sales Rep: Good morning, we'd love to review your sales automation requirements.\n"
        "Client: We have a budget of $50,000 for Q3. Please send a proposal by Friday."
    )
    res = client.post("/api/conversations/summarize", json={
        "title": "Strategy Meeting",
        "transcript": transcript_sample
    }, headers=auth_headers)

    assert res.status_code == 201
    assert "summary" in res.json
    assert "insights" in res.json
    assert "sentiment" in res.json
