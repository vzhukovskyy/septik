import getpass
import simulated
import hardware


def get_data():
    if getpass.getuser() == 'pi':
        return hardware.get_data()
    else:
        return simulated.get_data()
