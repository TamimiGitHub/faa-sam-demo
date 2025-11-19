# Part 3: Creating DocumentDB Agents in Agent Mesh

Now that you understand the data layer, it's time to connect Agent Mesh to your DocumentDB collections. You'll create dedicated agents for each data source to enable parallel processing and maintain a clean architectural separation.

## Step 1: Create the FDPS DocumentDB Agent

1. In the Agent Mesh interface, navigate to the "Agents" section.
2. Click on "Add New Agent" and select "DocumentDB Agent" from the list of available agent types.
3. Configure the FDPS agent with the following settings:
   - Name: FDPS Agent
   - Collection: FDPSPosition
   - Connection String: (Use the provided DocumentDB connection string)
   - Database Name: FAA_Data (or as specified in your environment)

4. Test the connection to ensure the agent can successfully query the FDPSPosition collection.

## Step 2: Create the STDDS DocumentDB Agent

1. Repeat the process to create another DocumentDB agent.
2. Configure the STDDS agent with these settings:
   - Name: STDDS Agent
   - Collection: STDDSPosition
   - Connection String: (Use the same DocumentDB connection string)
   - Database Name: FAA_Data (or as specified in your environment)

3. Test the connection to verify access to the STDDSPosition collection.

## Step 3: Test the Agent Connections

### Start the Agent Mesh Interface

1. Ensure Agent Mesh is running in your environment.
2. Open a web browser and navigate to the Agent Mesh interface URL (format: `http://<your-workshop-url>:8000`).

### Verify Agent Availability

1. Navigate to the "Agents" tab or section.
2. Confirm that you see both newly created agents:
   - FDPS Agent
   - STDDS Agent
3. Verify that both agents show as "Available" or "Online".

### Test the FDPS Agent

In the Agent Mesh chat or query interface, run the following prompt:

```
Get me an example document from the FDPS database.
```

**Expected Response:**

The agent should return a JSON document showing the structure of FDPS data, including fields such as:
- Aircraft identifier (flight number, tail number)
- Position data (latitude, longitude, altitude)
- Speed and heading
- Flight plan information
- Status indicators
- Timestamp

### Test the STDDS Agent

Run the following prompt:

```
Get me an example document from the STDDS database.
```

**Expected Response:**

The agent should return a JSON document showing the structure of STDDS data, including fields such as:
- Aircraft identifier
- Ground position coordinates
- Surface location (runway, taxiway, ramp)
- Ground speed and direction
- Surface status
- Timestamp

### Review the Data Structures

Examine the returned documents carefully to understand:
- Available fields and their data types
- Field naming conventions
- Data formats (especially for timestamps and coordinates)
- Relationships between different fields

This knowledge will be essential for formulating effective natural language queries in the next section.

## Next Steps

Now that we have our DocumentDB agents set up and connected, we're ready to start querying our flight data using natural language. In the next part, we'll explore how to ask questions about our data and interpret the results.

[Continue to Part 4: Asking Questions in Natural Language](400-Natural-Language.md)