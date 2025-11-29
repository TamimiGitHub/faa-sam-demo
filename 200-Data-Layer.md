# Setting Up the Data Layer

## Table of Contents
- [Understanding Your Workshop Environment](#understanding-your-workshop-environment)
- [Collection Overview](#collection-overview)
  - [FDPSPosition Collection](#fdpsposition-collection)
  - [STDDSPosition Collection](#stddsposition-collection)
- [Data Ingestion Architecture](#data-ingestion-architecture)
- [Understanding the Data Flow](#understanding-the-data-flow)
- [Next Steps](#next-steps)


## Understanding Your Workshop Environment

Your workshop environment includes a pre-configured DocumentDB instance that serves as the data layer for this exercise. This instance contains the primary collections that store real-time flight data.

## Collection Overview

### FDPSPosition Collection

This collection contains position reports and flight plan data from the FDPS system, including:
- Aircraft identification
- Current position (latitude, longitude, altitude)
- Flight plan information
- Route adherence data
- Timestamps and status indicators

### STDDSPosition Collection

This collection contains surface movement data from the STDDS system, including:
- Aircraft identification
- Ground position coordinates
- Taxiway and runway assignments
- Ground speed and heading
- Surface movement status

## Data Ingestion Architecture

The collections are continuously populated by a micro-integration that:

1. **Subscribe to Solace Event Mesh**: Each micro-integration subscribes to specific topic patterns for FDPS or STDDS data
2. **Receive real-time events**: As flight data is published, the micro-integrations receive relevant messages
3. **Transform and validate**: Data is validated and transformed as needed for database storage
4. **Write to DocumentDB**: Processed messages are written to the appropriate collection
5. **Maintain rolling window**: Old data is automatically purged to maintain the 10-minute historical window

_These micro-integrations are already running in your environment, continuously populating the database with live FAA data._

## Understanding the Data Flow

1. **Event Publication**: FAA systems publish flight data to the Solace Event Mesh
2. **Event Subscription**: Micro-integrations subscribe to relevant topics
3. **Data Processing**: Events are transformed and validated
4. **Database Write**: Processed data is written to DocumentDB collections
5. **Data Expiration**: Old data is automatically removed to maintain the historical window

This architecture ensures that your DocumentDB instance always contains the most recent 8 hours of flight data, providing a real-time view of the National Airspace System.

## Next Steps

In the next part, we'll create DocumentDB agents in Agent Mesh to interact with this data layer. These agents will allow us to query and analyze the real-time flight data using natural language.

[Continue to Creating DocumentDB Agents in Agent Mesh](300-DocumentDB-Agents.md)