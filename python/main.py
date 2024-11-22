import requests

class NotionCRUD:
    """
    A class for interacting with the Notion API to perform CRUD operations on a database.

    Attributes:
        secret_key (str): The secret key for authenticating with the Notion API.
        database_id (str): The ID of the Notion database to interact with.
        headers (dict): The headers for API requests.
    """

    def __init__(self, secret_key: str, database_id: str):
        """
        Initialize the NotionCRUD class with the provided secret key and database ID.

        Args:
            secret_key (str): The secret key for authenticating with the Notion API.
            database_id (str): The ID of the Notion database to interact with.
        """
        self.secret_key = secret_key
        self.database_id = database_id
        self.headers = {
            "Authorization": f"Bearer {self.secret_key}",
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28",  # Adjust version as necessary
        }

    def get_all(self, num_pages=None):
        """
        If num_pages is None, get all pages; otherwise, get the defined number of pages.

        Args:
            num_pages (int, optional): The number of pages to retrieve. Defaults to None.

        Returns:
            list: A list of pages retrieved from the Notion database.
        """
        url = f"https://api.notion.com/v1/databases/{self.database_id}/query"

        get_all = num_pages is None
        page_size = 100 if get_all else num_pages

        payload = {"page_size": page_size}
        response = requests.post(url, json=payload, headers=self.headers)

        if response.status_code != 200:
            raise Exception(f"Failed to fetch pages: {response.text}")

        data = response.json()
        results = data["results"]

        while data.get("has_more") and get_all:
            payload = {"page_size": page_size, "start_cursor": data["next_cursor"]}
            response = requests.post(url, json=payload, headers=self.headers)

            if response.status_code != 200:
                raise Exception(f"Failed to fetch more pages: {response.text}")

            data = response.json()
            results.extend(data["results"])

        return results

    def create_page(self, data: dict) -> requests.Response:
        """
        Creates a new page in the Notion database.

        Args:
            data (dict): A dictionary containing the properties for the new page.

        Returns:
            requests.Response: The response from the Notion API.
        """
        create_url = "https://api.notion.com/v1/pages"
        payload = {"parent": {"database_id": self.database_id}, "properties": data}

        response = requests.post(create_url, headers=self.headers, json=payload)

        if response.status_code != 200:
            raise Exception(f"Failed to create page: {response.text}")

        return response

    def update_page(self, page_id: str, data: dict) -> requests.Response:
        """
        Updates a page in the Notion database.

        Args:
            page_id (str): The ID of the page to update.
            data (dict): A dictionary containing the properties to update.

        Returns:
            requests.Response: The response from the Notion API.
        """
        url = f"https://api.notion.com/v1/pages/{page_id}"
        payload = {"properties": data}

        response = requests.patch(url, json=payload, headers=self.headers)

        if response.status_code != 200:
            raise Exception(f"Failed to update page: {response.text}")

        return response

    def delete_page(self, page_id: str) -> requests.Response:
        """
        Archives (deletes) a page in the Notion database.

        Args:
            page_id (str): The ID of the page to delete.

        Returns:
            requests.Response: The response from the Notion API.
        """
        url = f"https://api.notion.com/v1/pages/{page_id}"
        payload = {"archived": True}

        response = requests.patch(url, json=payload, headers=self.headers)

        if response.status_code != 200:
            raise Exception(f"Failed to delete page: {response.text}")

        return response

# Example usage
if __name__ == "__main__":
    SECRET_KEY = "your_secret_key_here"
    DATABASE_ID = "your_database_id_here"

    notion = NotionCRUD(secret_key=SECRET_KEY, database_id=DATABASE_ID)

    # Example of creating a page
    new_page_data = {
        "Name": {"title": [{"text": {"content": "New Page Title"}}]},  # Adjust property names as needed
        "Status": {"select": {"name": "Not Started"}}  # Example property
    }
    create_response = notion.create_page(data=new_page_data)
    print("Create Page Response:", create_response.json())

    # Example of getting pages
    pages = notion.get_pages(num_pages=5)  # Retrieve 5 pages
    print("Retrieved Pages:", pages)

    # Example of updating a page
    PAGE_ID = "your_page_id_here"
    update_data = {
        "Name": {"title": [{"text": {"content": "Updated Title"}}]},  # Adjust property names as needed
        "Status": {"select": {"name": "In Progress"}}  # Example property update
    }
    update_response = notion.update_page(page_id=PAGE_ID, data=update_data)
    print("Update Response:", update_response.json())

    # Example of deleting a page
    delete_response = notion.delete_page(page_id=PAGE_ID)
    print("Delete Response:", delete_response.json())