# Define the JSON schema
schema = {
    "type": "object",
    "properties": {
        "filename": {"type": "string"},
        "sheet": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "title": {"type": "string"},
                    "data": {
                        "type": "object",
                        "properties": {
                            "header": {"type": "array", "items": {"type": "string"}},
                            "data": {
                                "type": "array",
                                "items": {
                                    "type": "array",
                                    "items": {"type": "string"}
                                }
                            }
                        },
                        "required": ["header", "data"]
                    }
                },
                "required": ["title", "data"]
            }
        }
    },
    "required": ["filename", "sheet"]
}
