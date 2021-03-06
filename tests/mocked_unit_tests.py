""" Use mock to test socket, db, oauth """
from os.path import dirname, join
import sys
sys.path.append(join(dirname(__file__), "../"))
import unittest
import unittest.mock as mock
import app
import models
import db_utils
import db_instance
from db_instance import DB
from models import AuthUser
from models import Room

KEY_INPUT = "input"
KEY_EXPECTED = "expected"
KEY_COUNT = "count"

KEY_NAME = "name"
KEY_UCID = "ucid"
KEY_ID = "id"
KEY_ROLE = "role"

KEY_DATE = "date"
KEY_TIME = "available time"

KEY_ROOM_NUM = "room number"
KEY_SIZE = "room size" 
KEY_CAPACITY = "room capacity"

KEY_DATA = "data sent"
AUTH_TYPE = "auth_type"
NAME = "name"
EMAIL = "email"


class MockedJson:
    """ Mock json file format """
    def __init__(self, json_text):
        ''' Initialize json '''
        self.json_text = json_text

    def json(self):
        ''' Return json format '''
        return self.json_text


class MockedDB:
    """ Mock database including creating table and session """
    def __init__(self, app):
        ''' Initialize db '''
        self.app = app

    def Model(self):
        ''' mock db model '''
        return

    def app(self):
        ''' mock db app '''
        return self.app

    def create_all(self):
        ''' mock db create all '''
        return

    def session(self):
        ''' mock db sessions '''
        return MockedSession(self.app)


class MockedSession:
    """ Mock the property of database session """
    def __init__(self, data):
        ''' Initialize data '''
        self.data = data

    def commit(self):
        ''' mock db's session commit '''
        return

    def query(self):
        ''' mock db's session query '''
        return MockedQuery

    def add(self):
        ''' mock db's session add '''
        return
    
class MockedQuery:
    """ Mock the property of database query """
    def __init__(self, data):
        ''' Initialize data '''
        self.data = data
        
    def filter(self):
        ''' mock filter '''
        return


class MockedSocket:
    """ Mock socket for listening to incoming and outgoing data """
    def __init__(self, channel, data):
        ''' Initialize socket '''
        self.channel = channel
        self.data = data

    def on(self):
        ''' mock socket on method '''
        return

    def emit(self):
        ''' mock socket emit method'''
        return
    

