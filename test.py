import os
import unittest
import json
from app import app
from models import *

EXECUTIVE_PRODUCER = ('eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlNCRVY2R0c1a2dRWUdsMm5ManVkNSJ9.eyJpc3MiOiJodHRwczovL2ZzbmQtY2FzdGluZ2FnZW5jeS5hdS5hdXRoMC5jb20vIiwic3ViIjoiZ29vZ2xlLW9hdXRoMnwxMTM1NTY4OTQ3ODA3Mzk3MTg4OTYiLCJhdWQiOlsiQ2FzdGluZyIsImh0dHBzOi8vZnNuZC1jYXN0aW5nYWdlbmN5LmF1LmF1dGgwLmNvbS91c2VyaW5mbyJdLCJpYXQiOjE1OTc0MzIwNjIsImV4cCI6MTU5NzUxODQ0OSwiYXpwIjoiN2I0blZtYzg1RGdFMFpTa3cyenl0UUhIeGpBMjNPTWQiLCJzY29wZSI6Im9wZW5pZCBwcm9maWxlIGVtYWlsIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9ycyIsImRlbGV0ZTptb3ZpZXMiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9ycyIsInBhdGNoOm1vdmllcyIsInBvc3Q6YWN0b3JzIiwicG9zdDptb3ZpZXMiXX0.FwYL6AeIWqRugULKLD1RFUzrp8tkvPupO6runWXjjNLF3_Uss11Aw1E8DSfxZe3IeUrIEBeVmABRIA_a2Xx4s1_OlhZQT3IObYVfZn8q9Qg0GfTXVUboYik-HpiA4YPJnM2iMGIB4sT7TFy8AWkGCYpDCijeuu7PDKN_-jGFowPIHWNlpDbcK-IAK_ww-pMQrQcMu4n0kdOfwFV5-AatS7tROKvr2qnz27qyK7pmUpoM-L-3giv2KMbwjgrPTJAj1oBKxMDpa8g57j60N97jR14UrMmBRUBeJ1wK3h5pNd-9jub1aW7SrYqs0_3UtAdfbchSXVV1d4YjwdCBdU-w9Q')
CASTING_DIRECTOR = ('eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlNCRVY2R0c1a2dRWUdsMm5ManVkNSJ9.eyJpc3MiOiJodHRwczovL2ZzbmQtY2FzdGluZ2FnZW5jeS5hdS5hdXRoMC5jb20vIiwic3ViIjoiZ29vZ2xlLW9hdXRoMnwxMTA2MTIwMTM1OTMyNTQ0MTk2MDkiLCJhdWQiOlsiQ2FzdGluZyIsImh0dHBzOi8vZnNuZC1jYXN0aW5nYWdlbmN5LmF1LmF1dGgwLmNvbS91c2VyaW5mbyJdLCJpYXQiOjE1OTc0MzIzMzMsImV4cCI6MTU5NzUxODcyMCwiYXpwIjoiN2I0blZtYzg1RGdFMFpTa3cyenl0UUhIeGpBMjNPTWQiLCJzY29wZSI6Im9wZW5pZCBwcm9maWxlIGVtYWlsIiwicGVybWlzc2lvbnMiOltdfQ.jXL8qXeNeAxg_zOXyRFZ_Z2jqzDizxshMeDZMUNmJHrfsXQRtYtbibrsME7AtKVPrHL6D_HAw4b1Xrw9GHEuxvJhYRj92o7NsaanG-Ji6Ezs6pIpspBH305MkFOGUG4GcUuBwzFQFlGAaFczMLznOQvPbRP9wSYQSNZB8hk8-kILwKq9_gVfBpbqAlB-fhuO3G3dFZQAzw8MFhluZ9wZtaH0MWCytVgTeEcuZ-hkwBzNKJ9g7C76iO2efujfNaMCGRlo5fqnjAPrJSu2i4yNu3qaDjKgk6VmfXP8hy9djPU-1R0Q3G_pR-jX3WEvm5XzbRFdERAJncEI1O-2HUnZWw')
CASTING_ASSISTANT = ('eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlNCRVY2R0c1a2dRWUdsMm5ManVkNSJ9.eyJpc3MiOiJodHRwczovL2ZzbmQtY2FzdGluZ2FnZW5jeS5hdS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWYzMmJhMzZmNTM2ZTkwMDM3YWVjOTUyIiwiYXVkIjoiQ2FzdGluZyIsImlhdCI6MTU5NzQzMjQ3MiwiZXhwIjoxNTk3NTE4ODU5LCJhenAiOiI3YjRuVm1jODVEZ0UwWlNrdzJ6eXRRSEh4akEyM09NZCIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiXX0.wZnTBSg0vWx9VVA2J2OOztADPlrwIKGUH7wdBZTSa9qS5o8EHl7SI2S_mg_KM5WRDrF_x_YqRqaEip6BHJfQOXDy-Qv17xnINPr2d7Zqo7Yud3MbPyhCSFave-RLBZz5hw8GLsH0MDdReGOTFpEFr22symBipkoPNpyWVfC4IQxzXbtSLd1BSaGohvIMerNHDS8tp2HaWuhh7D_cGRpNfMVpmVdoAu9vRNccBz87AHgHpWijHXteSkvPqfP4DPIBJP_SIJ21zxibldBq37oLLyjfWk5PbUPqAYq8azakgfCxPe0WeL1hF8-ACywE_zK11jfyp77mHCrkajZGEjsUvw')


class CastingAgencyTestCase(unittest.TestCase):

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = app.test_client()

        self.database_name = "castingagency"
        self.database_path = 'postgresql://postgres:root@localhost:5432/castingagency'

        self.new_movie = {
            "title": "Extractioon 2020",
            "release_date": "2018"
        }

        self.new_movie2 = {
            "title": "cindrellla",
            "release_date": "2008"
        }

        self.new_movie3 = {
            "title": " alldiin",
            "release_date": "2010"
        }

        self.new_movie4 = {
            "title": "downtonabby",
            "release_date": "2000"
        }

        self.new_movie5 = {
            "title": "  beautiful mind",
            "release_date": "2017"
        }

        self.new_actor2 = {
            "name": "toas",
            "age": 44,
            "gender": "male"
        }

        self.new_actor = {
            "name": "the roc",
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
