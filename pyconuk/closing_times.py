import datetime

# Configure the BST timezone
bst = datetime.timezone(datetime.timedelta(hours=1))


def get_closing_time(env, name):
    """
    Generate a closing time with the given env or set a default.

    We set various closing times for this application (Badge editing, CfP,
    etc).  This function allows us to set an environment variable in Production
    while defaulting back to now + 1h for local development without cluttering
    the settings file with that logic.

    We want configuration in the environment to be readable so we will use
    ISO8601 formatted datetimes there, e.g. 2018-10-28T11:34:45+00:00
    """
    value = env.str(name, default=None)

    if value is None:
        # return a default of today + 100 days
        return datetime.datetime.now(tz=bst) + datetime.timedelta(days=100)

    # parse the given config value, setting the timezone info.
    return datetime.datetime.strptime(value, "%Y-%m-%dT%H:%M:%S%z")
