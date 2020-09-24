import argparse
import boto3

parser = argparse.ArgumentParser(description='provide the check value')
parser.add_argument('value', type=str,help='a string')
args = parser.parse_args()
check = args.value

aws_con=boto3.session.Session(profile_name="akkatir")
ec2_con=aws_con.client(service_name="ec2",region_name="us-east-1")

if check == "start":
  response=ec2_con.describe_instance_status(InstanceIds=["i-0745c0f2ff471a6c5","i-07eccd8e8299f91b8","i-0d73e96965fafd7c9"],IncludeAllInstances=True)
  for each in response['InstanceStatuses']:
      value=each['InstanceState']['Name']
      if value=='running':
         print("Already running " + each['InstanceId'] )
      elif value == 'stopped':
           ec2_stop = ec2_con.start_instances(InstanceIds=[each['InstanceId']])
           print('starting the instance ' + each['InstanceId'])
      elif value == 'pending':
           print('pending in progress ' + each['InstanceId'])
      else:
           print('unknown status')         
                                 
            
elif check == "stop":
   response=ec2_con.describe_instance_status(InstanceIds=["i-0745c0f2ff471a6c5","i-07eccd8e8299f91b8","i-0d73e96965fafd7c9"],IncludeAllInstances=True)
   for each in response['InstanceStatuses']:
       value=each['InstanceState']['Name']
       if value=='stopped':
          print("Already stopped " + each['InstanceId'] )
       elif value == 'stopping':
            print("Stopping in progress " + each['InstanceId'])
       elif value == 'running':
            ec2_stop = ec2_con.stop_instances(InstanceIds=[each['InstanceId']])
            print('stopping the instance ' + each['InstanceId'])
       elif value == 'pending':
            print('can not stop. pending in progress')
       else:
            print('unknown status')
else:
  print("wrong check value")
