from tasks.auth_flows import PrivateUser
from shapes.spike_test import SpikeTest

# By creating a User class that inherits directly from PrivateUser,
# we ensure that only its tasks (login, add_to_cart, checkout, etc.) are run.
class SpikeTestUser(PrivateUser):
    pass
