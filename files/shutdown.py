rename_process("shutdown-axp2101")
be.io.ledset(1)
be.deinit_consoles()
be.devices["AXP2101"][0].power_off()
