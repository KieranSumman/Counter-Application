"""
Test Cases for Counter Web Service
"""
from unittest import TestCase
import status
from counter import app

class CounterTest(TestCase):
    """Test Cases for Counter Web Service"""

    def setUp(self):
        self.client = app.test_client()

    def test_create_a_counter(self):
        """It should create a counter"""
        result = self.client.post("/counters/foo")
        self.assertEqual(result.status_code, status.HTTP_201_CREATED)
        data = result.get_json()
        self.assertIn("foo", data)
        self.assertEqual(data["foo"], 0)

    def test_duplicate_counter(self):
        """It should return an error for duplicates"""
        result = self.client.post("/counters/bar")
        self.assertEqual(result.status_code, status.HTTP_201_CREATED)
        result = self.client.post("/counters/bar")
        self.assertEqual(result.status_code, status.HTTP_409_CONFLICT)

    def test_update_a_counter(self):
        """It should update a counter"""
        result = self.client.post("/counters/boot")
        self.assertEqual(result.status_code, status.HTTP_201_CREATED)
        data = result.get_json()
        baseline = data["boot"]
        # UPDATE THE COUNTER
        result = self.client.put("/counters/boot")
        self.assertEqual(result.status_code, status.HTTP_200_OK)
        data = result.get_json()
        self.assertEqual(data["boot"], baseline + 1)

    def test_update_counter_that_doesnt_exist(self):
        """It should return a not found error for updating a non existent counter"""
        result = self.client.put("/counters/strap")
        self.assertEqual(result.status_code, status.HTTP_404_NOT_FOUND)

    def test_read_a_counter(self):
        """It should read the counter value"""
        result = self.client.post("/counters/shoe")
        self.assertEqual(result.status_code, status.HTTP_201_CREATED)
        result = self.client.get("/counters/shoe")
        self.assertEqual(result.status_code, status.HTTP_200_OK)
        data = result.get_json()
        self.assertEqual(data["shoe"], 0)

    def test_read_none_counter(self):
        """It should return a not found error for reading a non existent counter"""
        result = self.client.get("/counters/top")
        self.assertEqual(result.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_a_counter(self):
        """It should delete a counter"""
        result = self.client.post("/counters/cap")
        self.assertEqual(result.status_code, status.HTTP_201_CREATED)
        result = self.client.delete("/counters/cap")
        self.assertEqual(result.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_none_counter(self):
        """It should return a not found error for deleting a non existent counter"""
        result = self.client.delete("/counters/bag")
        self.assertEqual(result.status_code, status.HTTP_404_NOT_FOUND)
        