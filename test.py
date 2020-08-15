import os
import unittest
import json
from app import app
from models import *
# from config import Config


EXECUTIVE_PRODUCER = ('eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlNCRVY2R0c1a2dRWUdsMm5ManVkNSJ9.eyJpc3MiOiJodHRwczovL2ZzbmQtY2FzdGluZ2FnZW5jeS5hdS5hdXRoMC5jb20vIiwic3ViIjoiZ29vZ2xlLW9hdXRoMnwxMTM1NTY4OTQ3ODA3Mzk3MTg4OTYiLCJhdWQiOlsiQ2FzdGluZyIsImh0dHBzOi8vZnNuZC1jYXN0aW5nYWdlbmN5LmF1LmF1dGgwLmNvbS91c2VyaW5mbyJdLCJpYXQiOjE1OTc1MTE1MDgsImV4cCI6MTU5NzU5Nzg5NSwiYXpwIjoiN2I0blZtYzg1RGdFMFpTa3cyenl0UUhIeGpBMjNPTWQiLCJzY29wZSI6Im9wZW5pZCBwcm9maWxlIGVtYWlsIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9ycyIsImRlbGV0ZTptb3ZpZXMiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9ycyIsInBhdGNoOm1vdmllcyIsInBvc3Q6YWN0b3JzIiwicG9zdDptb3ZpZXMiXX0.fQwrTnQX3cRm94oIF9svxVnHFV2x6PID7ALdPU-qZVt0LwM90ZZ4rFU6l83VdJ0h-xOxNC7yC_bo2_yvKxqx9mSgjoHmI5k0QEhhlh-iXu0pjBkMvPdJ-X9pd1thTNCKoO7GmK4s3yF8sc1RtJiWw4uOXbs1jqJsNnDmJmoWuTe5pFdJORtLKkGNqg2rpltMHRR5npfAOhWojfMa1A_WXW0i03kwGOTvuupi5JK-r7PTg_4TbCI6q8KkVcfjHZYzjyMWTIlUINiK1AGq_xSy2h8gxNWVBn1b80bsgRNe2i4chYezVXxcHyLAzjhGgCDYUrvxoPzp-25PyfMMQR5sLA')
CASTING_DIRECTOR = ('eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlNCRVY2R0c1a2dRWUdsMm5ManVkNSJ9.eyJpc3MiOiJodHRwczovL2ZzbmQtY2FzdGluZ2FnZW5jeS5hdS5hdXRoMC5jb20vIiwic3ViIjoiZ29vZ2xlLW9hdXRoMnwxMTA2MTIwMTM1OTMyNTQ0MTk2MDkiLCJhdWQiOlsiQ2FzdGluZyIsImh0dHBzOi8vZnNuZC1jYXN0aW5nYWdlbmN5LmF1LmF1dGgwLmNvbS91c2VyaW5mbyJdLCJpYXQiOjE1OTc1MTE3MjYsImV4cCI6MTU5NzU5ODExMywiYXpwIjoiN2I0blZtYzg1RGdFMFpTa3cyenl0UUhIeGpBMjNPTWQiLCJzY29wZSI6Im9wZW5pZCBwcm9maWxlIGVtYWlsIiwicGVybWlzc2lvbnMiOltdfQ.eMbfqamTqI3kC-wKeV-atkPMBBQfiaKnz9LDmG8J90O9cvTyjsWMZQC2YL81qCYuLf5JS0vd23nZ8XvJGKPWn4SXL_NnYLVgS854f_t84KxQFI8gBIGpNeAOa4aGGwfyDxkxfXoi0OmIajohSz2wigmuTpUkJISjj66R-65sTDGp2-fW4O0knyuY2s1-f2szZHo4xcT7abXIoTJVhq0rWRXKLrZFZq1bRXz7GyJU5BnvX-T0iJ6SYW9W5geXdJ2lWuvsy9q9W_wptDVNo-WeUiSOkJt5O15VR1HtTGqgw0F73HNOtBX-jSMBzpo0tw5ITAvNYgewC9BvhoAU9f8zeA')
CASTING_ASSISTANT = ('eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlNCRVY2R0c1a2dRWUdsMm5ManVkNSJ9.eyJpc3MiOiJodHRwczovL2ZzbmQtY2FzdGluZ2FnZW5jeS5hdS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWYzMmJhMzZmNTM2ZTkwMDM3YWVjOTUyIiwiYXVkIjoiQ2FzdGluZyIsImlhdCI6MTU5NzUxMTg0MSwiZXhwIjoxNTk3NTk4MjI4LCJhenAiOiI3YjRuVm1jODVEZ0UwWlNrdzJ6eXRRSEh4akEyM09NZCIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiXX0.YEQ9E3CKiqaF7JgMMi7rqnl7Yhr9RsYaWgkJexQY3o4AXgLuMhpdbp1ht1UvnrpDZo-uPYIcASgh7ML-rYH33d47lAFCbK9wemLstJoa1VIeyBDA0-oVDVwRw1KPn40e2Zik2mdN7Sb2aa06MeiLXNhvUitJfJHuCLGzJNB5q0A3z9-yDwjFlii2Vee0sdGlt9rJ9szWc87h52kLvGYs6aySHVrZpL737pcMPqc7flNSfdDFH7nYpG0A-8W9AVMN7ju8oROmyw2eXShTrzfajE7GS7D5hKtji36UZC25sfRhQTiadEdev0vqHXaSJJ0r-GIhhSUdTymj_VQct0nNoA')


