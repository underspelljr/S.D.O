from app.services import user_service
from app.schemas.user import UserCreate, UserUpdate

def test_create_user(db_session):
    """
    Unit test for the create_user service function.
    """
    user_in = UserCreate(name="testuser")
    user = user_service.create_user(db=db_session, user_create=user_in)
    
    assert user.name == user_in.name
    assert user.id is not None
    assert user.uuid is not None
    assert user.permission_level == 0
    assert user.is_active == True

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

    # Soft delete a user and check if it's returned
    user_service.delete_user(db=db_session, user=users[0])
    users = user_service.get_all_users(db=db_session)
    assert len(users) == 1
    assert users[0].name == "testuser2"

def test_update_user(db_session):
    """
    Unit test for updating a user.
    """
    user_in = UserCreate(name="testuser")
    user = user_service.create_user(db=db_session, user_create=user_in)

    user_update = UserUpdate(permission_level=2)
    updated_user = user_service.update_user(db=db_session, user=user, user_update=user_update)
    assert updated_user.permission_level == 2

def test_delete_user(db_session):
    """
    Unit test for soft deleting a user.
    """
    user_in = UserCreate(name="testuser")
    user = user_service.create_user(db=db_session, user_create=user_in)

    deleted_user = user_service.delete_user(db=db_session, user=user)
    assert deleted_user.is_active == False

def test_approve_user(db_session):
    """
    Unit test for approving a user.
    """
    user_in = UserCreate(name="testuser")
    user = user_service.create_user(db=db_session, user_create=user_in)

    user_update = UserUpdate(permission_level=1)
    approved_user = user_service.update_user(db=db_session, user=user, user_update=user_update)
    assert approved_user.permission_level == 1
