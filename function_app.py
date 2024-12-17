import azure.functions as func
import logging
import json
import base64
import tempfile
import os
from markitdown import MarkItDown, FileConversionException, UnsupportedFormatException

app = func.FunctionApp()

@app.route(route="convert", auth_level=func.AuthLevel.FUNCTION)
async def convert_to_markdown(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    try:
        # Get request body
        req_body = req.get_json()
        
        if not req_body or 'file' not in req_body:
            return func.HttpResponse(
                json.dumps({
                    "error": "Please pass a base64 encoded file in the request body"
                }),
                mimetype="application/json",
                status_code=400
            )

        file_content = req_body.get('file')
        file_extension = req_body.get('extension', '')

        # Decode base64 content
        try:
            decoded_content = base64.b64decode(file_content)
        except Exception as e:
            return func.HttpResponse(
                json.dumps({
                    "error": f"Invalid base64 content: {str(e)}"
                }),
                mimetype="application/json",
                status_code=400
            )

        # Create a temporary file
        handle, temp_path = tempfile.mkstemp(suffix=file_extension)
        
        try:
            with os.fdopen(handle, 'wb') as temp_file:
                temp_file.write(decoded_content)
            
            # Initialize MarkItDown converter
            converter = MarkItDown()
            
            # Convert the file
            result = converter.convert_local(
                temp_path,
                file_extension=file_extension
            )

            # Prepare response
            response_data = {
                "title": result.title,
                "content": result.text_content
            }

            return func.HttpResponse(
                body=json.dumps(response_data),
                mimetype="application/json",
                status_code=200
            )

        except FileConversionException as e:
            return func.HttpResponse(
                json.dumps({
                    "error": f"File conversion error: {str(e)}"
                }),
                mimetype="application/json",
                status_code=422
            )
        except UnsupportedFormatException as e:
            return func.HttpResponse(
                json.dumps({
                    "error": f"Unsupported format: {str(e)}"
                }),
                mimetype="application/json",
                status_code=415
            )
        except Exception as e:
            logging.error(f"Error converting file: {str(e)}")
            return func.HttpResponse(
                json.dumps({
                    "error": f"Internal server error: {str(e)}"
                }),
                mimetype="application/json",
                status_code=500
            )
        
        finally:
            # Clean up temporary file
            try:
                os.unlink(temp_path)
            except:
                pass

    except Exception as e:
        logging.error(f"Error processing request: {str(e)}")
        return func.HttpResponse(
            json.dumps({
                "error": f"Internal server error: {str(e)}"
            }),
            mimetype="application/json",
            status_code=500
        )