class CastingAgencyTestCase(unittest.TestCase):

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = app.test_client()
       

        self.database_name = "castingagency"
        self.database_path = 'postgresql://postgres:root@localhost:5432/castingagency'

        self.new_movie = {
            "title": "Extrfea 2020",
            "release_date": "2018"
        }

        self.new_movie2 = {
            "title": "cindsefrea",
            "release_date": "2008"
        }

        self.new_movie3 = {
            "title": " adiin",
            "release_date": "2010"
        }

        self.new_movie4 = {
            "title": "downtobby",
            "release_date": "2000"
        }

        self.new_movie5 = {
            "title": "  beautifund",
            "release_date": "2017"
        }

        self.new_actor2 = {
            "name": "tosknjkfas",
            "age": 44,
            "gender": "male"
        }

        self.new_actor = {
            "name": "thesf knjroc",
            "age": 22,
            "gender": "male"
        }

    def tearDown(self):
        pass

    def test_get_movies(self):
        # send a get request to retrieve all movies from database  uusing the
        # role executive producer
        response = self.app.get(
            '/movies',
            headers={
                'Authorization': f'Bearer {EXECUTIVE_PRODUCER}'})
        data = json.loads(response.data)
        # check the status code
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])

    def test_401_get_movies(self):
        # send a request to  retrieve with no token
        response = self.app.get('/movies', headers={'Authorization': ''})
        self.assertEqual(response.status_code, 401)

    def test_add_movie(self):
        # query all movies before adding a new one
        movies_before_newmovie = Movie.query.all()
        # send a post request to add a new movie
        response = self.app.post(
            '/movies',
            json=self.new_movie,
            headers={
                'Authorization': f'Bearer {EXECUTIVE_PRODUCER}'})
        data = json.loads(response.data)
        # query all movies after adding a new one
        movies_After_newmovie = Movie.query.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        # if the number of movies incerase it means successful addition
        self.assertTrue(len(movies_before_newmovie)
                        < len(movies_After_newmovie))

    def test_422_if_movie_addition_not_allowed(self):
        # send a post request without  the a json body
        response = self.app.post(
            '/movies',
            json={},
            headers={
                'Authorization': f'Bearer {EXECUTIVE_PRODUCER}'})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)

    def test_modify_movie(self):
        # add a new movie to be modified later
        res = self.app.post(
            '/movies',
            json=self.new_movie2,
            headers={
                'Authorization': f'Bearer {EXECUTIVE_PRODUCER}'})
        data = json.loads(res.data)

        # retrieve the new movie just added
        movie = Movie.query.filter_by(id=data['movie']['id']).one_or_none()
        # modity the movie with the new information
        res2 = self.app.patch(
            f'/movies/{movie.id}',
            json=self.new_movie3,
            headers={
                'Authorization': f'Bearer {EXECUTIVE_PRODUCER}'})
        data2 = json.loads(res.data)
        self.assertEqual(res2.status_code, 200)
        self.assertEqual(data2['success'], True)

    def test_422_modify_movie(self):
        # send a post request without  the a json body for new changes
        response = self.app.patch(
            '/movies/1',
            json={},
            headers={
                'Authorization': f'Bearer {EXECUTIVE_PRODUCER}'})

        data = json.loads(response.data)
        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    def test_delete_movie(self):
        # add a new movie to be deleted later
        res = self.app.post(
            '/movies',
            json=self.new_movie4,
            headers={
                'Authorization': f'Bearer {EXECUTIVE_PRODUCER}'})
        data = json.loads(res.data)
        # rerieve the newly added movie
        movie = Movie.query.filter_by(id=data['movie']['id']).one_or_none()

        # delete the movie
        res2 = self.app.delete(
            f'/movies/{movie.id}',
            headers={
                'Authorization': f'Bearer {EXECUTIVE_PRODUCER}'})

        data2 = json.loads(res2.data)
        self.assertEqual(res2.status_code, 200)
        self.assertEqual(data2['success'], True)

    def test_delete_movie_unauthorized(self):
        # post a new movie with executive producer  role
        res = self.app.post(
            '/movies',
            json=self.new_movie5,
            headers={
                'Authorization': f'Bearer {EXECUTIVE_PRODUCER}'})
        data = json.loads(res.data)
        # rerieve the newly added movie
        movie = Movie.query.filter_by(id=data['movie']['id']).one_or_none()
        # delete the movie with casting director role ,which not allowed to
        res2 = self.app.delete(
            f'/movies/{movie.id}',
            headers={
                'Authorization': f'Bearer {CASTING_DIRECTOR}'})

        data2 = json.loads(res2.data)
        self.assertEqual(res2.status_code, 403)

        self.assertEqual(res2.get_json()['message'], 'unauthorized')

    def test_get_actors(self):
        # retrieve all actor in database
        response = self.app.get(
            '/actors',
            headers={
                'Authorization': f'Bearer {EXECUTIVE_PRODUCER}'})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actors'])

    def test_401_get_actors(self):
        # retrieve all actor in database with no Authorization
        response = self.app.get('/actors', headers={'Authorization': ''})
        self.assertEqual(response.status_code, 401)

    def test_add_Actor(self):
        # retrieve all actors before adding a new one
        Actors_before_newactor = Actor.query.all()
        response = self.app.post(
            '/actors',
            json=self.new_actor,
            headers={
                'Authorization': f'Bearer {EXECUTIVE_PRODUCER}'})
        data = json.loads(response.data)
        # retrieve all actors after adding a new one
        Actors_After_newactor = Actor.query.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        # the number of actors shoud increase
        self.assertTrue(len(Actors_before_newactor)
                        < len(Actors_After_newactor))

    def test_actor_addition_unathorized(self):
        # add an actor with casting director role ,which not allowed to

        response = self.app.post(
            '/actors',
            json={},
            headers={
                'Authorization': f'Bearer {CASTING_ASSISTANT}'})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 403)
        self.assertEqual(data['success'], False)

    def test_modify_actor(self):
        # add a new actor to be modified later
        res = self.app.post(
            '/actors',
            json=self.new_actor,
            headers={
                'Authorization': f'Bearer {EXECUTIVE_PRODUCER}'})
        data = json.loads(res.data)

        # retrieve the newly added actor
        actor = Actor.query.filter_by(id=data['actor']['id']).one_or_none()
        # modify the actor just retrieved
        res2 = self.app.patch(
            f'/actors/{actor.id}',
            json=self.new_actor2,
            headers={
                'Authorization': f'Bearer {EXECUTIVE_PRODUCER}'})
        data2 = json.loads(res.data)
        self.assertEqual(res2.status_code, 200)
        self.assertEqual(data2['success'], True)

    def test_422_modify_actor(self):
        # patch an actor without a json body
        response = self.app.patch(
            '/actors/1',
            json={},
            headers={
                'Authorization': f'Bearer {EXECUTIVE_PRODUCER}'})

        data = json.loads(response.data)
        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    def test_delete_actor(self):
        # add a new actor to be deleted later
        res = self.app.post(
            '/actors',
            json=self.new_actor,
            headers={
                'Authorization': f'Bearer {EXECUTIVE_PRODUCER}'})
        data = json.loads(res.data)
        # retrieve the newly added actor
        actor = Actor.query.filter_by(id=data['actor']['id']).one_or_none()

        # delete the actor just retrieved
        res2 = self.app.delete(
            f'/actors/{actor.id}',
            headers={
                'Authorization': f'Bearer {EXECUTIVE_PRODUCER}'})

        data2 = json.loads(res2.data)
        self.assertEqual(res2.status_code, 200)
        self.assertEqual(data2['success'], True)

    def test_delete_actor_unauthorized(self):
        # add a new actor to be deleted later
        res = self.app.post(
            '/actors',
            json=self.new_actor,
            headers={
                'Authorization': f'Bearer {EXECUTIVE_PRODUCER}'})
        data = json.loads(res.data)
        actor = Actor.query.filter_by(id=data['actor']['id']).one_or_none()
        # delete the actor with CASTING_ASSISTANT role whcih not allowed to
        res2 = self.app.delete(
            f'/actors/{actor.id}',
            headers={
                'Authorization': f'Bearer {CASTING_ASSISTANT}'})

        data2 = json.loads(res2.data)
        self.assertEqual(res2.status_code, 403)

        self.assertEqual(data2['message'], 'unauthorized')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
