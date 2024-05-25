import json

import boto3
import jwt

from auth.schemes import UserInDB
from config import settings


class Cognito:
    def __init__(self, client_id: str, user_pool_id: str):
        self.region_name = settings.AWS_REGION
        self._cgnt = boto3.client('cognito-idp', region_name=self.region_name)
        self.client_id = client_id
        self.user_pool_id = user_pool_id

    def login(self, username: str, password: str, auth_flow: str = 'ADMIN_NO_SRP_AUTH'):
        auth_data = {'USERNAME': username, 'PASSWORD': password}
        auth_result = {}
        try:
            r = self._cgnt.admin_initiate_auth(
                UserPoolId=self.user_pool_id,
                AuthFlow=auth_flow,
                AuthParameters=auth_data,
                ClientId=self.client_id,
            )
            auth_data = r.get('AuthenticationResult', {})
            access_token = auth_data.get('IdToken')
            refresh_token = auth_data.get('RefreshToken')
            expires_in = auth_data.get('ExpiresIn')
            auth_result = {
                'access_token': access_token,
                'refresh_token': refresh_token,
                'expires_in': expires_in,
            }
        except Exception as e:
            # TODO log para registro de tentativas
            print(e)

        return auth_result

    def get_user(self, token):
        return self._decode_jwt(token=token)

    def _decode_jwt(self, token):
        url_jwks = f'https://cognito-idp.{self.region_name}.amazonaws.com/{self.user_pool_id}/.well-known/jwks.json'
        jwks_client = jwt.PyJWKClient(url_jwks)
        signing_key = jwks_client.get_signing_key_from_jwt(token)
        data = jwt.decode(
            token,
            signing_key.key,
            algorithms=['RS256'],
            audience=settings.COGNITO_CLIENT_ID,
            options={'verify_aud': 'true'},
        )
        extra_data = json.loads(data.get('custom:extra_data'))
        user_in = UserInDB(
            username=data.get('cognito:username'),
            sub=data.get('sub'),
            provider_pix=data.get('custom:provider'),
            extra_data=extra_data,
        )
        return user_in
