rename_process("init-axp2101-conf")

vr("axp", be.devices["AXP2101"][0])
vr("axp")._aldo1_voltage_setpoint = 3300
vr("axp")._bldo1_voltage_setpoint = 0
vr("axp")._bldo2_voltage_setpoint = 3300
vr("axp")._aldo1_voltage_setpoint = 3300
dmtex("Configured /dev/AXP2101_" + str(vr("dev_id")) + " LDOs")
if vr("axp")._read_register8(39) != 31:
    vr("axp")._write_register8(39, 31) # 2s on time, 10s off time
    dmtex("Reconfigured /dev/AXP2101_" + str(vr("dev_id")) + " Control registers")
else:
    dmtex("/dev/AXP2101_" + str(vr("dev_id")) + " registers validated")

class battery:
    def __init__(self, pmic):
        self._pmic = pmic

    @property
    def voltage(self) -> float:
        return (
            (self._pmic.battery_voltage / 1000)
            if self._pmic.is_battery_connected
            else 0.0
        )

    @property
    def percentage(self) -> int:
        return max(
            0,
            min(
                100, self._pmic.battery_level if self._pmic.is_battery_connected else 0
            ),
        )

    @property
    def charger(self) -> bool:
        return

    @property
    def status(self) -> bool:
        if not self._pmic.is_battery_connected:
            return "disconnected"
        if self._pmic.battery_status.value == 3:
            return "charging"
        elif self._pmic.battery_status.value == 2:
            return "charged"
        else:
            return "discharging"

    @property
    def charging_enabled(self) -> bool:
        return self._pmic.battery_charging_enabled

    @charging_enabled.setter
    def charging_enabled(self, value: bool) -> None:
        self._pmic.battery_charging_enabled = value


be.based.run("mknod bat")
vr("node", be.api.getvar("return"))
be.api.subscript("/bin/stringproccessing/devid.py")
be.devices[vr("dev_name")][vr("dev_id")] = battery(vr("axp"))
del battery
dmtex("Battery sensor registered at /dev/" + vr("dev_name") + str(vr("dev_id")))
