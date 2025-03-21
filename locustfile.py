from locust import HttpUser, task, between

class LoadTestUser(HttpUser):
    wait_time = between(1, 3)  # Simulate a real user's wait time between requests

    @task
    def get_request(self):
        """Simulates GET request to your API endpoint."""
        self.client.get("http://127.0.0.1:8000/api/allcourses/")  # Replace with your actual API URL

    
    @task 
    def post_request(self):
       
        self.client.post("http://127.0.0.1:8000/auth/student/login/", json={"username": "STDArghya","password":"Arghya@1234"})  # Adjust payload

