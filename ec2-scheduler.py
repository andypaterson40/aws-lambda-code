import boto3
from datetime import datetime

ec2 = boto3.client('ec2')

instances = ec2.describe_instances()

startList = []
stopList = []

runningStateList = []
stoppedStateList = []

stopTime = '12:00:00'
startTime = '12:30:00'

curr_day = datetime.today().strftime("%a").lower()
curr_time = str(datetime.now().time())
print curr_day
print curr_time


# def lambda_handler(event, context):
for instance in instances['Reservations']:
    for i in instance['Instances']:
        instance_id = i['InstanceId']
        instance_state = i['State']['Name']

        if curr_day == 'fri':
            if curr_time >= stopTime and stopTime <= curr_time and instance_state == 'running':
                stopList.append(instance_id)
                print instance_id + ' added to stop list'

        # if curr_day == 'fri':
            if curr_time >= startTime and startTime <= curr_time and instance_state == 'stopped':
                startList.append(instance_id)
                print instance_id + ' added to start list'

if startList:
    print 'Starting ', len(startList), ' instances', startList
    ec2.start_instances(InstanceIds=startList)
else:
    print 'No instances to start'

if stopList:
    print 'Stopping ', len(stopList), ' instances', stopList
    ec2.stop_instances(InstanceIds=stopList)

