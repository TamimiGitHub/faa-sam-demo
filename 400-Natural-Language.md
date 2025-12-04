# Asking Questions in Natural Language

## Table of Contents
- [Overview](#overview)
- [Using Stored Prompts](#using-stored-prompts)
- [Available Prompts for Las Vegas (KLAS)](#available-prompts-for-las-vegas-klas)
  - [Planes on the Ground](#planes-on-the-ground)
  - [Schedule Compliance Check](#schedule-compliance-check)
  - [Flight Details from STDDS](#flight-details-from-stdds)
  - [Flight Details from FDPS](#flight-details-from-fdps)
  - [Comprehensive Flight Report](#comprehensive-flight-report)
  - [Updated Comprehensive Flight Report](#updated-comprehensive-flight-report)
- [Extracting Operational Insights](#extracting-operational-insights)
- [Next Steps](#next-steps)

## Overview

Now that your agents are connected and tested, you can begin querying the data using natural language. Agent Mesh will interpret your questions, determine which agent(s) to consult, construct appropriate database queries, and present the results in a user-friendly format.

In this section, we will perform **natural language analysis** on two key data types:
- **Surface-level operations** - Analyzing aircraft movements on the ground, taxiing, and ground operations at the airport
- **In-flight real-time data** - Monitoring aircraft in flight, including positions, altitudes, speeds, and flight status

> Note: For this workshop, we will be working exclusively with **Las Vegas Harry Reid International Airport (KLAS)**.

## Using Stored Prompts

If you recall earlier, we imported a list of prompts. You can access these prompts by typing a slash followed by the prompt number and name in the chat interface. For example, typing `/401 - Planes on the ground` will load the "Planes on the Ground" prompt. Note that some prompts have variables that you will need to input before sending in the prompt. 

Each stored prompt is designed for specific analytical tasks and will automatically populate the chat with the appropriate query.

Lets go ahead and choose a flight for our analysis

![flightradar](./img/flight_radar.png)

> Note: start from `/403` for time constraints

## Available Prompts for Las Vegas (KLAS)

The following prompts are available for analyzing operations at Las Vegas airport (KLAS):

### Planes on the Ground

**Description:** Provides a report of planes that are on the ground taxiing at KLAS.

**Usage:** Type `/401 - Planes on the ground` in the chat prompt

### Schedule Compliance Check

**Description:** Find flights behind estimated arrival times at KLAS.

**Usage:** Type `/402 - Schedule Compliance Check` in the chat prompt


### Flight Details from STDDS

**Description:** STDDS Flight Details for a specific flight at KLAS.

**Usage:** Type `/403 - Flight Details from STDDS` in the chat prompt, then provide the flight number when prompted


### Flight Details from FDPS

**Description:** FDPS Flight Details for a specific flight, including historical data.

**Usage:** Type `/404 - Flight Details from FDPS` in the chat prompt, then provide the flight number when prompted


### Comprehensive Flight Report

**Description:** Generate a combined report from both STDDS and FDPS for a specific flight.

**Usage:** Type `/405 - Comprehensive Flight Report` in the chat prompt, then provide the flight number when prompted


### Updated Comprehensive Flight Report

**Description:** Provide an updated report including all new and historical data from both STDDS and FDPS.

**Usage:** Type `/406 - Updated Comprehensive Flight Report` in the chat prompt, then provide the flight number when prompted

## Extracting Operational Insights

The natural language interface with stored prompts enables non-technical users to:
- Monitor airport congestion in real-time at KLAS
- Identify potential bottlenecks in ground operations
- Track flight status and delays efficiently
- Generate operational reports without writing SQL or code
- Access standardized queries for consistent analysis

By using the stored prompts (e.g., `/401 - Planes on the ground`, `/402 - Schedule Compliance Check`), you ensure consistent query formatting and can quickly access common analytical tasks for Las Vegas airport operations.

## Next Steps

In the next part, we'll add flight plan intelligence to our system, allowing for more sophisticated analysis such as comparing actual flight paths to planned routes.

[Continue to Adding Flight Plan Intelligence](500-Flight-Plan.md)