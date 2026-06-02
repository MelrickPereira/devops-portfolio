What is Observability?
    - if you have observabilty setup you can get the internal state of the system
    - System here are the application(is it working as expected? or are there any failures), Infra () and Network(latency,)

Examples:
    What is the Disk usage of a Node - whether it is constantly 100% utilized or is it under-utilized like 20%
    What is the CPU utilization of a Node
    What is the Memory Utilization
    out of 1000 http req --> how many failed or successeded

 Though Observability we can understand what has failed and why, the reason for failure and also understand how we can fix the issue

Pilers of Observabillit--> 
1. Matrices - responsible to understand what is the state of the system
2. Logging  - responsible to understand why is the system in that perticular state
3. Traces   - can help to fix the particular state

if all these things are setup, You have basically setup Observability

Real life example:

- say http call to an application is failing 
Matrices:  
you can check matrices and see that in the last 30 min 10 http req failed - and in the last 24h 100 req has failed, you can  get the historical data using matrices

Logging:  
using the matrices you can identify the timestamp of the failed req, you can go to the logs of that particular application 
and see who has sent the req and check which part of the application the req hit and why is that http req failing

Traces:
helps to trace the http request
client --> load balancer(LB) --> frontend(F) -->  backend(B) -->  database(DB)

it has the traces of whether 
- the request went to the LB
- did the reqest go the the frontend and if it did how long did it take 
- similarly did it do to the backend
- did it go to the correct backend

* this helps to identify where the issue is and fix it


Monitoring Vs Observibility

- Monitoring is basicaly matices with alerts setup and has a dashboard implemented (Grafana)
- where as Observibility includes the three pillars - Matrices, Logs, Traces
- Monitoring is a sub part of Observibility

