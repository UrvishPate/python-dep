import requests
from typing import Dict
from utils import handle_error, setup_logger
from aws_service import AWSService

class ZoomService:
    def __init__(self, zoom_meeting_id: str, zoom_passcode: str, aws_access_key: str, aws_secret_key: str):
        self.zoom_meeting_id = zoom_meeting_id
        self.zoom_passcode = zoom_passcode
        self.aws_service = AWSService(aws_access_key, aws_secret_key)
        self.logger = setup_logger('zoom_service', 'zoom_service.log')

    def create_meeting(self) -> Dict[str, str]:
        try:
            # Assuming Zoom API endpoint for creating a meeting
            response = requests.post(
                f'https://api.zoom.us/v2/users/me/meetings',
                headers={'Authorization': 'Bearer YOUR_ZOOM_JWT_TOKEN'},
                json={
                    'topic': 'AWS Stream',
                    'type': 2,
                    'settings': {
                        'meeting_authentication': True,
                        'meeting_authentication_option': self.zoom_meeting_id,
                        'meeting_authentication_pass': self.zoom_passcode
                    }
                }
            )
            response.raise_for_status()

            meeting = response.json()
            self.logger.info(f'Zoom meeting created with ID: {meeting["id"]}')

            stream_details = self.aws_service.create_stream(self.zoom_meeting_id, self.zoom_passcode)
            if 'error' in stream_details:
                raise Exception(stream_details['error'])

            self.logger.info(f'AWS stream created with ARN: {stream_details["stream_arn"]}')
            return stream_details

        except Exception as error:
            return handle_error(self.logger, error)
