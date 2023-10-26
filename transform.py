ft_call_log = '''INSERT INTO staging.ft_call_log(
                    id,
                    caller_ID,
                    agentID,
                    callDurationInSeconds)
                SELECT cl.call_id, cl.callerid, cl.agentid, cd.calldurationinseconds
                from dev_call_details cd inner join dev_call_log cl on 
                cd.callid = cl.call_id;
'''

dim_call_details = '''INSERT INTO staging.dim_call_details(
                callID,
                resolutionDurationInHours,
                callType,
                complaintTopic,
                assignedTo,
                status)
              SELECT cd.callid, cl.resolutiondurationinhours, cd.calltype, cl.complainttopic, cl.assignedto,cl.status 
              from dev_call_details cd inner join dev_call_log cl on 
              cd.callid = cl.call_id; 
'''

dim_agent = '''INSERT INTO staging.dim_agent(
               agentID,
               agentsGradeLevel)
               SELECT cl.agentID, cd.agentsgradelevel
               from dev_call_details cd inner join dev_call_log cl on 
               cd.callid = cl.call_id;
'''

agg_KPI1 = '''INSERT INTO staging.agg_KPI1(
              agentID,
              noOfResolvedCalls,
              noOfCallsReceived)
              SELECT agentid, 
              count(CASE 
	            WHEN status = 'resolved' THEN 1 else null end) as totalResolvedCalls,
              count(status) as TotalCallsReceived 
              from dev_call_log
              group by agentid
              order by totalResolvedCalls;
'''

agg_KPI2 = '''INSERT INTO staging.agg_KPI2(
              agentID,
              noOfCallsReceived,
              callsAssignedOrResolved)
              SELECT agentid, count(*) as totalcallsreceived, 
              count(CASE WHEN status = 'resolved' or agentID = assignedTo THEN 1 else null end) as resolvedorassigned
              from dev_call_log
              group by agentid
              order by totalcallsreceived;
'''

agg_KPI3 = '''INSERT INTO staging.agg_KPI3(
              agentID,
              agentsGradeLevel,
              totalCallDuration,
              avgCallDuration)
              SELECT agentid, agentsGradeLevel, SUM(callDurationInseconds) as TotalCallDuration, avg(callDurationInseconds) as AverageCallDuration
              from dev_call_details cd inner join dev_call_log cl on cd.callid = cl.call_id
              group by agentid, agentsGradeLevel;
'''

agg_KPI4 = '''INSERT INTO staging.agg_KPI4(
              agentID,
              agentsGradeLevel,
              earliestClosedCall,
              latestClosedCall)
              select agentID, agentsGradeLevel, min(callDurationInSeconds), max(callDurationInSeconds)
              from dev_call_details inner join dev_call_log on 
              dev_call_details.callid = dev_call_log.call_id
              where status = 'closed'
              group by agentID, agentsGradeLevel;

'''
transformed_tables = [ft_call_log, dim_call_details, dim_agent, agg_KPI1, agg_KPI2, agg_KPI3, agg_KPI4]
 
transformation_queries = [ft_call_log, dim_call_details, dim_agent, agg_KPI1, agg_KPI2, agg_KPI3, agg_KPI4]