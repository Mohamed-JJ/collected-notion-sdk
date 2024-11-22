class NotionCRUD {
    /**
     * A class for interacting with the Notion API to perform CRUD operations on a database.
     * @param {string} secretKey - The secret key for authenticating with the Notion API.
     * @param {string} databaseId - The ID of the Notion database to interact with.
     */
    constructor(secretKey, databaseId) {
        this.secretKey = secretKey;
        this.databaseId = databaseId;
        this.headers = {
            "Authorization": `Bearer ${this.secretKey}`,
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28" // Adjust version as necessary
        };
    }

    async getAll(numPages = null) {
        const url = `https://api.notion.com/v1/databases/${this.databaseId}/query`;
        const pageSize = numPages === null ? 100 : numPages;
        const payload = { "page_size": pageSize };

        const response = await fetch(url, {
            method: 'POST',
            headers: this.headers,
            body: JSON.stringify(payload)
        });

        if (!response.ok) {
            throw new Error(`Failed to fetch pages: ${await response.text()}`);
        }

        const data = await response.json();
        let results = data.results;

        while (data.has_more) {
            payload.start_cursor = data.next_cursor;
            const nextResponse = await fetch(url, {
                method: 'POST',
                headers: this.headers,
                body: JSON.stringify(payload)
            });

            if (!nextResponse.ok) {
                throw new Error(`Failed to fetch more pages: ${await nextResponse.text()}`);
            }

            const nextData = await nextResponse.json();
            results = results.concat(nextData.results);
        }

        return results;
    }

    async createPage(data) {
        const createUrl = "https://api.notion.com/v1/pages";
        const payload = {
            "parent": { "database_id": this.databaseId },
            "properties": data
        };

        const response = await fetch(createUrl, {
            method: 'POST',
            headers: this.headers,
            body: JSON.stringify(payload)
        });

        if (!response.ok) {
            throw new Error(`Failed to create page: ${await response.text()}`);
        }

        return response.json();
    }

    async updatePage(pageId, data) {
        const url = `https://api.notion.com/v1/pages/${pageId}`;
        const payload = { "properties": data };

        const response = await fetch(url, {
            method: 'PATCH',
            headers: this.headers,
            body: JSON.stringify(payload)
        });

        if (!response.ok) {
            throw new Error(`Failed to update page: ${await response.text()}`);
        }

        return response.json();
    }

    async deletePage(pageId) {
        const url = `https://api.notion.com/v1/pages/${pageId}`;
        const payload = { "archived": true };

        const response = await fetch(url, {
            method: 'PATCH',
            headers: this.headers,
            body: JSON.stringify(payload)
        });

        if (!response.ok) {
            throw new Error(`Failed to delete page: ${await response.text()}`);
        }

        return response.json();
    }
}