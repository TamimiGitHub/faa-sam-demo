1. Clone the MCP server
    ```
    git clone https://github.com/jschabowsky/aviation-mcp.git
    cd aviation-mcp
    ```

1. Install nodejs
    ```
    sudo dnf install -y nodejs
    ```

1. Install dependencies:

   ```bash
   npm install
   ```

1. Build the server (this will fetch the latest Swagger definition, generate the API client, and compile the TypeScript):

   ```bash
   npm run build
   ```

1. Create ECR Repository:

   ```
   aws ecr create-repository --repository-name mcp-server --region us-east-1
   ```