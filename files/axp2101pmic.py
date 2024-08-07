rename_process("axp2101pmic")
vr("opts", be.api.xarg())
from axp2101 import AXP2101

vr("i2c", be.devices["i2c"][0])
if "i" in vr("opts")["o"]:
    be.based.run("mknod AXP2101")
    be.devices["AXP2101"][0] = AXP2101(vr("i2c"))
    be.api.setvar("return", "0")
elif "d" in vr("opts")["o"]:
    be.based.run("rmnod AXP2101_0")
    be.api.setvar("return", "0")
else:
    term.write("Usage:\n    axp2101pmic -i\n    axp2101pmic -d")
del AXP2101
