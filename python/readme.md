# NotionCRUD Documentation

## Overview

`NotionCRUD` is a Python class for interacting with the Notion API to perform CRUD (Create, Read, Update, Delete) operations on a Notion database. This class simplifies the process of managing pages within Notion by providing an easy-to-use interface.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
  - [Initialization](#initialization)
  - [Methods](#methods)
- [Example Usage](#example-usage)
- [Error Handling](#error-handling)
- [Contributing](#contributing)

## Installation

To use the `NotionCRUD` class, ensure you have Python installed on your machine. You can install any necessary dependencies with pip, although this class primarily uses the built-in `requests` library.

```bash
pip install requests
```

## Usage

### Initialization

To create an instance of `NotionCRUD`, you need to provide your Notion API secret key and the database ID you wish to interact with.

```python
notion = NotionCRUD(secret_key="your_secret_key_here", database_id="your_database_id_here")
```

### Methods

```python
def get_all(num_pages=None): 
    """
    Retrieves pages from the Notion database.
    Args:
        num_pages (int, optional): The number of pages to retrieve. If None, retrieves all pages.
    Returns:
        list: A list of pages retrieved from the Notion database.
    """
    pass

def create_page(data: dict): 
    """
    Creates a new page in the Notion database.

    Args:
        data (dict): A dictionary containing the properties for the new page.
    Returns:
        requests.Response: The response from the Notion API.
    """
    pass

def update_page(page_id: str, data: dict): 
    """
    Updates an existing page in the Notion database.

    Args:
        page_id (str): The ID of the page to update.
        data (dict): A dictionary containing the properties to update.
    Returns:
        requests.Response: The response from the Notion API.
    """
    pass

def delete_page(data: dict): 
    """
    Archives (deletes) a page in the Notion database.

    Args:
        page_id (str): The ID of the page to delete.
    Returns:
        requests.Response: The response from the Notion AP
    """
    pass
```

### Example usage

```python
if __name__ == "__main__":
    SECRET_KEY = "your_secret_key_here"
    DATABASE_ID = "your_database_id_here"

    notion = NotionCRUD(secret_key=SECRET_KEY, database_id=DATABASE_ID)

    # Creating a page
    new_page_data = {
        "Name": {"title": [{"text": {"content": "New Page Title"}}]},
        "Status": {"select": {"name": "Not Started"}}
    }
    create_response = notion.create_page(data=new_page_data)
    print("Create Page Response:", create_response.json())

    # Getting pages
    pages = notion.get_all(num_pages=5)
    print("Retrieved Pages:", pages)

    # Updating a page
    PAGE_ID = "your_page_id_here"
    update_data = {
        "Name": {"title": [{"text": {"content": "Updated Title"}}]},
        "Status": {"select": {"name": "In Progress"}}
    }
    update_response = notion.update_page(page_id=PAGE_ID, data=update_data)
    print("Update Response:", update_response.json())

    # Deleting a page
    delete_response = notion.delete_page(page_id=PAGE_ID)
    print("Delete Response:", delete_response.json())
```

### Error handling

If an API request fails, an exception will be raised with a message indicating the nature of the error. You can catch these exceptions in your application to handle errors gracefully.

```python
try:
    # Your code here
except Exception as e:
    print(f"An error occurred: {e}")
```

## Contributing

Contributions are welcome! If you would like to contribute to this project, please submit a pull request or open an issue to discuss potential changes.