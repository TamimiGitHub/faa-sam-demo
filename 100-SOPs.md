# Table of Contents

1. [Introduction to FAA Systems](#introduction-to-faa-systems)
   - [FDPS (Flight Data Processing System)](#fdps-flight-data-processing-system)
   - [STDDS (Surface Data Distribution System)](#stdds-surface-data-distribution-system)
2. [Understanding System Documentation with RAG](#understanding-system-documentation-with-rag)
3. [Exercise: Create a RAG agent](#exercise-create-a-rag-agent)
   - [Step 1: Add the RAG Plugin](#step-1-add-the-rag-plugin)
   - [Step 2: Configure the RAG Agent](#step-2-configure-the-rag-agent)
   - [Step 3: Set Up Environment Variables](#step-3-set-up-environment-variables)
   - [Step 4: Create Document Directory](#step-4-create-document-directory)
   - [Step 5: Run the RAG Agent](#step-5-run-the-rag-agent)
   - [Step 6: Verify Agent Setup](#step-6-verify-agent-setup)
4. [Exercise: Analyzing System Documentation](#exercise-analyzing-system-documentation)
   - [Step 1: Upload CONOPS Documents](#step-1-upload-conops-documents)
   - [Step 2: Query the RAG Agent](#step-2-query-the-rag-agent)
5. [Next Steps](#next-steps) The Data Streams - FDPS, STDDS, and RAG

## Introduction to FAA Systems

In this workshop, we'll work with two critical FAA data systems:

### FDPS (Flight Data Processing System)

FDPS is the FAA's primary system for managing flight plan data and tracking aircraft through the National Airspace System (NAS). It processes flight plans, monitors aircraft positions, and coordinates handoffs between air traffic control facilities.

### STDDS (Surface Data Distribution System)

STDDS provides real-time information about aircraft movements on airport surfaces, including taxiways, runways, and ramps. This system is crucial for ground traffic management and preventing runway incursions.

## Understanding System Documentation with RAG

In a real FAA project, each system comes with extensive CONOPS (Concept of Operations) documentation—often exceeding 200 pages per system. We'll use Agent Mesh's RAG (Retrieval-Augmented Generation) capabilities to extract relevant information.

## Exercise: Create a RAG agent

In this exercise, you'll set up a Retrieval Augmented Generation (RAG) agent that can ingest, process, and answer questions about FAA system documentation.

### Step 1: Add the RAG Plugin

1. Open a new terminal session
   ![New Terminal](img/new-terminal.png)

1. Navigate to the `sam` directory and activate the python virtual environment
   ```
   cd sam
   source .venv/bin/activate
   ```

1. Run the following command to add the RAG plugin:

```sh
sam plugin add faa-docs-agent --plugin sam-rag
```

1. This will create a new agent configuration file at `configs/agents/faa-docs-agent.yaml`

### Step 2: Configure the RAG Agent

1. Open `configs/agents/faa-docs-agent.yaml` in your editor and understand the following sections:

   - Scanner Configuration
   - Preprocessor Configuration
   - Splitter Configuration
   - Embedding Configuration
   - Vector Database Configuration
   - LLM Configuration
   - Retrieval Configuration

1. Update `app_config.instructions`
   ```
   You are an Aviation Technical Documentation Specialist with access to a comprehensive knowledge base of Federal Aviation Administration (FAA) systems and operational procedures. Your role is to provide expert-level technical guidance, specifications, and operational context for aviation professionals working with FAA data systems.

        Response Guidelines:
        - Provide concise, accurate answers focused on the specific question asked
        - Include only essential technical details unless comprehensive coverage is specifically requested
        - Use bullet points or structured formats for clarity when listing information
        - Avoid repetitive explanations of basic concepts unless the user is clearly a beginner
        - When searching documents, extract and present only the most relevant information

        You can ingest documents and retrieve relevant information.
        You can search for information in the ingested documents and provide augmented responses.
        Use the 'ingest_document' tool to add new documents to the system.
        Use the 'search_documents' tool to find relevant information based on user queries.
        Utilize this agent for any technical questions related to FAA aviation systems, flight data processing, airport surface operations, or SWIM data integration. The agent provides authoritative, technically accurate responses based on official FAA documentation and operational procedures.
   ```

1. Update the `agent_card.description`
   ```
   "Specialized Aviation Systems Expert with comprehensive access to Federal Aviation Administration (FAA) technical documentation and operational procedures. This RAG agent serves as an authoritative source for aviation professionals requiring detailed technical guidance on FAA data systems, flight operations, and airport surface management."
   ```

1.Update `agent_card.skills.id: "document_retrieval"`
   ```
    - id: "document_retrieval"
      name: "Document Retrieval"
      description: "Provide context about aviation and faa data. This includes information about enroute flights, the format and structure of the data"
      examples:
         - "What is the structure of the FDPSPosition collection in a JSON Schema format"
         - "Find documents related to machine learning algorithms."
   ```

### Step 3: Set Up Environment Variables

Update your `.env` file with the necessary variables. Your workshop instructor will provide the specific values for your environment.

```
## Qdrant Configuration
QDRANT_URL="<qdrant_url>:6333"
QDRANT_API_KEY="<API_KEY>"
QDRANT_COLLECTION="SOP"
QDRANT_EMBEDDING_DIMENSION=1536
OPENAI_EMBEDDING_MODEL="text-embedding-ada-002"
DOCUMENTS_PATH="faa_documents"
```

### Step 4: Create Document Directory

1. Create a directory for your FAA documentation:

```sh
mkdir -p faa_documents
```

_This directory will be used in the next exercise to store the FDPS and STDDS CONOPS documents_

### Step 5: Run the RAG Agent

1. Start your RAG agent with the following command:

```sh
sam run configs/agents/faa-docs-agent.yaml
```

1. The agent will initialize and connect to your vector database.
1. It will be ready to scan and ingest documents in the next exercise.

### Step 6: Verify Agent Setup

1. Check the terminal output for any errors.
1. Verify that the agent has successfully connected to:
   - The Solace broker
   - The vector database
1. If you see any connection errors, double-check your environment variables and configuration.

## Exercise: Analyzing System Documentation

### Step 1: Upload CONOPS Documents

1. Navigate to the Agent Mesh WebUI.
1. Upload the FDPS CONOPS document to Agent Mesh.
1. Upload the STDDS CONOPS document to Agent Mesh.
1. Use the following prompt:

   ```
   Upload the following documents to my vector database
   ```

### Step 2: Query the RAG Agent

Use the RAG agent to analyze the uploaded documentation by running the following prompts:

```
Tell me about the FDPS and STDDS systems and data.
```

Wait for the response, review the summary, then proceed with the next prompt:

```
Tell me what types of outcomes I could expect by analyzing data from these systems.
```

The RAG agent will provide:
- High-level overviews of each system's purpose and functionality
- Descriptions of the data structures and key fields
- Insights into potential analysis opportunities
- Relationships between the two systems

This approach is significantly more efficient than reading hundreds of pages of technical documentation manually.

## Next Steps

In the next part, we'll explore setting up the data layer for our workshop environment. We'll dive into the DocumentDB instance that serves as the foundation for our real-time flight data analysis.

[Continue to Setting Up the Data Layer](200-Data-Layer.md)