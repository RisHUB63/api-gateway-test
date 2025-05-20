from locust import HttpUser, task, between

class MyUser(HttpUser):
    wait_time = between(1, 3)
    host = "http://localhost:8000"
    @task
    def get_data(self):
        self.client.get("/api/create")
        self.client.get("/api/update")
        self.client.get("/api/delete")
        self.client.get("/api/list")
        self.client.get("/api/format")
