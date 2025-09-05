# import sys
# import os
# print(f"path:  {os.getcwd()}")
# sys.path.append("..")

from src.api import app  as myapp   # Import your FastAPI app


# client = TestClient(app)


# Test for getting all sellers
def test_get_all_sellers(test_client, create_sellers, auth_headers):
    # Use the `auth_headers` fixture to authenticate the request
    response = test_client.get("/api/v1/sellers/", headers=auth_headers)
    
    # Assert that the status code is 200 OK
    assert response.status_code == 200
    
    # Parse the response data as JSON
    sellers = response.json()
    
    # Ensure the response is a list of sellers
    assert isinstance(sellers, list)
    
    # Check that the number of sellers returned matches the number created in the database
    assert len(sellers) == len(create_sellers)


# Test for creating a new seller
def test_create_seller(test_client, auth_headers):
    # Define new seller data to create
    new_seller_data = {
        "official_name": "New Seller",
        "address": "789 New St",
        "city": "New City"
    }

    # Send a POST request to create a new seller with authentication
    response = test_client.post("/api/v1/sellers/", json=new_seller_data, headers=auth_headers)

    # Assert that the status code is 200 OK
    assert response.status_code == 200
    
    # Parse the response to get the created seller data
    created_seller = response.json()
    
    # Check that the returned seller's official name matches the input data
    assert created_seller["official_name"] == new_seller_data["official_name"]
    
    # Check that the seller's address and city match the input data
    assert created_seller["address"] == new_seller_data["address"]
    assert created_seller["city"] == new_seller_data["city"]


# Test for getting a specific seller by ID
def test_get_seller_by_id(test_client, create_sellers, auth_headers):
    # Get the ID of the first seller created in the `create_sellers` fixture
    seller_id = create_sellers[0].id
    
    # Send a GET request to fetch the seller by ID with authentication
    response = test_client.get(f"/api/v1/sellers/{seller_id}", headers=auth_headers)

    # Assert that the status code is 200 OK
    assert response.status_code == 200
    
    # Parse the response to get the seller data
    seller = response.json()
    
    # Check that the seller's ID matches the ID in the URL
    assert seller["id"] == str(seller_id)


# Test for updating a seller
def test_update_seller(test_client, create_sellers, auth_headers):
    # Get the ID of the first seller created in the `create_sellers` fixture
    seller_id = create_sellers[0].id
    
    # Define the updated seller data
    updated_seller_data = {
        "id": str(seller_id),
        "name": "Updated Seller Name",
        "official_name": "Updated Official Seller",
        "address": "123 Updated St",
        "city": "Updated City"
    }

    # Send a PUT request to update the seller with authentication
    response = test_client.put(f"/api/v1/sellers/{seller_id}", json=updated_seller_data, headers=auth_headers)

    # Assert that the status code is 200 OK
    assert response.status_code == 200
    
    # Parse the response to get the updated seller data
    updated_seller = response.json()
    
    # Check that the updated seller's data matches the input data
    assert updated_seller["name"] == updated_seller_data["name"]
    assert updated_seller["official_name"] == updated_seller_data["official_name"]
    assert updated_seller["address"] == updated_seller_data["address"]
    assert updated_seller["city"] == updated_seller_data["city"]


# Test for deleting a seller
def test_delete_seller(test_client, create_sellers, auth_headers):
    # Get the ID of the first seller created in the `create_sellers` fixture
    seller_id = create_sellers[0].id
    
    # Send a DELETE request to delete the seller with authentication
    response = test_client.delete(f"/api/v1/sellers/{seller_id}", headers=auth_headers)

    # Assert that the status code is 200 OK (successful deletion)
    assert response.status_code == 200
    
    # Send a GET request to check if the seller was deleted
    get_response = test_client.get(f"/api/v1/sellers/{seller_id}", headers=auth_headers)

    # Assert that the status code is 404 (seller not found)
    assert get_response.status_code == 404


# Test for counting bills by seller name
def test_count_bills_by_name(test_client, auth_headers):
    # Send a GET request to the "count_bills_by_name" endpoint
    response = test_client.get("/api/v1/sellers/count_bills_by_name/", headers=auth_headers)
    
    # Assert that the status code is 200 OK
    assert response.status_code == 200
    
    # Parse the response to get the count of bills by name
    bills_count = response.json()
    
    # Check that the response is a list of counts (you can add specific checks here if needed)
    assert isinstance(bills_count, list)


# Test for summing bills by seller name
def test_summ_bills_by_name(test_client, auth_headers):
    # Send a GET request to the "summ_bills_by_name" endpoint
    response = test_client.get("/api/v1/sellers/summ_bills_by_name/", headers=auth_headers)
    
    # Assert that the status code is 200 OK
    assert response.status_code == 200
    
    # Parse the response to get the sum of bills by name
    bills_sum = response.json()
    
    # Check that the response is a list of sums (you can add specific checks here if needed)
    assert isinstance(bills_sum, list)


# Test for counting goods by seller name
def test_count_goods_by_name(test_client, auth_headers):
    # Send a GET request to the "count_goods_by_name" endpoint
    response = test_client.get("/api/v1/sellers/count_goods_by_name/", headers=auth_headers)
    
    # Assert that the status code is 200 OK
    assert response.status_code == 200
    
    # Parse the response to get the count of goods by seller name
    goods_count = response.json()
    
    # Check that the response is a list of counts (you can add specific checks here if needed)
    assert isinstance(goods_count, list)
