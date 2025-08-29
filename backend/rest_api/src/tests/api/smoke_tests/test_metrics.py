

def test_get_metrics(test_client):
    """Test get metrics"""
    response = test_client.get("/api/v1/metrics/")
    assert response.status_code == 200