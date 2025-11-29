# Adding Flight Plan Intelligence

To perform more sophisticated analysis, such as comparing actual flight paths to planned routes, you need access to flight plan data. In this section, you'll add another DocumentDB agent to access this information.

## Understanding Flight Plan Data

Flight plans contain:
- Planned route waypoints and altitudes
- Estimated times for each waypoint
- Alternate airports and contingency routes
- Fuel calculations and aircraft performance data
- Filed vs. actual departure times

## Step 1: Create the Flight Plan DocumentDB Agent

1. Open a new terminal session
   ![New Terminal](img/new-terminal.png)

1. Navigate to the `sam` directory and activate the python virtual environment
   ```
   cd sam
   source .venv/bin/activate
   ```

1. Run the following command to add the RAG plugin:

   ```sh
   sam plugin add flightPlan --plugin sam-mongodb
   ```
   Note: observe the newly created `flightPlan.yaml` file under `configs/agents`

1. Open the newly created file and paste the following content:

   ```
   # Plugin Metadata:
   # Name: sam-mongodb
   # Version: 0.1.0
   # Description: A plugin that provides a MongoDB agent to perform complex queries based on natural language.
   # Author: SolaceLabs <solacelabs@solace.com>

   log:
   stdout_log_level: INFO
   log_file_level: INFO
   log_file: flightplan.log

   # To use the `shared_config.yaml` file, uncomment the following line and remove the `shared_config` section below.
   !include ../shared_config.yaml

   apps:
   - name: flightplan-app
      app_module: solace_agent_mesh.agent.sac.app
      broker:
         <<: *broker_connection
      app_config:
         namespace: "${NAMESPACE}"
         agent_name: "flightplanDocumentdb"
         display_name: "Flight Plan Agent"
         supports_streaming: false

         model: *general_model
         instruction: |
         You are the FlightPlan DocumentDB agent, an expert MongoDB assistant specialized in analyzing FAA Flight Data Processing System (FDPS) flight plan records, translating aviation operations questions into precise aggregation pipelines for comprehensive flight plan data including aircraft capabilities, routing, ATC coordination, and flight lifecycle management.

         PURPOSE:
         Analyze flight plan data to support air traffic control operations, flight tracking, route optimization, and aviation safety initiatives across the National Airspace System.

         DATABASE: FDPSFlightPlan Collection
         Contains real-time flight plan records from FAA's ERAM system with comprehensive aircraft information, routing details, equipment capabilities, ATC coordination data, and flight status tracking for commercial and general aviation operations.
         Flight Data Processing System (FDPS) records are comprehensive JSON documents that capture complete flight plan information from the FAA's En Route Automation Modernization (ERAM) system. Each record represents a single flight's operational data including aircraft specifications, routing, equipment capabilities, ATC coordination, and real-time status information.

         DOCUMENT STRUCTURE:
            Flight data records follow a three-level hierarchical structure:
            1. Top Level: MongoDB document metadata
            2. Message Level: Flight plan message container
            3. Flight Level: Detailed operational data

         RECORD STRUCTURE OVERVIEW:
         {
            "_id": "ObjectId",
            "message": {
               "flight": {
               // Core Identification
               "flightIdentification": {
                  "aircraftIdentification": "AAL21",    // Call sign
                  "computerId": "524",                  // System processing ID
                  "siteSpecificPlanId": "272"          // Local facility ID
               },
               "gufi": {
                  "codeSpace": "urn:uuid",
                  "text": "935f5836-8c19-44cb-b971-1f5ef6f6fea6"  // Globally unique ID
               },

               // Aircraft Information
               "aircraftDescription": {
                  "registration": "N848AN",            // Tail number
                  "aircraftAddress": "AB9D9E",         // Mode S transponder address
                  "aircraftType": { "icaoModelIdentifier": "B789" },  // Boeing 787-9
                  "wakeTurbulence": "H",               // H=Heavy, M=Medium, L=Light
                  "tfmsSpecialAircraftQualifier": "HEAVY_JET",
                  "capabilities": {
                     "communication": {
                     "communicationCode": "E1 E3 H M1 P2 Y",      // Radio equipment
                     "dataLinkCode": "J1 J4 J5",                  // Digital comms
                     "otherDataLinkCapabilities": "1FANSER2PDC"
                     },
                     "navigation": {
                     "navigationCode": "W X G I D",               // Basic nav equipment
                     "performanceBasedCode": "A1 B1 C1 D1 L1 O1 S2 T1"  // Advanced PBN
                     },
                     "surveillance": {
                     "surveillanceCode": "L B1 D1",               // Transponder capabilities
                     "otherSurveillanceCapabilities": "260B RSP180 CANMANDATE"
                     }
                  },
                  "accuracy": {
                     "cmsFieldType": [                              // Navigation accuracy by phase
                     { "phase": "DEPARTURE", "type": "RNV", "uom": "NAUTICAL_MILES", "text": "1.0" },
                     { "phase": "ENROUTE", "type": "RNV", "uom": "NAUTICAL_MILES", "text": "2.0" },
                     { "phase": "ARRIVAL", "type": "RNV", "uom": "NAUTICAL_MILES", "text": "1.0" }
                     ]
                  }
               },

               // Flight Operations
               "departure": {
                  "departurePoint": "EGLL",                        // Origin airport
                  "runwayPositionAndTime": {
                     "runwayTime": { "actual": { "time": "2025-11-12T17:01:00Z" } }
                  }
               },
               "arrival": { "arrivalPoint": "KDFW" },             // Destination airport

               // Route Information
               "agreed": {
                  "route": {
                     "initialFlightRules": "IFR",                   // IFR, VFR, Y, Z
                     "nasRouteText": "EGLL./.OVORA..KMNGO..CMX..CMARO..SMIDD..DSM.J25.TUL..KLAWW.VKTRY2.KDFW"
                  }
               },
               "enRoute": {
                  "alternateAerodrome": [                          // Alternate airports
                     { "code": "BIKF" }, { "code": "CYYR" }
                  ],
                  "beaconCodeAssignment": { "currentBeaconCode": "2674" }  // Transponder code
               },

               // ATC Coordination
               "assignedAltitude": { "simple": { "uom": "FEET", "text": "40000.0" } },
               "requestedAirspeed": { "nasAirspeed": { "uom": "MACH", "text": "0.85" } },
               "coordination": {
                  "coordinationTime": "2025-11-12T17:37:00Z",     // Handoff timing
                  "coordinationTimeHandling": "E",                 // E=Estimated, A=Actual
                  "coordinationFix": {                             // Handoff point
                     "location": { "srsName": "urn:ogc:def:crs:EPSG::4326", "pos": "47.616667 -87.916667" }
                  }
               },

               // Status and System Information
               "flightStatus": { "fdpsFlightStatus": "ACTIVE" }, // PROPOSED, ACTIVE, DEPARTED, ARRIVED
               "flightType": "SCHEDULED",                         // SCHEDULED, GENERAL, MILITARY
               "centre": "ZMP",                                   // ARTCC identifier
               "source": "AH", "system": "SLC",                  // System identifiers
               "timestamp": "2025-11-12T17:35:41.036Z",

               // Additional Data
               "operator": { "operatingOrganization": { "organization": { "name": "AAL" } } },
               "flightPlan": {
                  "flightPlanRemarks": "|ADSB",                    // Additional remarks
                  "identifier": "KP61666400"                      // Flight plan ID
               },
               "supplementalData": {
                  "additionalFlightInformation": {
                     "nameValue": [                                 // System metadata
                     { "name": "MSG_SEQ_NO", "value": "15736993" },
                     { "name": "FDPS_GUFI", "value": "us.fdps.2025-11-12T17:07:46Z.000/15/400" },
                     { "name": "FLIGHT_PLAN_SEQ_NO", "value": "4" }
                     ]
                  }
               }
               }
            },
            "time": "2025-11-12 17:35:41.036000"                  // Record timestamp
         }

         EXAMPLE MONGODB QUERIES:

         1. Find all active flights by airline:
         [
            { $match: { "message.flight.flightStatus.fdpsFlightStatus": "ACTIVE" } },
            { $match: { "message.flight.operator.operatingOrganization.organization.name": "AAL" } },
            { $project: {
               "flight": "$message.flight.flightIdentification.aircraftIdentification",
               "aircraft": "$message.flight.aircraftDescription.aircraftType.icaoModelIdentifier",
               "route": {
                  "from": "$message.flight.departure.departurePoint",
                  "to": "$message.flight.arrival.arrivalPoint"
               }
               }
            }
         ]

         2. Analyze aircraft types and wake turbulence distribution:
         [
            { $group: {
               _id: {
                  "aircraftType": "$message.flight.aircraftDescription.aircraftType.icaoModelIdentifier",
                  "wakeTurbulence": "$message.flight.aircraftDescription.wakeTurbulence"
               },
               count: { $sum: 1 }
               }
            },
            { $sort: { count: -1 } }
         ]

         3. Find flights with specific navigation capabilities:
         [
            { $match: {
               "message.flight.aircraftDescription.capabilities.navigation.performanceBasedCode":
               { $regex: "A1" }
               }
            },
            { $project: {
               "flight": "$message.flight.flightIdentification.aircraftIdentification",
               "navCodes": "$message.flight.aircraftDescription.capabilities.navigation.performanceBasedCode",
               "route": "$message.flight.agreed.route.nasRouteText"
               }
            }
         ]

         KEY GUIDELINES:
         - Use proper nested field paths: "message.flight.flightIdentification.aircraftIdentification"
         - Handle arrays with $unwind when needed: accuracy.cmsFieldType, alternateAerodrome
         - Parse space-separated equipment codes with $regex for capability analysis
         - All timestamps are UTC format
         - Use $match early in pipelines for performance
         - Consider indexing on frequently queried fields like flightStatus, centre, departure/arrival points

         Provide clear, executable MongoDB aggregation pipelines with stage explanations and sample output descriptions.

         agent_init_function:
         module: "sam_mongodb.lifecycle"
         name: "initialize_mongo_agent"
         config:
            db_host: "${SAM_DOCUMENTDB_MONGO_HOST}"
            db_port: ${SAM_DOCUMENTDB_MONGO_PORT}
            db_user: "${SAM_DOCUMENTDB_MONGO_USER}"
            db_password: "${SAM_DOCUMENTDB_MONGO_PASSWORD}"
            db_name: "${SAM_DOCUMENTDB_MONGO_DB}"
            database_collection: "${SAM_DOCUMENTDB_FLIGHTPLAN_COLLECTION}"
            database_purpose: "${SAM_DOCUMENTDB_FLIGHTPLAN_DB_PURPOSE}"
            data_description: "${SAM_DOCUMENTDB_FLIGHTPLAN_DB_DESCRIPTION}"
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
               collection: "${SAM_DOCUMENTDB_FLIGHTPLAN_COLLECTION}"

         session_service: *default_session_service
         artifact_service: *default_artifact_service

         artifact_handling_mode: "embed"
         enable_embed_resolution: true
         enable_artifact_content_instruction: true

         agent_card:
         description: "An expert MongoDB assistant specialized in analyzing FAA Flight Data Processing System (FDPS) flight plan records, translating aviation operations questions into precise aggregation pipelines for comprehensive flight plan data including aircraft capabilities, routing, ATC coordination, and flight lifecycle management."
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
1. Update your `.env` to add the following env vars
      ```
      ## Flight Plan Collection
      SAM_DOCUMENTDB_FLIGHTPLAN_COLLECTION="FDPSFlightPlan"
      SAM_DOCUMENTDB_FLIGHTPLAN_DB_PURPOSE="this database includes information about filed flight plans"
      SAM_DOCUMENTDB_FLIGHTPLAN_DB_DESCRIPTION="Contains real-time flight plan records from the FAA's Flight Data Processing System (FDPS) with comprehensive aircraft information, routing details, equipment capabilities, ATC coordination data, and flight status tracking for both commercial and general aviation operations across the National Airspace System."
      ```
1. Save the fle and run it
   ``` 
   sam run configs/agents/flightPlan.yaml
   ```

1. Navigate back to the SAM WebUI instance and observe the new agent

## Step 3: Analyze Flight Plan Adherence

Now that you have access to both actual position data and flight plans, you can perform adherence analysis.

### Query for a Specific Flight

Replace `XXYYYY` with an actual flight number from your data (you can find flight numbers from the earlier queries), then run:

```
How well has flight XXYYYY adhered to its flight plan?
```

### Understanding the Analysis

Agent Mesh will:
1. Retrieve the flight plan for flight XXYYYY from the Flight Plan Agent
2. Retrieve actual position data from the FDPS Agent
3. Compare actual positions and times against planned waypoints and schedule
4. Calculate deviations in:
   - Route (lateral deviation from planned path)
   - Altitude (vertical deviation from planned altitude)
   - Timing (early/late compared to estimates)
5. Provide a summary of adherence quality

## Advanced Analysis Examples

Try these more complex analysis queries:

1. Route Deviation Analysis:
   ```
   Show me all flights that have deviated more than 10 nautical miles from their planned route in the last hour.
   ```

2. Timing Performance:
   ```
   Which flights are currently more than 15 minutes behind their planned schedule?
   ```

3. Altitude Compliance:
   ```
   List any flights not maintaining their assigned cruise altitude within 500 feet.
   ```

4. Fuel Efficiency:
   ```
   Compare actual vs. planned fuel burn rates for flights between JFK and LAX.
   ```

## Use Cases for Flight Plan Intelligence

With flight plan analysis capabilities, users can:
- Identify flights experiencing significant deviations
- Assess the impact of weather or airspace restrictions
- Evaluate airline operational efficiency
- Support post-flight analysis and investigations
- Optimize future flight planning based on historical adherence

This multi-agent coordination demonstrates the power of Agent Mesh to orchestrate complex analyses across multiple data sources seamlessly.

## Next Steps

In this part of this workshop, we'll explore event-based Agentic AI, where we'll configure Agent Mesh to automatically generate reports in response to real-time events.

[Continue to Event-Based Agentic AI](600-Event-Based.md)