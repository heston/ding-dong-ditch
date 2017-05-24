from dingdongditch import trigger, user_settings


if __name__ == '__main__':
    # bootstrap user data
    user_settings.init_data()
    # wait for events
    trigger.run()
