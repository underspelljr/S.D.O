from app.services import user_service
from app.schemas.user import UserCreate

def test_create_user(db_session):
    """
    Unit test for the create_user service function.
    """
    user_in = UserCreate(name="testuser")
    user = user_service.create_user(db=db_session, user_create=user_in)
    
    assert user.name == user_in.name
    assert user.id is not None
    assert user.uuid is not None

def test_get_all_users(db_session):
    """
    Unit test for retrieving all users.
    """
    user_in1 = UserCreate(name="testuser1")
    user_in2 = UserCreate(name="testuser2")
    user_service.create_user(db=db_session, user_create=user_in1)
    user_service.create_user(db=db_session, user_create=user_in2)

    users = user_service.get_all_users(db=db_session)
    assert len(users) == 2
    assert users[0].name == "testuser1"
    assert users[1].name == "testuser2"