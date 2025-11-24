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

### Configure the Agent

Following the same process used in Part 3, create a new DocumentDB agent:

1. In the Agent Mesh interface, navigate to "Add New Agent"
2. Select "DocumentDB Agent" as the agent type
3. Configure with these settings:
   - Name: Flight Plan Agent
   - Collection: FlightPlans
   - Connection String: (Use the same DocumentDB connection string)
   - Database Name: FAA_Data

4. Save and verify the connection is successful

## Step 2: Test Flight Plan Access

Run a test query to verify access to flight plan data:

```
Get me an example flight plan document from the database.
```

Review the returned document to understand the structure of flight plan data, including:
- Route waypoints and timing
- Aircraft performance parameters
- Fuel planning data
- Alternate airport information
- Weather considerations

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

In the final part of this workshop, we'll explore event-based Agentic AI, where we'll configure Agent Mesh to automatically generate reports in response to real-time events.

[Continue to Part 6: Event-Based Agentic AI](600-Event-Based.md)