class DbUtilTestCase(unittest.TestCase):
    """ Test functions that uses socket """
    
    def setUp(self):
        """ Initialize before unit test"""
        self.test_login_info = [
            {
                KEY_ID: 123,
                KEY_UCID: "jd123",
                KEY_ROLE: "student",
                KEY_NAME: "Jane Dow",
                KEY_EXPECTED: {
                    KEY_ID: 123,
                    KEY_UCID: "jd123",
                    KEY_ROLE: "student",
                    KEY_NAME: "Jane Dow",
                },
            },
        ]
        
        self.test_room_info = [
            {
                KEY_ID: 2,
                KEY_ROOM_NUM: 101,
                KEY_SIZE: "small",
                KEY_CAPACITY: 8,
                KEY_EXPECTED: {
                    KEY_ID: 2,
                    KEY_ROOM_NUM: 101,
                    KEY_SIZE: "small",
                    KEY_CAPACITY: 8,
                },
            },
        ]
        
        self.test_date_info = [
            {
                KEY_DATE: '11-12-2020',
                KEY_TIME: {
                    9: [2], 
                    11: [3], 
                    13: [4], 
                    15: [2],
                },
                KEY_EXPECTED: {
                    KEY_DATE: '11-12-2020',
                    KEY_TIME: {
                        9: [], 
                        11: [3], 
                        13: [4], 
                        15: [2],
                    }
                },
            },
        ]
        
        self.success_test_connect = [
            {
                KEY_INPUT: 2,
                KEY_EXPECTED: {
                    KEY_COUNT: 2,
                },
            },
        ]

    
    def mocked_db(self, app):
        """ Mock database """
        return MockedDB(app)

    def mocked_socket(self):
        """ Mock socket """
        return MockedSocket("connected", {"test": "Connected"})
        
    def mocked_add_or_get_auth_user(self, ucid, name):
        """ Mock adding auth user """
        return MockedDB
        
    def mocked_get_user_obj_from_id(self, id, as_dict=False):
        """ Mock the user id obj """
        return MockedDB
        
    def mocked_date(self, data):
        """ Mock receiving date """
        return MockedSocket("channel", {'DATE_KEY': '11-11-2020'})
      
    def test_on_connect(self):
        """ Test who successfully connected """
        for test in self.success_test_connect:
            with mock.patch("app.on_connect", self.mocked_socket):
                response = app.on_connect()
                expected = test[KEY_EXPECTED]

            self.assertNotEqual(response, expected[KEY_COUNT])    

    @mock.patch("db_utils.DB")
    def test_get_user_obj_from_id(self, mocked_db):
        """ Test the user's info based on id """
        for test in self.test_login_info:
            response = db_utils.get_user_obj_from_id(test[KEY_ID],True)
            expected = test[KEY_EXPECTED]
            
            db_utils.get_user_obj_from_id(response)
            mocked_db.session.commit.assert_called()

        self.assertNotEqual(response, expected[KEY_ID])
    
    @mock.patch("db_utils.DB")
    def test_get_all_user_objs(self, mocked_db):
        """ Test all the users' login info in the database """
        for test in self.test_login_info:
            response = db_utils.get_all_user_objs(False)
            expected = test[KEY_EXPECTED]
            
            db_utils.get_all_user_objs(response)
            mocked_db.session.commit.assert_called()

        self.assertNotEqual(len(response), len(expected[KEY_UCID]))
        self.assertFalse(response)
        
    @mock.patch("db_utils.DB")
    def test_get_all_room_objs(self, mocked_db):
        """ Test the room for availability """
        for test in self.test_room_info:
            response = db_utils.get_all_room_objs()
            expected = test[KEY_EXPECTED]
            
            db_utils.get_all_room_objs(response)
            mocked_db.session.commit.assert_called()
        
        self.assertIsNot(response, expected[KEY_CAPACITY])
        
    @mock.patch("db_utils.DB")
    def test_get_room_obj_by_id(self, mocked_db):
        """ Test the room based on the id given """
        for test in self.test_room_info:
            response = db_utils.get_room_obj_by_id(test[KEY_ID], False)
            expected = test[KEY_EXPECTED]
            
            db_utils.get_room_obj_by_id(response)
            mocked_db.session.commit.assert_called()
        
        self.assertIsNotNone(response)
        self.assertNotEqual(response, expected[KEY_SIZE])
       
    @mock.patch("db_utils.DB")
    def test_get_number_of_rooms(self, mocked_db):
        """ Test the number of rooms availabile """
        for test in self.test_room_info:
            response = db_utils.get_number_of_rooms()
            expected = test[KEY_EXPECTED]
            
            db_utils.get_number_of_rooms()
            mocked_db.session.commit.assert_called()
        
        self.assertNotEqual(len(response), expected[KEY_CAPACITY])
        self.assertNotEqual(len(response), expected[KEY_ROOM_NUM])
        
    @mock.patch("db_utils.DB")
    def test_get_available_room_ids_for_date(self, mocked_db):
        """ Test the room's availability based on date """
        for test in self.test_date_info:
            response = db_utils.get_available_room_ids_for_date(test[KEY_DATE])
            expected = test[KEY_EXPECTED]
            
            db_utils.get_available_room_ids_for_date(test[KEY_DATE])
            mocked_db.session.commit.assert_called()
            
        self.assertEqual(response[9], expected[KEY_TIME][9])
        
    @mock.patch("db_utils.DB")
    def test_get_available_times_for_date(self, mocked_db):
        """ Test the given date """
        for test in self.test_date_info:
            response = db_utils.get_available_times_for_date(test[KEY_DATE])
            expected = test[KEY_EXPECTED]
            
            db_utils.get_available_times_for_date(test[KEY_DATE])
            mocked_db.session.commit.assert_called()
            
        self.assertEqual(response[9], len(expected[KEY_TIME][9]))
        self.assertNotEqual(response[13], len(expected[KEY_TIME][15]))
        
    def test_init(self):
        """ Test if the database is being initialize at the beginning """
        with mock.patch("db_instance.init_db", self.mocked_db):
            response = db_instance.init_db(app)

        self.assertTrue(response)
        
    def on_date_availability_request(self):
        """ Test availability being sent from client """
        for test in self.test_date_info:
            with mock.patch("app.on_date_availability_request", self.mocked_date):
                data = {'DATE_KEY': '11-11-2020'}
                response = app.on_date_availability_request(data)
                expected = test[KEY_EXPECTED]
            
            self.assertNotEqual(response, expected)
            
    def on_reservation_submit(self):
        """ Test reservation availability being sent from client """
        for test in self.test_room_info:
            with mock.patch("app.on_date_availability_request", self.mocked_date):
                data = {'DATE_KEY': '11-11-2020'}
                response = app.on_reservation_submit(data)
                expected = test[KEY_EXPECTED]
            
            self.assertEqual(response, expected)
            
            
if __name__ == "__main__":
    unittest.main()