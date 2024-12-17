# markitdown-azure-function

An Azure Functions implementation of the markitdown library that converts various file formats to Markdown. This service accepts base64 encoded files and returns their content in Markdown format.

## Features

- Supports multiple file formats:
  - PDF (.pdf)
  - Word Documents (.docx)
  - Excel Spreadsheets (.xlsx)
  - PowerPoint Presentations (.pptx)
  - HTML files (.html, .htm)
  - Plain text files (.txt)
  - Images (.jpg, .jpeg, .png)
  - Audio files (.wav, .mp3) with metadata
  - ZIP archives

- Special handling for:
  - Wikipedia pages
  - YouTube pages (including transcript extraction)
  - Bing search results

## Prerequisites

- Python 3.9 or later
- Azure Functions Core Tools
- Azure subscription (for deployment)

## Local Development Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/markitdown-azure-function.git
cd markitdown-azure-function
```

2. Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows use: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create local.settings.json:
```json
{
    "IsEncrypted": false,
    "Values": {
        "FUNCTIONS_WORKER_RUNTIME": "python",
        "AzureWebJobsStorage": "UseDevelopmentStorage=true"
    }
}
```

5. Run the function locally:
```bash
func start
```

## Usage

Send a POST request to the `/api/convert` endpoint:

```json
{
    "file": "base64_encoded_file_content",
    "extension": ".pdf"
}
```

Response format:

```json
{
    "title": "Document Title (if available)",
    "content": "Markdown formatted content"
}
```

### Example using curl:

```bash
curl -X POST https://your-function-app.azurewebsites.net/api/convert \
     -H "Content-Type: application/json" \
     -H "x-functions-key: your-function-key" \
     -d '{"file": "base64_encoded_content", "extension": ".pdf"}'
```

### Example using Power Automate:

1. Use "Get file content" action to read the file
2. Convert to base64 using the expression: `base64(body('Get_file_content'))`
3. Send HTTP POST request with the following configuration:
   - Method: POST
   - URI: Your function endpoint
   - Headers:
     - Content-Type: application/json
     - x-functions-key: Your function key
   - Body: 
     ```json
     {
         "file": "@{outputs('Base64_conversion')}",
         "extension": ".pdf"
     }
     ```

## Deployment

1. Create an Azure Function App:
```bash
az functionapp create --name your-app-name --storage-account your-storage --consumption-plan-location your-location --runtime python
```

2. Deploy the function:
```bash
func azure functionapp publish your-app-name
```

## Error Handling

The API returns different status codes based on the error type:

- 400: Invalid request (missing or invalid file content)
- 415: Unsupported file format
- 422: File conversion error
- 500: Internal server error

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Based on the [markitdown](https://github.com/microsoft/markitdown) library by Microsoft
- Uses various open-source libraries for file format conversion