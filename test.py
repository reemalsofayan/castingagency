import os
import unittest
import json
from app import app
from models import *

EXECUTIVE_PRODUCER = ('eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlNCRVY2R0c1a2dRWUdsMm5ManVkNSJ9.eyJpc3MiOiJodHRwczovL2ZzbmQtY2FzdGluZ2FnZW5jeS5hdS5hdXRoMC5jb20vIiwic3ViIjoiZ29vZ2xlLW9hdXRoMnwxMTM1NTY4OTQ3ODA3Mzk3MTg4OTYiLCJhdWQiOlsiQ2FzdGluZyIsImh0dHBzOi8vZnNuZC1jYXN0aW5nYWdlbmN5LmF1LmF1dGgwLmNvbS91c2VyaW5mbyJdLCJpYXQiOjE1OTcxNTEyODQsImV4cCI6MTU5NzIzNzY4NCwiYXpwIjoiN2I0blZtYzg1RGdFMFpTa3cyenl0UUhIeGpBMjNPTWQiLCJzY29wZSI6Im9wZW5pZCBwcm9maWxlIGVtYWlsIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9ycyIsImRlbGV0ZTptb3ZpZXMiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9ycyIsInBhdGNoOm1vdmllcyIsInBvc3Q6YWN0b3JzIiwicG9zdDptb3ZpZXMiXX0.gOmPbEOKKP4XWkGZGQtutmhiedtftWm3RJ8I5BJ2GCZO6eGq55WSK2WBfaQ39QYFyMuaA-M3dABRf4VDZr2AidfQ3aPxQ2pdn3xGSZdwSF0Fzd13fKtLS3Ru8jhLbkz9mCVgeVRreh8K93T5GCEcDJ3ywzF7ibj5KsEkxmF9P8bnTeqa-xqkBXt6hTkNC4pi5XwL97lzg0cpHEbo40wkmw-c-D02Yh4x6d-6r4xA0Upwu8p8FchBl7BfYD6gyVOI2zobd22Q-6Ez37aypK1SexYeb_--YbUGTITkO2HbOEjdguHK3gsvP8vO5yJ4OvNel_OCvb0DUHKTSmwKOzUH1Q')
CASTING_DIRECTOR = ('eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlNCRVY2R0c1a2dRWUdsMm5ManVkNSJ9.eyJpc3MiOiJodHRwczovL2ZzbmQtY2FzdGluZ2FnZW5jeS5hdS5hdXRoMC5jb20vIiwic3ViIjoiZ29vZ2xlLW9hdXRoMnwxMTA2MTIwMTM1OTMyNTQ0MTk2MDkiLCJhdWQiOlsiQ2FzdGluZyIsImh0dHBzOi8vZnNuZC1jYXN0aW5nYWdlbmN5LmF1LmF1dGgwLmNvbS91c2VyaW5mbyJdLCJpYXQiOjE1OTcxNTA3MjMsImV4cCI6MTU5NzIzNzEyMywiYXpwIjoiN2I0blZtYzg1RGdFMFpTa3cyenl0UUhIeGpBMjNPTWQiLCJzY29wZSI6Im9wZW5pZCBwcm9maWxlIGVtYWlsIiwicGVybWlzc2lvbnMiOltdfQ.MaaWcXZCXBg6-H1EUjrN_KMsripYjaLX_U1VFqSRSpkgOVhGDNiqBoLIgjXktu0xc_FvQFBdS7x5kLaZOuhz0j2AAAennqwWCNZ0bOEZcWX2GKI2WjjIlfRIZGyati6Ku9tHw6T2zPrSD3Rx6tnBCYAgMH8Vu_skXiFVXVnrtHWWjVki4WyJTT-Q70F51B9DPCWlWPcKYaRVGsZBch_IBWGb2aOz5Cskuf6QCzKUikMhqS8lf3ArmVuJIb--JeIik3DLhTgu1gAO3RgEXCoR46ry_5WL7vSmSnnD5Aiq8ozrBqsMouyLKmj29yHaD3LXv8_ubEnWFbyn83LBWIQV0g')
CASTING_ASSISTANT = ('eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlNCRVY2R0c1a2dRWUdsMm5ManVkNSJ9.eyJpc3MiOiJodHRwczovL2ZzbmQtY2FzdGluZ2FnZW5jeS5hdS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWYzMmJhMzZmNTM2ZTkwMDM3YWVjOTUyIiwiYXVkIjoiQ2FzdGluZyIsImlhdCI6MTU5NzE2MDMxMywiZXhwIjoxNTk3MjQ2NzEzLCJhenAiOiI3YjRuVm1jODVEZ0UwWlNrdzJ6eXRRSEh4akEyM09NZCIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiXX0.J94yZUJE-igB_zpwB7kAwMH_fb526URjUPbe6vE4Pw9M1_aqNahMjAp3dVlDXO7OFEgb2iewO5XAkIgAwr2hhA4EF0eH_teEfjTfjxx0Y4IS1NZSdrHsImaQPW1xmwjwNmrysDCmaVC7EP5hoaRFOQTK63AcU-E2vl3ePIYenR0CbX2YXrJiwKIc3gYrQ2iOS2RD8NCEGH_5zwvshGDkk_NqIAmjcPYpLUWNhk5OaakpviENbFyeGxwAtWXs5tbXKtCClFqvJaLVDb-NTl9iGZRcXeXuDCXRpJHWEOc16i2iWVNoUrIoARxE6B2YrSf2A0zG5VavFTaO7oye2N8ZYw')


class CastingAgencyTestCase(unittest.TestCase):

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = app.test_client()

        self.database_name = "castingagency"
        self.database_path = 'postgresql://postgres:root@localhost:5432/castingagency'

        self.new_movie = {
            "title": " wld whcnwebz23",
            "release_date": "2018"
        }

        self.new_movie2 = {
            "title": " gofgwwe",
            "release_date": "2008"
        }

        self.new_movie3 = {
            "title": " goffdes5",
            "release_date": "2010"
        }

        self.new_movie4 = {
            "title": " titawefnff",
            "release_date": "2000"
        }

        self.new_movie5 = {
            "title": " the budewfwewr",
            "release_date": "2017"
        }

        self.new_actor2 = {
            "name": "richard armfiwftage",
            "age": 44,
            "gender": "male"
        }

        self.new_actor = {
            "name": "richard armietage",
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
