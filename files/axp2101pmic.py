rename_process("axp2101pmic")
vr("opts", be.api.xarg())
vr("i2c", be.devices["i2c"][0])
if "i" in vr("opts")["o"]:
    be.based.run("mknod AXP2101")
    from axp2101 import AXP2101
    vr("axp", AXP2101(vr("i2c")))
    be.devices["AXP2101"][0] = vr("axp")
    del AXP2101
    dmtex("Registed /dev/AXP2101_0 Power Management device")
    vr("axp")._aldo1_voltage_setpoint = 3300
    vr("axp")._bldo1_voltage_setpoint = 0
    vr("axp")._bldo2_voltage_setpoint = 3300
    vr("axp")._aldo1_voltage_setpoint = 3300
    dmtex("Configured /dev/AXP2101_0 LDOs")
    if vr("axp")._read_register8(39) != 31:
        vr("axp")._write_register8(39, 31) # 2s on time, 10s off time
        dmtex("Reconfigured /dev/AXP2101_0 Control registers")
    else:
        dmtex("/dev/AXP2101 registers validated")
    be.api.setvar("return", "0")
elif "d" in vr("opts")["o"]:
    be.based.run("rmnod AXP2101_0")
    be.api.setvar("return", "0")
else:
    term.write("Usage:\n    axp2101pmic -i\n    axp2101pmic -d")
