# Creating DocumentDB Agents in Agent Mesh

## Table of Contents
- [Step 1: Create the FDPS DocumentDB Agent](#step-1-create-the-fdps-documentdb-agent)
  - [Configure Agent Settings](#step-1-create-the-fdps-documentdb-agent)
  - [Update Environment Variables](#step-1-create-the-fdps-documentdb-agent)
  - [Run the Agent](#step-1-create-the-fdps-documentdb-agent)
- [Step 2: Create the STDDS DocumentDB Agent](#step-2-create-the-stdds-documentdb-agent)
  - [Configure Agent Settings](#step-2-create-the-stdds-documentdb-agent)
  - [Update Environment Variables](#step-2-create-the-stdds-documentdb-agent)
  - [Run the Agent](#step-2-create-the-stdds-documentdb-agent)
- [Verify Agent Availability](#verify-agent-availability)
  - [Test the FDPS Agent](#test-the-fdps-agent)
  - [Test the STDDS Agent](#test-the-stdds-agent)
  - [Review the Data Structures](#review-the-data-structures)
- [Next Steps](#next-steps)

Now that you understand the data layer, it's time to build agent that will connect to your DocumentDB collections. You'll create dedicated agents for each data source to enable parallel processing and maintain a clean architectural separation.

## Step 1: Create the FDPS DocumentDB Agent

1. Open a new terminal session
   ![New Terminal](img/new-terminal.png)

1. Navigate to the `sam` directory and activate the python virtual environment
   ```
   cd sam
   source .venv/bin/activate
   ```

1. Run the following command to add the RAG plugin:

   ```sh
   sam plugin add flight-db --plugin sam-mongodb
   ```
   Note: observe the newly created `flight-db.yaml` file under `configs/agents`

1. Open the newly created file and make the following changes
   1. Uncomment `!include ../shared_config.yaml` on line 13

   1. Since we are importing a shared configuration, remove the `shared_config:` block from 14-43

   1. Update the `app_config.instruction` to the following
      ```
      You are the FDPS DocumentDB agent, an expert MongoDB assistant specialized in Flight Data Processing System (FDPS) data analysis. Your primary goal is to translate user questions about flight operations into accurate and efficient MongoDB aggregation pipelines for a database containing real-time flight telemetry and control system data.

        Response Guidelines:
        - Provide direct, concise answers to queries
        - Present query results in clear, structured formats (tables when appropriate)
        - Only include pipeline explanations when specifically requested
        - Focus on the data requested, not extensive background information
        - For multiple results, summarize key patterns rather than listing every record unless specifically requested

        ====================
        DATA STRUCTURE KNOWLEDGE
        ====================

        DOCUMENT STRUCTURE:
        All documents follow this root pattern:
        {
          "_id": "ObjectId",
          "message": {
            "flight": { /* primary flight data */ }
          },
          "time": "timestamp",
          "messageType": "string"
        }

        KEY FLIGHT FIELDS:
        - Aircraft ID: message.flight.flightIdentification.aircraftIdentification
        - GUFI (Primary Key): message.flight.gufi.text
        - Centre: message.flight.center
        - System: message.flight.system
        - Position Lat/Lon: message.flight.enRoute.position.position.location.pos
        - Altitude: message.flight.enRoute.position.altitude.text
        - Ground Speed: message.flight.enRoute.position.actualSpeed.surveillance.text
        - Flight Status: message.flight.flightStatus.fdpsFlightStatus
        - Departure Airport: message.flight.departure.departurePoint
        - Arrival Airport: message.flight.arrival.arrivalPoint
        - ATC Unit: message.flight.controllingUnit.unitIdentifier

        ====================
        VALID DATA VALUES
        ====================

        FLIGHT STATUS CODES FOR message.flight.flightStatus.fdpsFlightStatus:
        - ACTIVE: The flight is airborne and currently being tracked in the NAS
        - FILED: A flight plan has been filed, but the flight has not yet departed or been activated
        - PROPOSED: A flight plan is being coordinated or is in a preliminary state
        - CANCELED: The flight has been officially canceled by the operator
        - DEPARTED: The flight has taken off, often used temporarily before switching to ACTIVE
        - LANDED: The flight has successfully arrived at its destination and is no longer active in the NAS
        - CLOSED: The flight record is no longer active or relevant for real-time tracking (often follows LANDED)

        GUFI FORMAT for message.flight.gufi.text:
        - The GUFI (Globally Unique Flight Identifier) is a UUIDv4 formatted as a 32 character hexadecimal string with hyphens: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
          Example: "123e4567-e89b-12d3-a456-426614174000"

        IDENTIFIER FIELDS:
        - Aircraft ID (message.flight.flightIdentification.aircraftIdentification): Alphanumeric callsign assigned to the aircraft
        - Centre (message.flight.center): Three-letter code representing the ATC center managing the flight
        - System (message.flight.system): Code indicating the data source system (e.g., "FDPS", "ADS-B")
        - Position Lat/Lon (message.flight.enRoute.position.position.location.pos): String formatted as "latitude longitude" (e.g., "34.0522 -118.2437")
        - Airport Codes (message.flight.departure.departurePoint and message.flight.arrival.arrivalPoint): Standard ICAO airport codes (e.g., "KJFK", "KLAX")

        PIPELINE BEST PRACTICES
        ====================

        MANDATORY PRACTICES:
        1. ALWAYS prefix flight fields with "message.flight."
        2. CONVERT string numerics to numbers using $toDouble for calculations
        3. HANDLE null values in optional fields
        4. USE time-based filtering for recent data queries
        5. FILTER early in pipeline for performance
      ```
   1. Make sure the `agent_init_function` looks like this. Note the different `db_host` `db_port` `db_user` `db_password` `db_name` values
      ```
      config:
          db_host: "${SAM_DOCUMENTDB_MONGO_HOST}"
          db_port: "${SAM_DOCUMENTDB_MONGO_PORT}"
          db_user: "${SAM_DOCUMENTDB_MONGO_USER}"
          db_password: "${SAM_DOCUMENTDB_MONGO_PASSWORD}"
          db_name: "${SAM_DOCUMENTDB_MONGO_DB}"
          database_collection: "${FLIGHT_DB_MONGO_COLLECTION}"
          database_purpose: "${FLIGHT_DB_DB_PURPOSE}"
          data_description: "${FLIGHT_DB_DB_DESCRIPTION}"
          auto_detect_schema: ${AUTO_DETECT_SCHEMA, true}
          max_inline_results: ${MAX_INLINE_RESULTS, 10}
      ```
   1. Update your `.env` to add the following env vars
      ```
      SAM_DOCUMENTDB_MONGO_HOST="<documentDB_host>" # e.g. faa-data.cluster-cmllhe9ilflq.us-west-2.docdb.amazonaws.com
      SAM_DOCUMENTDB_MONGO_PORT="27017"
      SAM_DOCUMENTDB_MONGO_USER="faa"="faa"
      SAM_DOCUMENTDB_MONGO_PASSWORD="faaistheb3st"
      SAM_DOCUMENTDB_MONGO_DB="FAAData"

      ## FDPS Position Collection
      FLIGHT_DB_MONGO_COLLECTION="FDPSPosition"
      FLIGHT_DB_DB_PURPOSE="this database includes information about enroute flights including location, speed, and altitude"
      FLIGHT_DB_DB_DESCRIPTION="data includes which artcc center the aircraft is in, the departure and arrival information along with its current enroute position (latitude, longitude), actual speed (KNOTS), altitude along with the flight number (AircractIdentification) and flight plan id."
      ```
   1. Update the agent card description
      ```
       description: "You are an intelligent Flight Data Analysis Agent with direct access to a database containing real-time flight telemetry   and control system data.
                      Your role is to interpret, query, and analyze structured flight information. You can extract insights, summarize data, answer technical queries, and correlate information across records.
                      Each record in the database represents a single flight event snapshot.
                      This data is typically sourced from air traffic control systems, flight data processing systems (FDPS), and ADS-B surveillance feeds."
      ```
   1. Update the `skills` section to 
      ```
      skills:
          - id: "mongo_query"
            name: "mongo_query"
            description: "Answers questions by querying the connected DocumentDB database and the FDPSPosition collection."
      ```

   1. The final agent yaml config should look like this
      ```
      log:
         stdout_log_level: INFO
         log_file_level: INFO
         log_file: fdps.log

      # To use the `shared_config.yaml` file, uncomment the following line and remove the `shared_config` section below.
      !include ../shared_config.yaml

      apps:
      - name: fdps-app
         app_module: solace_agent_mesh.agent.sac.app
         broker:
            <<: *broker_connection
         app_config:
            namespace: "${NAMESPACE}"
            agent_name: "fdpsDocumentdb"
            display_name: "Flight Data (FDPS) Agent"
            supports_streaming: false

            model: *general_model
            instruction: |
            You are the FDPS DocumentDB agent, an expert MongoDB assistant specialized in Flight Data Processing System (FDPS) data analysis. Your primary goal is to translate user questions about flight operations into accurate and efficient MongoDB aggregation pipelines for a database containing real-time flight telemetry and control system data.

            Response Guidelines:
            - Provide direct, concise answers to queries
            - Present query results in clear, structured formats (tables when appropriate)
            - Only include pipeline explanations when specifically requested
            - Focus on the data requested, not extensive background information
            - For multiple results, summarize key patterns rather than listing every record unless specifically requested

            ====================
            DATA STRUCTURE KNOWLEDGE
            ====================

            DOCUMENT STRUCTURE:
            All documents follow this root pattern:
            {
               "_id": "ObjectId",
               "message": {
                  "flight": { /* primary flight data */ }
               },
               "time": "timestamp",
               "messageType": "string"
            }

            KEY FLIGHT FIELDS:
            - Aircraft ID: message.flight.flightIdentification.aircraftIdentification
            - GUFI (Primary Key): message.flight.gufi.text
            - Centre: message.flight.center
            - System: message.flight.system
            - Position Lat/Lon: message.flight.enRoute.position.position.location.pos
            - Altitude: message.flight.enRoute.position.altitude.text
            - Ground Speed: message.flight.enRoute.position.actualSpeed.surveillance.text
            - Flight Status: message.flight.flightStatus.fdpsFlightStatus
            - Departure Airport: message.flight.departure.departurePoint
            - Arrival Airport: message.flight.arrival.arrivalPoint
            - ATC Unit: message.flight.controllingUnit.unitIdentifier

            ====================
            VALID DATA VALUES
            ====================

            FLIGHT STATUS CODES FOR message.flight.flightStatus.fdpsFlightStatus:
            - ACTIVE: The flight is airborne and currently being tracked in the NAS
            - FILED: A flight plan has been filed, but the flight has not yet departed or been activated
            - PROPOSED: A flight plan is being coordinated or is in a preliminary state
            - CANCELED: The flight has been officially canceled by the operator
            - DEPARTED: The flight has taken off, often used temporarily before switching to ACTIVE
            - LANDED: The flight has successfully arrived at its destination and is no longer active in the NAS
            - CLOSED: The flight record is no longer active or relevant for real-time tracking (often follows LANDED)

            GUFI FORMAT for message.flight.gufi.text:
            - The GUFI (Globally Unique Flight Identifier) is a UUIDv4 formatted as a 32 character hexadecimal string with hyphens: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
               Example: "123e4567-e89b-12d3-a456-426614174000"

            IDENTIFIER FIELDS:
            - Aircraft ID (message.flight.flightIdentification.aircraftIdentification): Alphanumeric callsign assigned to the aircraft
            - Centre (message.flight.center): Three-letter code representing the ATC center managing the flight
            - System (message.flight.system): Code indicating the data source system (e.g., "FDPS", "ADS-B")
            - Position Lat/Lon (message.flight.enRoute.position.position.location.pos): String formatted as "latitude longitude" (e.g., "34.0522 -118.2437")
            - Airport Codes (message.flight.departure.departurePoint and message.flight.arrival.arrivalPoint): Standard ICAO airport codes (e.g., "KJFK", "KLAX")

            PIPELINE BEST PRACTICES
            ====================

            MANDATORY PRACTICES:
            1. ALWAYS prefix flight fields with "message.flight."
            2. CONVERT string numerics to numbers using $toDouble for calculations
            3. HANDLE null values in optional fields
            4. USE time-based filtering for recent data queries
            5. FILTER early in pipeline for performance

            agent_init_function:
            module: "sam_mongodb.lifecycle"
            name: "initialize_mongo_agent"
            config:
               db_host: "${SAM_DOCUMENTDB_MONGO_HOST}"
               db_port: ${SAM_DOCUMENTDB_MONGO_PORT}
               db_user: "${SAM_DOCUMENTDB_MONGO_USER}"
               db_password: "${SAM_DOCUMENTDB_MONGO_PASSWORD}"
               db_name: "${SAM_DOCUMENTDB_MONGO_DB}"
               database_collection: "${SAM_DOCUMENTDB_MONGO_COLLECTION}"
               database_purpose: "${SAM_DOCUMENTDB_DB_PURPOSE}"
               data_description: "${SAM_DOCUMENTDB_DB_DESCRIPTION}"
               auto_detect_schema: ${AUTO_DETECT_SCHEMA, true}
               max_inline_results: ${MAX_INLINE_RESULTS, 10}

            agent_cleanup_function:
            module: "sam_mongodb.lifecycle"
            name: "cleanup_mongo_agent_resources"

            tools:
            - tool_type: builtin-group
               group_name: "artifact_management"
            - tool_type: builtin-group
               group_name: "data_analysis"
            - tool_type: python
               component_module: "sam_mongodb.search_query"
               function_name: "mongo_query"
               tool_config:
                  collection: "${SAM_DOCUMENTDB_MONGO_COLLECTION}"

            session_service: *default_session_service
            artifact_service: *default_artifact_service

            artifact_handling_mode: "embed"
            enable_embed_resolution: true
            enable_artifact_content_instruction: true

            agent_card:
            description: "You are an intelligent Flight Data Analysis Agent with direct access to a database containing real-time flight telemetry and control system data.
                           Your role is to interpret, query, and analyze structured flight information. You can extract insights, summarize data, answer technical queries, and correlate information across records.
                           Each record in the database represents a single flight event snapshot.
                           This data is typically sourced from air traffic control systems, flight data processing systems (FDPS), and ADS-B surveillance feeds."
            defaultInputModes: ["text"]
            defaultOutputModes: ["text", "file"]
            skills:
               - id: "mongo_query"
                  name: "mongo_query"
                  description: "Answers questions by querying the connected DocumentDB database and the FDPSPosition collection."

            agent_card_publishing:
            interval_seconds: 30

            agent_discovery:
            enabled: false

            inter_agent_communication:
            allow_list: []
            request_timeout_seconds: 30
         ```
1. Save the fle and run it
   ``` 
   sam run configs/agents/flight-db.yaml
   ```

1. Navigate back to the SAM WebUI instance and observe the new agent

## Step 2: Create the STDDS DocumentDB Agent
1. Open a new terminal session
   ![New Terminal](img/new-terminal.png)

1. Navigate to the `sam` directory and activate the python virtual environment
   ```
   cd sam
   source .venv/bin/activate
   ```

1. Run the following command to add the RAG plugin:

   ```sh
   sam plugin add sttds-db --plugin sam-mongodb
   ```
   Note: observe the newly created `sttds-db.yaml` file under `configs/agents`

1. Open the newly created file and paste the following content
   ```
   log:
      stdout_log_level: INFO
      log_file_level: INFO
      log_file: stdds-documentdb.log

   # To use the `shared_config.yaml` file, uncomment the following line and remove the `shared_config` section below.
   !include ../shared_config.yaml

   apps:
   - name: stdds-documentdb-app
      app_module: solace_agent_mesh.agent.sac.app
      broker:
         <<: *broker_connection
      app_config:
         namespace: "${NAMESPACE}"
         agent_name: "stddsDocumentdb"
         display_name: "Surface Movements (STDDS) Agent"
         supports_streaming: true

         model: *general_model
         instruction: |
         You are the STDDS DocumentDB agent, an expert MongoDB assistant specialized in Surface Traffic Data Display System (STDDS) data analysis. Your primary goal is to translate user questions about aircraft surface operations into accurate and efficient MongoDB aggregation pipelines for a database containing real-time airport surface movement data.

         Response Guidelines:
         - Provide direct, concise answers to surface operations queries
         - Present data in structured formats (tables for multiple results)
         - Only explain pipeline logic when specifically requested
         - Focus on answering the specific question asked
         - For airport activity queries, summarize key patterns and metrics

         ====================
         DATA STRUCTURE KNOWLEDGE
         ====================

         DOCUMENT STRUCTURE:
         {
            "_id": "ObjectId",
            "SurfaceMovementEventMessage": { /* primary data */ },
            "timestamp": "ISO8601",
            "messageType": "string"
         }

         KEY FIELDS:
         - SurfaceMovementEventMessage.callsign: Aircraft identifier (e.g., "AAL100")
         - SurfaceMovementEventMessage.track: Track number
         - SurfaceMovementEventMessage.stid: Surface track ID
         - SurfaceMovementEventMessage.airport: ICAO airport code (e.g., "KJFK", "KDFW")
         - SurfaceMovementEventMessage.aircraftType: ICAO aircraft type (e.g., "B77W", "A321")
         - SurfaceMovementEventMessage.event: Event type ["spotout", "runwayin", "runwayout", "on", "off"]
         - SurfaceMovementEventMessage.status: Current status ["onsurface", "onrunway", "airborne"]
         - runway: Runway identifier (when applicable, e.g., "04L/22R")
         - position: {latitude, longitude}
         - altitude: Altitude in feet
         - time: Event timestamp


         agent_init_function:
         module: "sam_mongodb.lifecycle"
         name: "initialize_mongo_agent"
         config:
            db_host: "${SAM_DOCUMENTDB_MONGO_HOST}"
            db_port: ${SAM_DOCUMENTDB_MONGO_PORT}
            db_user: "${SAM_DOCUMENTDB_MONGO_USER}"
            db_password: "${SAM_DOCUMENTDB_MONGO_PASSWORD}"
            db_name: "${SAM_DOCUMENTDB_MONGO_DB}"
            database_collection: "${SAM_DOCUMENTDB_STDDS_COLLECTION}"
            database_purpose: "${SAM_DOCUMENTDB_STDDS_DB_PURPOSE}"
            data_description: "${SAM_DOCUMENTDB_STDDS_DB_DESCRIPTION}"
            auto_detect_schema: ${AUTO_DETECT_SCHEMA, true}
            max_inline_results: ${MAX_INLINE_RESULTS, 10}

         agent_cleanup_function:
         module: "sam_mongodb.lifecycle"
         name: "cleanup_mongo_agent_resources"

         tools:
         - tool_type: builtin-group
            group_name: "artifact_management"
         - tool_type: builtin-group
            group_name: "data_analysis"
         - tool_type: python
            component_module: "sam_mongodb.search_query"
            function_name: "mongo_query"
            tool_config:
               collection: "${SAM_DOCUMENTDB_STDDS_COLLECTION}"

         session_service: *default_session_service
         artifact_service: *default_artifact_service

         artifact_handling_mode: "embed"
         enable_embed_resolution: true
         enable_artifact_content_instruction: true

         agent_card:
         description: "This agent provides real-time insights from FAA surface movement data, including aircraft and vehicle positions, runway events, and departure activities. It can query, filter, and summarize surface operations at specific airports to support situational awareness and performance analysis. Users can ask it for details like 'Which aircraft are taxiing at JFK?' or 'Show recent runway crossings at LAX.'"
         defaultInputModes: ["text"]
         defaultOutputModes: ["text", "file"]
         skills:
            - id: "mongo_query"
               name: "mongo_query"
               description: "Answers questions by querying the connected DocumentDB database and the STDDSPosition collection."

         agent_card_publishing:
         interval_seconds: 30

         agent_discovery:
         enabled: false

         inter_agent_communication:
         allow_list: []
         request_timeout_seconds: 30
   ```

1. Update the `.env` file to have the following vars
   ```
   ## STDDS Position Collection
   SAM_DOCUMENTDB_STDDS_COLLECTION="STDDSPosition"
   SAM_DOCUMENTDB_STDDS_DB_PURPOSE="this database includes information about flight surface data"
   SAM_DOCUMENTDB_STDDS_DB_DESCRIPTION="The STDDS database contains real-time FAA flight tracking records that capture comprehensive aircraft operational data including precise GPS coordinates, altitude, speed, velocity vectors, flight identification details, route information, departure and arrival airports, runway usage times, ADS-B surveillance broadcasts, and current flight status, providing a complete situational awareness picture for air traffic management, surface movement monitoring, and aviation safety analysis across the national airspace system."
   ```

1. Save the fle and run it
   ``` 
   sam run configs/agents/sttds-db.yaml
   ```

1. Navigate back to the SAM WebUI instance and observe the new agent

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