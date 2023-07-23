import json
import boto3
from flask import Flask, request
import datetime
from typing import List
from handler import datetime_converter
from aws_configurations import AWS_SESSION_TOKEN, AWS_SECRET_ACCESS_KEY, AWS_ACCESS_KEY_ID

app = Flask(__name__)

def get_aws_regions_list() -> List:
    """
    This function return a list of regions in AWS, accroding to regions.txt file.

    :rtype: object
    """
    with open("regions.txt", "r") as f:
        return [x.replace(",", "") for x in f.readline().split()]

def create_region_instances_json_file(region: str, instances: List) -> None:
    """
    This function gets an AWS region string and a list of instances, and creates a json file for them.
    :param region:
    :param instances:
    :return:
    """
    for x in instances:
        x.update({"days_from_launching" : abs(datetime.date.today() - x["date"]).days})
        x["date"] = datetime_converter(x["date"])
    instances = sorted(instances, key=lambda x: x["date"])
    with open(f"{region}.json", "w", encoding='utf-8') as file:
        json.dump(instances, file, ensure_ascii=False, indent=4)

def create_region_files() -> None:
    """
    This function gets instances from AWS for each region in the list, and triggers the function
    create_region_instances_json_file
    :return:
    """
    regions = get_aws_regions_list()
    for region in regions:
        ec2 = boto3.resource('ec2',
                             aws_access_key_id=AWS_ACCESS_KEY_ID,
                             aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                             aws_session_token=AWS_SESSION_TOKEN,
                             region_name=region)

        instances_for_region = []
        for f in ec2.instances.all():
            instances_for_region.append({"id": f.id, "date": f.launch_time})
        create_region_instances_json_file(region, instances_for_region)

def make_response(status, success=False, message=None, **kwargs):
    response = {"success": success, "message":message}
    for key, value in kwargs.items():
        response.update({key: value})
    return response, status

@app.route("/", methods=['GET'])
def endpoint():
    """
    The is the endpoint function, Implemented with Flask.
    For example: http://127.0.0.1:5000/?region=us-east-1
    :rtype: object
    """
    region = request.args.get("region")
    if region is None: # Hint the user in case the argument is empty.
        return make_response(400, message=f"Please specify the AWS region. example: {request.base_url}?region"
                                          f"=<aws_region>")
    if region not in get_aws_regions_list(): # Validate the region name.
        return make_response(400, message=f"Un-recognized region {region}")
    try:
        file = open("{}.json".format(region), "r")
    except FileNotFoundError: # The file was not found, trying to generate it
        try:
            create_region_files()
        except Exception as e: # Probably couldn't access AWS for AccessDenied or RequestExpired
            return make_response(400,
                                 message="Couldn't generate the instances data from AWS. Please check your AWS "
                                         "credentials", exception_message=str(e))

    file = open("{}.json".format(region), "r")
    response = make_response(200, success=True, message=f"Instances for {region} are attached", data=json.load(file))
    file.close()
    return response


if __name__ == "__main__":
    app.run()
