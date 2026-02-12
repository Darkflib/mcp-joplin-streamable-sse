# Joplin Remote MCP server for LLM integration

This project is a server that allows you to interact with your Joplin notes remotely using the Joplin API. It is designed to be used with the MCP (Model Context Protocol) for LLM (Language Model) integration, allowing you to access and manipulate your Joplin notes through natural language commands.

## Features

- Remote access to Joplin notes via API
- Create/move/delete Joplin folders (notebooks)
- Integration with MCP for LLM interaction
- Secure authentication using Joplin API token
- Easy setup and configuration

## Notes

- Ensure you have the Joplin API enabled and a valid API token before using this server.
- This server is intended for use in a secure environment, as it allows remote access to your Joplin notes. Always keep your API token secure and do not expose it publicly.
- The server is designed to be used with LLMs, so it may not have a traditional user interface. It is meant to be accessed programmatically through the MCP protocol.

## Installation

This project uses Streamable HTTP transport (recommended) and runs an MCP endpoint at:

- http://$MCP_HOST:$MCP_PORT/mcp

### Setup (uv)

1. Create a .env from the example:

   - copy .env.example to .env
2. Fill in:

   - JOPLIN_TOKEN
   - MCP_API_KEY
3. Install dependencies:

   - uv sync --all-extras

### Run

- uv run mcp-joplin-streamable-sse

The server is protected by an X-API-Key header. Your MCP client must send:

- X-API-Key: $MCP_API_KEY

## References

[Joplin Data API reference](https://joplinapp.org/help/api/references/rest_api/) -- the API documentation for Joplin, which provides details on how to interact with your notes and other data. Note: this is the data API, the plugin API is different and not used here.

In the documentation below, the token may not be specified every time however you will need to include it.

```bash
curl http://localhost:41184/notes?token=ABCD123ABCD123ABCD123ABCD123ABCD123
curl --data '{ "title": "My note", "body": "Some note in **Markdown**"}' http://localhost:41184/notes
curl -X DELETE http://localhost:41184/tags/ABCD1234/notes/EFGH789
```

## Security

- Do not commit .env
- Rotate JOPLIN_TOKEN if it was ever shared or committed
- Keep MCP bound to 127.0.0.1 unless you have additional network protections
