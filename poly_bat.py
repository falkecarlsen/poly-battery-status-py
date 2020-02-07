import re
from enum import Enum
from pathlib import Path
from pprint import pprint

PSEUDO_FS_PATH = "/sys/class/power_supply/"
CURRENT_CHARGE_FILENAME = "energy_now"
MAX_CHARGE_FILENAME = "energy_full"
POWER_DRAW_FILENAME = "power_now"
TLP_THRESHOLD_PERCENTAGE = 0.8


class Status(Enum):
    CHARGING = 1
    DISCHARGING = 2
    PASSIVE = 3


class Configuration:
    time_to_completion: int
    percentage: float
    status: Status

    def __init__(self, time_to_completion, percentage, status):
        self.time_to_completion = time_to_completion
        self.percentage = percentage
        self.status = status


class Battery:
    status: Status
    current_charge: int
    max_charge: int
    power_draw: int

    def __init__(self, status, current_charge, max_charge, power_draw):
        self.Status = status
        self.current_charge = current_charge
        self.max_charge = max_charge
        self.power_draw = power_draw


def get_configuration() -> Configuration:
    # get all batteries on system
    batteries = []
    for x in Path(PSEUDO_FS_PATH).iterdir():
        bat_name = str(x.parts[len(x.parts) - 1])
        if re.match("^BAT\d+$", bat_name):
            print(bat_name)
            batteries.append(Battery(
                get_status(bat_name),
                get_current_charge(bat_name),
                get_max_charge(bat_name),
                get_power_draw(bat_name)))

    # calculate global status, assumes that if a battery is not passive, it will be discharging or charging
    config_status = Status.PASSIVE
    for bat in batteries:
        if bat.Status == Status.CHARGING:
            config_status = Status.CHARGING
            break
        elif bat.Status == Status.DISCHARGING:
            config_status = Status.DISCHARGING
            break

    # construct and return configuration
    return Configuration(calc_time(batteries, config_status), calc_percentage(batteries), config_status)


def get_status(bat_name: str) -> Status:
    raw_status = Path(f"{PSEUDO_FS_PATH}{bat_name}/status").open().read().strip()
    print(raw_status)
    if raw_status == "Unknown" or raw_status == "Full":
        return Status.PASSIVE
    elif raw_status == "Charging":
        return Status.CHARGING
    elif raw_status == "Discharging":
        return Status.DISCHARGING
    else:
        raise ValueError


def get_current_charge(bat_name: str) -> int:
    return int(Path(f"{PSEUDO_FS_PATH}{bat_name}/{CURRENT_CHARGE_FILENAME}").open().read().strip())


def get_max_charge(bat_name: str) -> int:
    return int(Path(f"{PSEUDO_FS_PATH}{bat_name}/{MAX_CHARGE_FILENAME}").open().read().strip())


def get_power_draw(bat_name: str) -> int:
    return int(Path(f"{PSEUDO_FS_PATH}{bat_name}/{POWER_DRAW_FILENAME}").open().read().strip())


def calc_time(batteries: list, status: Status) -> int:
    if status == Status.PASSIVE:
        return 0
    # get total metrics on configuration
    total_current_charge = sum([bat.current_charge for bat in batteries])
    total_max_charge = sum([bat.max_charge for bat in batteries])
    total_power_draw = sum([bat.power_draw for bat in batteries])
    print_status(total_current_charge)
    if status == Status.DISCHARGING:
        # return number of seconds until empty
        return (total_current_charge / total_power_draw) * 3600
    elif status == Status.CHARGING:
        # return number of seconds until (optionally relatively) charged
        return (((total_max_charge * TLP_THRESHOLD_PERCENTAGE) - total_current_charge) / total_power_draw) * 3600


def calc_percentage(batteries: list) -> float:
    total_max_charge = sum([bat.max_charge for bat in batteries])
    total_current_charge = sum([bat.current_charge for bat in batteries])
    return total_current_charge / total_max_charge


def calc_display_time() -> str:
    pass


def print_status(config: Configuration):
    pass


def main():
    config = get_configuration()
    pprint(config)


if __name__ == '__main__':
    main()
