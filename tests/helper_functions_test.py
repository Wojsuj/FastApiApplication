from functional_module import helper_functions
import pytest
from app import models
from fastapi import HTTPException
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import numpy as np
import cv2

#Connect to test databases
SQLALCHEMY_DATABASE_URL = "sqlite:///./tests/test_databases/test_database.db"
SQLALCHEMY_DATABASE_EMPTY_URL = "sqlite:///./tests/test_databases/empty_test_database.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
engine_empty = create_engine(SQLALCHEMY_DATABASE_EMPTY_URL)

SessionTest = sessionmaker(bind=engine)
SessionTestEmpty = sessionmaker(bind=engine_empty)

test_image_path = "tests/images/test.jpg"
#Tests

#get_thumbnail_size function tests:

def test_get_thumbnail_size_should_return_tuple():
    text = "50x50"
    returned_tuple = helper_functions.get_thumbnail_size(size = text)
    assert not type(returned_tuple) is not tuple, "Returned type is not a tuple"

def test_get_thumbnail_size_should_return_int():
    errors = []
    text = "50x50"
    width, height = helper_functions.get_thumbnail_size(size = text)
    if type(width) is not int: errors.append("Width is not an int")
    if type(height) is not int: errors.append("Height is not an int")
    assert not errors, "Errors occured:\n{}".format("\n".join(errors))

def test_get_thumbnail_size_should_not_pass_in_wrong_format():
    text = "5000"
    with pytest.raises(HTTPException):
        helper_functions.get_thumbnail_size(size= text)


#get_random_id function tests:

def test_random_id_should_return_int():
    session = SessionTest()
    item = models.Image
    random_id = helper_functions.get_random_id(db = session, item = item)
    assert not type(random_id) is not int, "random_id is not an int"

def test_random_id_should_not_pass_empty_database():
    session = SessionTestEmpty()
    item = models.Image
    with pytest.raises(HTTPException):
        helper_functions.get_random_id(db = session, item = item)


#read_image function tests:

def test_read_image_should_return_image():
    image = helper_functions.read_image(image_path=test_image_path)
    assert not type(image) is not np.ndarray, "Returned image is not nd.array"

def test_read_image_should_not_pass_wrong_type():
    test_image_path = None
    with pytest.raises(HTTPException):
        image = helper_functions.read_image(image_path=test_image_path)


#resize_image function tests:

def test_resize_image_should_not_enlarge_thumbnail():
    test_image = cv2.imread(test_image_path)
    with pytest.raises(HTTPException):
        resized_image = helper_functions.resize_image(image=test_image, resize_width=1000, resize_height=2000)

def test_resize_image_should_return_image():
    test_image = cv2.imread(test_image_path)
    resized_image = helper_functions.resize_image(image=test_image, resize_width=20, resize_height=20)
    assert not type(resized_image) is not np.ndarray, "Returned image is not nd.array"


#change_image_to_png_format tests:

def test_change_image_to_png_format_should_return_image():

    test_image = cv2.imread(test_image_path)
    png_image = helper_functions.change_image_to_png_format(image = test_image)
    assert not type(png_image) is not np.ndarray, "Returned image is not nd.array"


#load_random_image tests:

def load_random_image_should_return_tuple():
    session = SessionTest()
    size = "50x50"
    returned_tuple = helper_functions.load_random_image(db = session, size = size)
    assert not type(returned_tuple) is not tuple, "Returned type is not a tuple"

def load_random_image_should_return_string_in_tuple():
    session = SessionTest()
    size = "50x50"
    path, image = helper_functions.load_random_image(db = session, size = size)
    assert not type(path) is not str, "Returned type is not a str"

def load_random_image_should_return_image_in_tuple():
    session = SessionTest()
    size = "50x50"
    path, image = helper_functions.load_random_image(db = session, size = size)
    assert not type(image) is not np.ndarray, "Returned type is not a np.ndarray"


#load_image_at_given_path tests:

def load_image_at_given_path_should_return_image():
    size = "50x50"
    path, image = helper_functions.load_image_at_given_path(image_path = test_image_path, size = size)
    assert not type(image) is not np.ndarray, "Returned type is not a np.ndarray"


#get_image_size tests:

def test_get_image_size_should_return_int():
    errors = []
    test_image = cv2.imread(test_image_path)
    width, height = helper_functions.get_image_size(test_image)
    if type(width) is not int: errors.append("Width is not an int")
    if type(height) is not int: errors.append("Height is not an int")
    assert not errors, "Errors occured:\n{}".format("\n".join(errors))

def test_get_image_size_should_return_tuple():
    test_image = cv2.imread(test_image_path)
    returned_tuple = helper_functions.get_image_size(test_image)

    assert not type(returned_tuple) is not tuple, "Returned type is not a tuple"
