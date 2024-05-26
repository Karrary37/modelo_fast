from locust import HttpUser, TaskSet, between, task


class UserBehavior(TaskSet):
    def on_start(self):
        self.token = None
        self.create_token()

    def create_token(self):
        response = self.client.post(
            '/auth/login', json={'username': 'user1', 'password': 'password1'}
        )
        if response.status_code == 200:
            self.token = response.json().get('token')

    @task(2)
    def create_link(self):
        if self.token:
            self.client.post(
                '/shorten/',
                headers={'Authorization': f'Bearer {self.token}'},
                json={
                    'original_url': 'https://formalizacao-staging.happyconsig.com.br/c3e5b945-b849-4d6c-aa73-43f9f8ab6d86'
                },
            )


class WebsiteUser(HttpUser):
    tasks = [UserBehavior]
    wait_time = between(1, 5)
