# Event-Based Agentic AI

So far, you've been querying data on-demand. In this section, you'll configure Agent Mesh to automatically generate reports in response to real-time events—specifically, when flights land.

## Understanding Event-Driven Agentic AI

The FAA's FDPS system publishes status updates for every flight. When a flight lands, its status changes to `DROPPED`. By subscribing to these events, you can trigger automated workflows without manual intervention.

## The Event Gateway

The Agent Mesh Event Gateway is a component that:
- Subscribes to topics on the Solace Event Mesh
- Receives events matching subscription patterns
- Triggers configured agents or workflows when events arrive
- Can publish results back to the event mesh

## Step 1: Configure the Event Gateway

### Topic Subscription
```
faa/fdps/status/DROPPED/>
```

_This topic pattern subscribes to all FDPS status messages where the status is DROPPED_

### Event Filter Configuration

1. Navigate to the Event Gateway configuration in Agent Mesh
2. Add a new subscription with the following settings:
   - Topic Pattern: `faa/fdps/status/DROPPED/>`
   - Message Type: JSON
   - Queue Name: landing_reports
   - Durable: true

## Step 2: Create the Landing Report Workflow

### Define the Workflow

When a DROPPED event is received, the Event Gateway should:

1. **Extract flight information** from the event payload (flight number, timestamp, airport)
2. **Starts Stimulus to Agent Mesh** and the orchestrator agent receives the prompt
3. **Invoke the FDPS Agent** to retrieve the full flight history
4. **Invoke the Flight Plan Agent** to retrieve the original flight plan
5. **Generate a landing report** that includes:
   - Flight identification and basic details
   - Actual vs. planned landing time
   - Route adherence summary
   - Flight duration and performance metrics
   - Any notable deviations or events
6. **Publish the report** back to the event mesh for consumption by other systems

### Configure Report Generation

1. Create a new workflow in Agent Mesh:
   ```yaml
   name: landing_report_workflow
   trigger:
     type: event
     topic: faa/fdps/status/DROPPED/>
   actions:
     - name: generate_report
       type: agent_chain
       agents:
         - fdps_agent
         - flight_plan_agent
       template: |
         Generate a landing report for flight {flight_id} that landed at {airport} at {timestamp}.
         Include route adherence, timing performance, and any significant events.
   output:
     topic: faa/reports/landings/{flight_id}
     format: json
   ```

2. Save and activate the workflow

## Step 3: Test the Automated Reporting

To test the event-driven reporting:

1. Use the Agent Mesh interface to simulate a DROPPED event:
   ```json
   {
     "flight_id": "UA1234",
     "status": "DROPPED",
     "timestamp": "2025-11-19T14:30:00Z",
     "airport": "SFO"
   }
   ```

2. Monitor the output topic `faa/reports/landings/UA1234` for the generated report

3. Review the generated report to ensure it contains:
   - Flight identification
   - Landing timestamp and airport
   - Planned vs. actual landing time comparison
   - Route adherence summary
   - Performance metrics
   - Any anomalies or noteworthy events

## Benefits of Event-Driven Reporting

This automated approach provides:
- **Immediate insights**: Reports generated within seconds of landing
- **Consistency**: Every landing produces a standardized report
- **Scalability**: Handles hundreds of landings per hour without manual effort
- **Integration**: Reports available on the event mesh for any consuming system
- **Reduced workload**: Eliminates manual report creation and distribution

## Final Takeaways

### What You've Accomplished

Congratulations! In this workshop, you have:

1. **Utilized Agent Mesh for real-time FAA data analysis**: You've connected to live aviation data streams and extracted meaningful insights using natural language queries

2. **Built a multi-agent architecture**: You created specialized DocumentDB agents for FDPS, STDDS, and flight plan data, demonstrating how Agent Mesh orchestrates multiple data sources

3. **Integrated RAG-based summarization**: You used RAG to analyze technical documentation, extracting relevant information without reading hundreds of pages

4. **Automated event-driven reporting**: You configured the Event Gateway to trigger agentic stimuli automatically in response to real-time events, demonstrating the power of event-driven Agentic AI

### Key Concepts Reviewed

#### Agent-Based Architecture
You've seen how individual agents, each with a specific purpose and data source, can be combined to answer complex questions that span multiple systems.

#### Natural Language Data Access
Non-technical users can now access FAA data without knowing database schemas, query languages, or system architectures—democratizing data access across the organization.

#### Event-Driven AI
By connecting AI agents to real-time event streams, you've created a system that proactively generates insights rather than waiting for users to ask questions.

#### The Power of Integration
Solace Agent Mesh bridges AI capabilities with enterprise event-driven architecture, creating intelligent, responsive systems that enhance decision-making.

### Next Steps

To continue your Agent Mesh journey:

1. **Explore additional agent types**: Experiment with REST API agents, SQL database agents, or custom agents for your specific systems

2. **Build more complex workflows**: Create multi-step workflows that chain together multiple agents and decision points

3. **Integrate with your systems**: Connect Agent Mesh to your organization's actual data sources and event streams

4. **Train your team**: Share what you've learned and identify use cases within your organization

5. **Join the community**: Connect with other Agent Mesh users to share patterns, solutions, and best practices

Thank you for participating in this workshop on using Solace Agent Mesh with real-time FAA data!