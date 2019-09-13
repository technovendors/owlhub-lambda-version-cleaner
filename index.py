import json
import boto3

client = boto3.client('lambda')


def clean_old_lambda_versions(marker=''):
    # list all function with page
    if marker == '':
        functions = client.list_functions()
    else:
        functions = client.list_functions(Marker=marker)

    # Loop through all function to get all of version
    for function in functions['Functions']:
        while True:
            # get versions of a lambda function
            versions = client.list_versions_by_function(FunctionName=function['FunctionArn'])['Versions']
            # remove last 5 versions form array to hold 5 versions as backup
            versions = versions[:-5]

            # keep only latest version
            if len(versions) < 2:
                print('{}: done'.format(function['FunctionName']))
                break

            for version in versions:
                # remove all versions execpt the latest one
                if version['Version'] != function['Version']:
                    arn = version['FunctionArn']
                    print('delete_function(FunctionName={})'.format(arn))
                    # Delete function
                    client.delete_function(FunctionName=arn)

    # Paginate for other lambda functions
    if 'NextMarker' in functions:
        clean_old_lambda_versions(functions['NextMarker']);


def handler(event, context):
    clean_old_lambda_versions();

    return {
        'statusCode': 200,
        'body': json.dumps('old lambda versions get cleaned!')
    }
