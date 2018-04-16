import getpass


if getpass.getuser() == 'pi':
    import hardware
    module = hardware
else:
    import simulated
    module = simulated


def get_data():
    return module.get_data()
