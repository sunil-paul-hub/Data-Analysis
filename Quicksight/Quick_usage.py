import boto3

# Initialize the QuickSight client
quicksight_client = boto3.client('quicksight')

# Your AWS account ID
aws_account_id = 'XXXX'


# Function to list all users and their emails and roles
def list_users():
    users_info = {}

    try:
        response = quicksight_client.list_users(
            AwsAccountId=aws_account_id,
            Namespace='default'  # Or use your QuickSight namespace
        )

        for user in response.get('UserList', []):
            users_info[user['Arn']] = {
                'Email': user['Email'],
                'Role': user['Role']
            }

    except Exception as e:
        print(f"Error listing users: {e}")

    return users_info


# Function to list all shared folders
def list_shared_folders():
    try:
        response = quicksight_client.list_folders(
            AwsAccountId=aws_account_id,
            Namespace='default'
        )
        folders = response.get('FolderSummaryList', [])

        if not folders:
            print("No shared folders found.")
        else:
            print("Shared Folders:")
            for folder in folders:
                print(f"  - Folder Name: {folder['Name']} (ID: {folder['Id']})")

    except Exception as e:
        print(f"Error listing shared folders: {e}")


# Function to list all shared datasets, analyses, and dashboards
def list_shared_items():
    try:
        print("\nListing Shared Datasets, Analyses, and Dashboards:")

        # List shared datasets
        response = quicksight_client.list_data_sets(AwsAccountId=aws_account_id)
        datasets = response.get('DataSetSummaries', [])
        if datasets:
            print("\nShared Datasets:")
            for dataset in datasets:
                print(f"  - Dataset Name: {dataset['Name']} (ID: {dataset['DataSetId']})")

        # List shared analyses
        response = quicksight_client.list_analyses(AwsAccountId=aws_account_id)
        analyses = response.get('AnalysisSummaryList', [])
        if analyses:
            print("\nShared Analyses:")
            for analysis in analyses:
                print(f"  - Analysis Name: {analysis['Name']} (ID: {analysis['AnalysisId']})")

        # List shared dashboards
        response = quicksight_client.list_dashboards(AwsAccountId=aws_account_id)
        dashboards = response.get('DashboardSummaryList', [])
        if dashboards:
            print("\nShared Dashboards:")
            for dashboard in dashboards:
                print(f"  - Dashboard Name: {dashboard['Name']} (ID: {dashboard['DashboardId']})")

    except Exception as e:
        print(f"Error listing shared items: {e}")


# Function to retrieve and display permissions for shared items (datasets, analyses, dashboards)
def list_permissions_for_shared_items(users_info):
    try:
        print("\nListing Permissions for Shared Items:")

        # List shared datasets and permissions
        response = quicksight_client.list_data_sets(AwsAccountId=aws_account_id)
        datasets = response.get('DataSetSummaries', [])
        for dataset in datasets:
            dataset_id = dataset['DataSetId']
            print(f"\nPermissions for Dataset: {dataset['Name']} (ID: {dataset_id})")
            permissions_response = quicksight_client.describe_data_set_permissions(
                AwsAccountId=aws_account_id,
                DataSetId=dataset_id
            )
            for permission in permissions_response.get('Permissions', []):
                principal = permission['Principal']
                actions = permission['Actions']
                if principal in users_info:
                    email = users_info[principal]['Email']
                    role = users_info[principal]['Role']
                    print(f"  - Principal: {principal}, Email: {email}, Role: {role}, Actions: {actions}")

        # List shared analyses and permissions
        response = quicksight_client.list_analyses(AwsAccountId=aws_account_id)
        analyses = response.get('AnalysisSummaryList', [])
        for analysis in analyses:
            analysis_id = analysis['AnalysisId']
            print(f"\nPermissions for Analysis: {analysis['Name']} (ID: {analysis_id})")
            permissions_response = quicksight_client.describe_analysis_permissions(
                AwsAccountId=aws_account_id,
                AnalysisId=analysis_id
            )
            for permission in permissions_response.get('Permissions', []):
                principal = permission['Principal']
                actions = permission['Actions']
                if principal in users_info:
                    email = users_info[principal]['Email']
                    role = users_info[principal]['Role']
                    print(f"  - Principal: {principal}, Email: {email}, Role: {role}, Actions: {actions}")

        # List shared dashboards and permissions
        response = quicksight_client.list_dashboards(AwsAccountId=aws_account_id)
        dashboards = response.get('DashboardSummaryList', [])
        for dashboard in dashboards:
            dashboard_id = dashboard['DashboardId']
            print(f"\nPermissions for Dashboard: {dashboard['Name']} (ID: {dashboard_id})")
            permissions_response = quicksight_client.describe_dashboard_permissions(
                AwsAccountId=aws_account_id,
                DashboardId=dashboard_id
            )
            for permission in permissions_response.get('Permissions', []):
                principal = permission['Principal']
                actions = permission['Actions']
                if principal in users_info:
                    email = users_info[principal]['Email']
                    role = users_info[principal]['Role']
                    print(f"  - Principal: {principal}, Email: {email}, Role: {role}, Actions: {actions}")

    except Exception as e:
        print(f"Error listing permissions for shared items: {e}")


# Main function to list shared folders, shared items, and their permissions with user email and role
def list_shared_folders_and_items():
    users_info = list_users()
    list_shared_folders()
    list_shared_items()
    list_permissions_for_shared_items(users_info)


# Call the main function
list_shared_folders_and_items()
