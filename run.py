from dingdongditch import trigger, user_settings


if __name__ == '__main__':
    # bootstrap user data watching
    user_settings.get_data()
    trigger.run()
