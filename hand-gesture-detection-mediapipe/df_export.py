import boto3
import pandas as pd

# Initialize DynamoDB resource
dynamodb = boto3.resource('dynamodb', region_name='ap-southeast-1')  # Change the region if needed
table_name = 'TicTacToeGameHistory'

def export_dynamodb_to_dataframe():
    try:
        table = dynamodb.Table(table_name)
        # Scan the entire table (use cautiously for large tables)
        response = table.scan()
        items = response.get('Items', [])

        # Convert to DataFrame
        df = pd.DataFrame(items)

        # Check if DataFrame is empty
        if df.empty:
            print("No data found in the DynamoDB table.")
            return None

        print("Data exported successfully!")
        return df

    except Exception as e:
        print(f"Error exporting data: {e}")
        return None

# Export data and save to Python file
df = export_dynamodb_to_dataframe()
print(df.head())