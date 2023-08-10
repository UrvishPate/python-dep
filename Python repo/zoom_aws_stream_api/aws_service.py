import boto3
from typing import Dict
from botocore.exceptions import BotoCoreError, ClientError

class AWSService:
    def __init__(self, aws_access_key: str, aws_secret_key: str):
        self.aws_access_key = aws_access_key
        self.aws_secret_key = aws_secret_key
        self.client = boto3.client(
            'ivs',
            aws_access_key_id=self.aws_access_key,
            aws_secret_access_key=self.aws_secret_key,
            region_name='us-west-2'
        )

    def create_stream(self, zoom_meeting_id: str, zoom_passcode: str) -> Dict[str, str]:
        try:
            response = self.client.create_channel(
                name=f'zoom_{zoom_meeting_id}',
                latencyMode='NORMAL',
                type='BASIC',
                authorized=True
            )
            return {
                'stream_arn': response['channel']['arn'],
                'stream_url': response['channel']['ingestEndpoint'],
                'stream_key': response['streamKey']['value']
            }
        except (BotoCoreError, ClientError) as error:
            return {"error": str(error)}
