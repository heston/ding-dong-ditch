from dingdongditch import trigger, user_settings


if __name__ == '__main__':
    # bootstrap user data watching
    user_settings.init_data()
    trigger.run()
