## API Endpoints

### Resource Endpoints


#### Retrieve, Update, and Delete a Specific Worker
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