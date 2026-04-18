import requests
import json

BASE_URL = 'http://127.0.0.1:8000/graphql/'

# Test 1: CREATE mutation
print("=" * 50)
print("TEST 1: CREATE SHOP")
print("=" * 50)

create_query = '''
mutation {
  createShop(name: "FreshMart", address: "Hyderabad, Telangana", emails: ["fresh@mart.com", "support@freshmart.com"], phones: ["9999999999", "8888888888"]) {
    shop {
      id
      name
      address
      emails { email }
      phones { phone }
    }
  }
}
'''

response = requests.post(BASE_URL, json={'query': create_query})
create_result = response.json()
print(json.dumps(create_result, indent=2))

# Extract shop ID if successful
shop_id = None
if 'data' in create_result and create_result['data']:
    shop = create_result['data'].get('createShop', {}).get('shop')
    if shop:
        shop_id = shop['id']
        print(f"\nCreated shop with ID: {shop_id}")

# Test 2: READ ALL query
print("\n" + "=" * 50)
print("TEST 2: READ ALL SHOPS")
print("=" * 50)

read_all_query = '''
query {
  allShops {
    id
    name
    address
    emails { email }
    phones { phone }
  }
}
'''

response = requests.post(BASE_URL, json={'query': read_all_query})
print(json.dumps(response.json(), indent=2))

# Test 3: READ ONE query (if we have a shop ID)
if shop_id:
    print("\n" + "=" * 50)
    print(f"TEST 3: READ SHOP ID {shop_id}")
    print("=" * 50)
    
    read_one_query = f'''
    query {{
      shop(id: {shop_id}) {{
        id
        name
        address
        emails {{ email }}
        phones {{ phone }}
      }}
    }}
    '''
    
    response = requests.post(BASE_URL, json={'query': read_one_query})
    print(json.dumps(response.json(), indent=2))

    # Test 4: UPDATE mutation
    print("\n" + "=" * 50)
    print(f"TEST 4: UPDATE SHOP ID {shop_id}")
    print("=" * 50)
    
    update_query = f'''
    mutation {{
      updateShop(id: {shop_id}, name: "FreshMart Updated", emails: ["newemail@freshmart.com"], phones: ["7777777777"]) {{
        shop {{
          id
          name
          address
          emails {{ email }}
          phones {{ phone }}
        }}
      }}
    }}
    '''
    
    response = requests.post(BASE_URL, json={'query': update_query})
    print(json.dumps(response.json(), indent=2))

    # Test 5: DELETE mutation
    print("\n" + "=" * 50)
    print(f"TEST 5: DELETE SHOP ID {shop_id}")
    print("=" * 50)
    
    delete_query = f'''
    mutation {{
      deleteShop(id: {shop_id}) {{
        ok
      }}
    }}
    '''
    
    response = requests.post(BASE_URL, json={'query': delete_query})
    print(json.dumps(response.json(), indent=2))
