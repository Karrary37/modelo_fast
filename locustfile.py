from locust import HttpUser, TaskSet, between, task


class UserBehavior(TaskSet):
    @task(1)
    def create_link(self):
        jwt = self.client.post(
            '/auth/login',
            json={
                'username': 'user1',
                'password': 'password1'
            }
        )

        self.client.post(
            '/shorten/',
            headers={
                'Authorization': f'Bearer {jwt.json().get("token")}'
            },
            json={
                'original_url': 'https://formalizacao-staging.happyconsig.com.br/c3e5b945-b849-4d6c-aa73-43f9f8ab6d86'
            },
        )


class WebsiteUser(HttpUser):
    tasks = [UserBehavior]
    wait_time = between(1, 5)
