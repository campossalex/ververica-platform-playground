import configparser


def get_configs():
    config = configparser.ConfigParser()
    config.read("/root/ververica-platform-playground/datagen/configuration/configuration.ini")

    bootstrap_servers = config["KAFKA"]["bootstrap_servers"]

    configs = {"bootstrap_servers": bootstrap_servers}

    print("configs: {0}".format(str(configs)))

    return configs
