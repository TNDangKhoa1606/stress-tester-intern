from locust import events

@events.init.add_listener
def on_locust_init(environment, **kwargs):
    """
    Adds custom arguments to the Locust parser.
    These arguments can be set via command-line, environment variables, or a config file.
    """
    environment.parser.add_argument(
        "--username",
        type=str,
        env_var="LOCUST_USERNAME",
        default="alice",
        help="Username for login"
    )
    environment.parser.add_argument(
        "--password",
        type=str,
        env_var="LOCUST_PASSWORD",
        default="alice123",
        help="Password for login"
    )
