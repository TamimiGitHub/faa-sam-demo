# Workshop: Agentic AI with Realtime FAA Data

## Table of Contents

1. [Overview](#overview)
   - [The Mission](#the-mission)
   - [The Challenge](#the-challenge)
   - [Your Task: "Chat with your Data"](#your-task-chat-with-your-data)
   - [The Technical Landscape](#the-technical-landscape)
   - [Topic Structure](#topic-structure)
2. [Prerequisites](#prerequisites)
3. [Prepare AWS Environment](#prepare-aws-environment)
4. [Workshop Structure](#workshop-structure)
5. [Getting Started](#getting-started)
6. [Support](#support)
7. [Additional Resources](#additional-resources)
8. [Note on AWS Environment Setup](#note-on-aws-environment-setup)
   - [Running it on your own](#running-it-on-your-own)

## Workshop: Agentic AI with Realtime FAA Data

## Overview

Hi there! Welcome to our AWS Re:Invent 2025 workshop 👋 In this hands-on workshop, you will explore how to use Solace Agent Mesh and AWS resources to analyze real-time FAA (Federal Aviation Administration) flight data streams. This workshop demonstrates how to transform complex aviation data into actionable insights using AI-powered agents and natural language queries.

### 🎯 The Mission
Imagine you're part of an elite team of FAA engineers tasked with revolutionizing how aviation professionals interact with flight data. Your mission? To harness the power of AI and transform the way flight planners, operators, and controllers access critical information.

### 🤔 The Challenge
Every day, aviation professionals face a common hurdle: while they're experts in their domain, navigating the FAA's vast ocean of data sources can be overwhelming. They know what they need, but finding it in the complex web of aviation data? That's where things get turbulent.

### 🌟 Your Task: "Chat with your Data"
You'll build an intelligent system that lets aviation professionals simply ask questions in plain English and get instant, accurate answers from real-time flight data. No more digging through complex databases or decoding technical data structures!

### 🌐 The Technical Landscape
- The FAA's real-time flight information flows through a sophisticated publish/subscribe messaging system, powered by the Solace Event Mesh
- This system lets users tap into exactly the data streams they need, creating an efficient, dynamic flow of information
- To make this data AI-ready, we're capturing a 10-minute historical window in DocumentDB (Don't worry, we've already set this up in your workshop environment!)

### Topic Structure
The FAA stream is being published on the following topic hierarchy

```
FDPS/position/{FLIGHT_ID}/{STATUS}/{CALLSIGN}/{ORIGIN}/{DESTINATION}/{LATITUDE}/{LONGITUDE}/{GROUND_SPEED}/{ALTITUDE}/{HEADING}
```
And
```
STDDS/position/{AIRPORT_CODE}/{FLIGHT_ID}
```

By the end of this workshop, you will have built a multi-agent system that can:
- Interact with real-time flight data from multiple FAA systems
- Analyze flight plan adherence
- Generate automated landing reports
- Provide operational insights to flight planners, operators, and controllers

You will use:
- AWS resources: EC2 Instances, DocumentDB, Bedrock LLM, AgentCore
- Agentic Frameworks: MCP, A2A, Strands, Solace Agent Mesh
- Solace Platform: Event Broker

Ready for takeoff? Let's transform how aviation professionals interact with their data! ✈️

## Prerequisites

- Command-line knowledge
- Python 3.10+
- AWS account. If you are attending this event in person, the necessary plumbing is already configured for you
- Your curiosity!

## Prepare AWS Environment
To setup your AWS Environment, please follow the steps in the [Environment Setup](010-Env-Setup.md) document

## Workshop Structure

This workshop is divided into the following  parts:

1. [Standard Operating Procedures](100-SOPs.md) - Understanding FDPS, STDDS, and RAG
1. [Data Layer](200-Data-Layer.md) - Setting up the data infrastructure
1. [DocumentDB Agents](300-DocumentDB-Agents.md) - Creating database agents
1. [Natural Language Queries](400-Natural-Language.md) - Querying data using natural language
1. [Flight Plan Intelligence](500-Flight-Plan.md) - Adding flight plan analysis
1. [Event-Based AI](600-Event-Based.md) - Implementing event-triggered reporting

## Getting Started

Follow the workshop parts in order, starting with [Part 1: Standard Operating Procedures](100-SOPs.md)

## Support

If you need assistance during the workshop:
- Raise your hand for in-person support
- Post questions [Solace Agent Mesh forum](https://community.solace.com/c/solace-agent-mesh/16)

## Additional Resources

- ⭐️ [Solace Agent Mesh Github Repo](https://github.com/SolaceLabs/solace-agent-mesh)
- [Solace Agent Mesh Product](https://solace.com/products/agent-mesh/)
- [Event-Driven Architecture Patterns](https://solace.com/)
- [AWS Agent Core](https://aws.amazon.com/bedrock/agentcore/)

## Note on AWS Environment Setup

This workshop requires several AWS resources that are provisioned through CloudFormation templates found in the `cloudformations` directory. The template sets up:

1. **EC2 Instances**:
   - Software Solace broker for event streaming
   - VSCode editor for development

2. **DocumentDB**:
   - Database for storing flight data
   - Collections for FDPS, STDDS, and flight plans

3. **AWS Secrets Manager**:
   - Stores credentials and connection strings
   - Manages access to various services

4. **Elastic Beanstalk Applications**:
   - Subscribes to data streams
   - Processes and stores incoming data

### Running it on your own

1. Clone this repository:

2. Deploy the AWS resources:
Upload and deploy the cloud formations using the AWS Console UI