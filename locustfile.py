# locustfile.py

# Basic test user
'''
from locust import HttpUser, task, between

class TestUtilisateur(HttpUser):
    wait_time = between(1, 3)
    
    @task
    def accueil(self):
        self.client.get("/")


# Additional endurance test user
from locust import HttpUser, task, between

class EnduranceTestUser(HttpUser):
    wait_time = between(2, 5)
    
    @task
    def long_running_test(self):
        self.client.get("/")

'''

from locust import HttpUser, task, between

class AuthenticatedUser(HttpUser):
    wait_time = between(1, 3)
    
    def on_start(self):
        # Exécuté une fois au démarrage pour chaque utilisateur
        response = self.client.post("/login", json={
            "username": "testuser",
            "password": "password123"
        })
        # Récupérer le token si nécessaire
        self.token = response.json().get("token")
    
    @task
    def access_protected_resource(self):
        headers = {"Authorization": f"Bearer {self.token}"}
        self.client.get("/dashboard", headers=headers)
    
    @task
    def update_profile(self):
        headers = {"Authorization": f"Bearer {self.token}"}
        self.client.put("/profile", json={"name": "Test User"}, headers=headers)