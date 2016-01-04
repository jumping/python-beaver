# -*- coding: utf-8 -*-
import boto
import cloudinit.ec2_utils

def pure_value(values):
    ret = []
    if isinstance(values, str):
        values = [values]

    for value in values:
        value = value.replace(' ', '')
        value = value.replace('- ', '')
        value = value.replace('_', '')
        ret.append(value)

    return ret    

def instance_tag(instance_id):
    try:
        conn = boto.connect_ec2()
        tags = conn.get_all_instances([instance_id])[0].instances[0].tags
    
        if tags and isinstance(tags, dict):
            tag_value = tags.values()
            return tag_value
    except:    
        pass

def metadata():
    #get data from the 169.254.169.254/latest/meta-data
    metadata = cloudinit.ec2_utils.get_instance_metadata()
    services = metadata.get('services','')
    if services and services.get('domain','') != 'amazonaws.com':
        return

    ret = []
    avaliable_zone = metadata.get('placement','')
    if avaliable_zone:
        zone = avaliable_zone.get('availability-zone')
        ret.append(zone)
    
    instance_id = metadata.get('instance-id')
    security_groups = metadata.get('security-groups')
    if isinstance(security_groups, str):
        security_groups = [security_groups]
    ret.extend(security_groups)    

    #get all values of instance tags
    instance_tag_values = instance_tag(instance_id)
    if instance_tag_values:
        ret.extend(instance_tag_values)

    return pure_value(ret)

