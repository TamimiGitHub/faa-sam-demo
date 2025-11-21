# Part 4: Asking Questions in Natural Language

## Table of Contents
- [Exercise: Querying Inbound Flights](#exercise-querying-inbound-flights)
  - [Query for LAS Arrivals](#query-for-las-arrivals)
  - [Understanding the Response](#understanding-the-response)
- [Exercise: Querying Ground Operations](#exercise-querying-ground-operations)
  - [Query for Ground Traffic](#query-for-ground-traffic)
  - [Understanding the Response](#understanding-the-response-1)
- [Extracting Operational Insights](#extracting-operational-insights)
- [Advanced Queries](#advanced-queries)
- [Next Steps](#next-steps)

Now that your agents are connected and tested, you can begin querying the data using natural language. Agent Mesh will interpret your questions, determine which agent(s) to consult, construct appropriate database queries, and present the results in a user-friendly format.

## Exercise: Querying Inbound Flights

### Query for LAS Arrivals

In the Agent Mesh interface, enter the following prompt:

```
Provide me a summary of flights inbound into LAS.
```

_Note: LAS is the IATA airport code for Las Vegas Harry Reid International Airport_

### Understanding the Response

Agent Mesh will:
1. Identify that this query requires FDPS data (flight positions and routes)
2. Route the request to the FDPS Agent
3. Construct a database query to find aircraft with destination LAS
4. Filter for inbound flights (flights currently en route, not yet landed)
5. Aggregate and summarize the results
6. Present a human-readable summary

**Expected Summary Elements:**
- Number of inbound flights
- Flight identifiers and airlines
- Current positions and estimated times of arrival
- Altitude and speed information
- Origin airports

## Exercise: Querying Ground Operations

### Query for Ground Traffic

Enter the following prompt:

```
Provide me a summary of flights on the ground and taxiing in LAS.
```

### Understanding the Response

Agent Mesh will:
1. Recognize this requires STDDS data (surface movements)
2. Route the request to the STDDS Agent
3. Query for aircraft at LAS with ground/taxiing status
4. Summarize surface operations

**Expected Summary Elements:**
- Number of aircraft on the ground
- Aircraft currently taxiing vs. parked
- Taxiway and runway occupancy
- Departure vs. arrival operations
- Ground movement patterns

## Extracting Operational Insights

The natural language interface enables non-technical users to:
- Monitor airport congestion in real-time
- Identify potential bottlenecks in ground operations
- Track inbound traffic for resource planning
- Generate operational reports without writing SQL or code

Try experimenting with your own queries to explore different aspects of the data, such as specific airlines, aircraft types, or time-based patterns.

## Advanced Queries

As you become more familiar with the data, try some more complex queries:

1. Compare inbound traffic volumes between two different airports:
   ```
   Compare the number of inbound flights to LAS and SFO in the next 2 hours.
   ```

2. Analyze ground congestion across multiple airports:
   ```
   Which of the top 5 busiest US airports currently has the most aircraft taxiing?
   ```

3. Investigate potential delays:
   ```
   Are there any inbound flights to JFK that are more than 30 minutes behind their scheduled arrival time?
   ```

4. Examine airspace utilization:
   ```
   What's the average altitude of flights currently over Colorado?
   ```

Remember, the power of natural language querying lies in its flexibility. Feel free to ask questions as you would to a human expert, and Agent Mesh will work to interpret and answer them using the available data.

## Next Steps

In the next part, we'll add flight plan intelligence to our system, allowing for more sophisticated analysis such as comparing actual flight paths to planned routes.

[Continue to Part 5: Adding Flight Plan Intelligence](500-Flight-Plan.md)