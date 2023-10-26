# =============================================== FOR DEV SCHEMA
dev_call_log = '''CREATE TABLE IF NOT EXISTS dev.dev_call_log
(
    call_id int,
    callerid varchar,
    agent_ID int,
    complaintTopic varchar,
    assignedTo int,
    status varchar,
    resolutionDurationInHours int
);'''

dev_call_details = '''CREATE TABLE IF NOT EXISTS dev.dev_call_details
(
    call_ID int,
    callDurationInSeconds int,
    agentsGradeLevel varchar,
    call_Type varchar,
    callEndedByAgent bool default True
);'''


# =============================================== FOR STAR SCHEMA
ft_call_log = '''
CREATE TABLE IF NOT EXISTS staging.ft_call_log(
    id BIGINT IDENTITY(1, 1),
    caller_ID INT, 
    agentID INT, 
    callDurationInSeconds NUMERIC(3, 2)
);
'''

dim_call_details = '''
    CREATE TABLE IF NOT EXISTS staging.dim_call_details(
        callID IDENTITY(1, 1),
        resolutionDurationInHours NUMERIC(3, 2), 
        callType TEXT, 
        complaintTopic VARCHAR(100),
        assignedTo integer,
        status VARCHAR(100)
    );
'''

dim_agent = '''
    CREATE TABLE IF NOT EXISTS staging.dim_agent (
        agentID integer,
        agentsGradeLevel VARCHAR
    );
'''

agg_KPI1 = '''
CREATE TABLE IF NOT EXISTS staging.agg_KPI1 (
    agentID integer,
    noOfResolvedCalls integer,
    noOfCallsReceived integer
);
'''

agg_KPI2 = '''
CREATE TABLE IF NOT EXISTS staging.agg_KPI2
(
    agentID integer, 
    noOfCallsReceived integer,
    callsAssignedOrResolved integer
);
'''

agg_KPI3 = '''
CREATE TABLE IF NOT EXISTS staging.agg_KPI3
(
    agentID integer, 
    agentsGradeLevel VARCHAR,
    totalCallDuration integer,
    avgCallDuration NUMERIC (3, 2)
);
'''

agg_KPI4 = '''
CREATE TABLE IF NOT EXISTS staging.agg_KPI4
(
    agentID integer, 
    agentsGradeLevel VARCHAR,
    earliestClosedCall integer,
    latestClosedCall integer
);
'''

dev_tables = [dev_call_log, dev_call_details]
transformed_tables= [ft_call_log, dim_call_details, dim_agent, agg_KPI1, agg_KPI2, agg_KPI3, agg_KPI4]