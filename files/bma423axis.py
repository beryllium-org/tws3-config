rename_process("bma423axis")
vr("opts", be.api.xarg())
vr("i2c", be.devices["i2c"][0])
if "i" in vr("opts")["o"]:
    try:
        from bma423 import BMA423
        vr("bma", BMA423(vr("i2c")))
        be.based.run("mknod BMA423")
        vr("node", be.api.getvar("return"))
        be.api.subscript("/bin/stringproccessing/devid.py")
        vr("bma").acc_range = 3
        be.devices["BMA423"][vr("dev_id")] = vr("bma")
        del BMA423
        dmtex("Created BMA423 sensor")
        class temp:
            def __init__(self, bma):
                self._bma = bma

            @property
            def name(self) -> str:
                return "BMA423-Temp0"
            @property
            def temperature(self) -> float:
                return float(self._bma.temperature)

        be.based.run("mknod temp")
        vr("node", be.api.getvar("return"))
        be.api.subscript("/bin/stringproccessing/devid.py")
        be.devices["temp"][vr("dev_id")] = temp(vr("bma"))
        del temp
        dmtex("Temperature sensor registered at /dev/temp" + str(vr("dev_id")))
    except:
        dmtex("Failed to create BMA423 sensor!")
        try:
            del BMA423
        except NameError:
            pass
    be.api.setvar("return", "0")
elif "d" in vr("opts")["o"]:
    be.based.run("rmnod BMA423_0")
    be.based.run("rmnod temp0")
    be.api.setvar("return", "0")
else:
    term.write("Usage:\n    axp2101pmic -i\n    axp2101pmic -d")
