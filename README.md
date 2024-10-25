## Deployed Link
```
[API Endpoints] https://api-dev.subsecure.in/api/
[Websocket Endpoints] wss://api-dev.subsecure.in/ws/
```

## API Endpoints

#### Update Workers API
- **URL:** `/api/update-workers/`
- **Methods:**
  - `PUT`: Update a set of workers by ID.
- **Body:**
  - ```json
        [
            {
                "worker_id": "W001",
                "location_id": "L002"
            },
            {
                "worker_id": "W002",
                "location_id": "L003"
            },
            {
                "worker_id": "W003",
                "location_id": "L001"
            }
        ]
    ```
- **Description:** This endpoint allows you to update workers by its ID.

## Websocket Endpoints

#### Fetch Live Workers Data
- **URL:** `/ws/workers/`
- **Response Body:**
  - ```json
        {
            "workers": [
                {
                    "id": "W001",
                    "name": "Mohan Lal",
                    "age": 32,
                    "location_id": "L002"
                },
                {
                    "id": "W002",
                    "name": "Aman Raj",
                    "age": 28,
                    "location_id": "L003"
                },
                {
                    "id": "W003",
                    "name": "Chikoo Yadav",
                    "age": 34,
                    "location_id": "L004"
                },
                {
                    "id": "W004",
                    "name": "Nandan Lal",
                    "age": 30,
                    "location_id": "L005"
                }
            ]
        }
    ```
- **Description:** This websocket allows you to get live worker status.

#### Fetch Live Location Data
- **URL:** `/ws/locations/`
- **Response Body:**
  - ```json
        {
            "locations": [
                {
                    "id": "L001",
                    "description": "Underground Shaft 1",
                    "temperature": 41.6,
                    "o2_level": 72.0,
                    "number_of_workers": 0,
                    "emergency_bit": false
                },
                {
                    "id": "L002",
                    "description": "Underground Shaft 2",
                    "temperature": 39.5,
                    "o2_level": 80.0,
                    "number_of_workers": 1,
                    "emergency_bit": false
                },
                {
                    "id": "L003",
                    "description": "Mine front 1",
                    "temperature": 50.2,
                    "o2_level": 64.0,
                    "number_of_workers": 1,
                    "emergency_bit": false
                },
                {
                    "id": "L004",
                    "description": "Warehouse 1",
                    "temperature": 40.6,
                    "o2_level": 86.0,
                    "number_of_workers": 1,
                    "emergency_bit": false
                },
                {
                    "id": "L005",
                    "description": "Warehouse 2",
                    "temperature": 39.5,
                    "o2_level": 83.0,
                    "number_of_workers": 1,
                    "emergency_bit": false
                }
            ]
        }
    ```
- **Description:** This websocket allows you to get live nodes status