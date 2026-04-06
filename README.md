# Sustainable Energy-Aware Cloud Scheduling Environment

## Overview

This project implements a real-world reinforcement learning environment for energy-aware cloud workload scheduling. It simulates how an AI agent schedules compute jobs across multiple regions powered by different energy sources such as solar, wind, and coal.

The objective is to enable intelligent scheduling decisions that balance environmental sustainability, cost efficiency, and job completion deadlines.

---

## Motivation

Modern cloud computing systems consume large amounts of energy, often relying on carbon-intensive sources. Existing scheduling systems focus primarily on performance and cost, neglecting environmental impact.

This environment addresses that gap by enabling agents to:

* Reduce carbon emissions
* Optimize energy costs
* Respect renewable energy constraints
* Meet job deadlines efficiently

This makes it useful for training and evaluating AI systems for sustainable computing.

---

## Environment Description

The environment consists of:

### Regions

* Multiple data center regions (e.g., us-east, eu-west, asia-south)
* Each region has compute capacity and an energy mix

### Energy Sources

Each energy source includes:

* Carbon intensity
* Cost
* Availability

Examples:

* Solar (low carbon, variable)
* Wind (moderate variability)
* Coal (high carbon, stable)

### Jobs

Each job includes:

* Compute requirement
* Deadline
* Assignment status

---

## Observation Space

The agent observes the full system state:

```json
{
  "time": int,
  "jobs": [...],
  "regions": [...],
  "energy_sources": {...}
}
```

---

## Action Space

The agent performs scheduling actions:

```json
{
  "job_id": int,
  "region": string,
  "action_type": "assign"
}
```

---

## Reward Function

The reward function is multi-objective:

* Lower carbon emissions → higher reward
* Lower energy cost → higher reward
* Meeting deadlines → positive reward
* Missing deadlines → penalty

Conceptually:

Reward =
0.5 × Carbon Efficiency

* 0.3 × Cost Efficiency
* 0.2 × Deadline Satisfaction

---

## Tasks

### Easy Task

* Objective: Assign all jobs
* Difficulty: Low
* Evaluation: Completion rate

### Medium Task

* Objective: Assign all jobs before deadlines
* Difficulty: Moderate
* Evaluation: Completion + deadlines

### Hard Task

* Objective: Optimize carbon emissions while meeting deadlines
* Difficulty: High
* Evaluation: Multi-objective optimization

---

## Baseline Scores

Using the provided baseline agent:

* Easy: 1.0
* Medium: 1.0
* Hard: 0.81

These scores demonstrate increasing difficulty and realistic constraints.

---

## Setup Instructions

### Install dependencies

```bash
pip3 install pydantic fastapi uvicorn openenv-core openai
```

---

### Run inference

```bash
python3 inference.py
```

---

### Run API server

```bash
python3 -m server.app
```

---

### Test endpoints

* Reset: http://localhost:8000/reset
* Step: POST /step

---

## Docker Usage

```bash
docker build -t green-env .
docker run -p 8000:8000 green-env
```

---

## Usage

* The agent observes the system state
* Selects actions to assign jobs to regions
* Receives reward based on sustainability and efficiency
* Continues until all jobs are completed or time limit is reached

---

## OpenEnv Compliance

* Implements step(), reset(), state()
* Uses typed models (Pydantic)
* Includes openenv.yaml
* Passes openenv validation
* Includes baseline inference script

---

## Conclusion

This project provides a realistic simulation platform for evaluating AI agents in sustainable cloud scheduling. It enables experimentation with multi-objective optimization involving environmental impact, cost, and performance.

---

## Author

Sanjai
