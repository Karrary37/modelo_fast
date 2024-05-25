from locust import HttpUser, TaskSet, task, between

class UserBehavior(TaskSet):
    @task(1)
    def create_link(self):
        self.client.post("/shorten/", json={"original_url": "https://formalizacao-staging.happyconsig.com.br/c3e5b945-b849-4d6c-aa73-43f9f8ab6d86"})
class WebsiteUser(HttpUser):
    tasks = [UserBehavior]
    wait_time = between(1, 5)
