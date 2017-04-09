#! /usr/bin/env python

import boto, boto.ec2, datetime

# EC2, AMI 권한 있는 Key, Secret Key 입력
ACCESS_KEY = 'insert_key_here'
SECRET_KEY = 'insert_secret_key_here'

# 백업할 Region 을 List 로 입력
regions = ['us-west-1']

def create_image(region_name):

    ec2_conn = boto.ec2.connect_to_region(region_name, aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY)
    ec2_instances = [i for r in ec2_conn.get_all_instances() for i in r.instances]

    today = datetime.date.today()
    today_str = today.strftime("%y%m%d")

    for ec2 in ec2_instances:
        id = ec2.id
        name = ec2.tags.get('Name')

        # AMI 이름 포맷 : EC2이름-Backup-yyyMMdd
        ec2_conn.create_image(id, name + '-Backup-' + today_str, 'Automatic Backup by Cron', True)


for region in regions:
    create_image(region)
