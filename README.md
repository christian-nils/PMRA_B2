# Parkside PMRA B2

Some notes written when investigating the mainboard of the Parkside B2 lawnmower. The mainboard version is `SF8B101_Main_v1.7`, with the design date `2023.07.05`.

Much more advanced work on the Parkside PMRA can be found on https://github.com/Nekraus/PARKSIDE_PMRA and https://github.com/sven337/ParksideRobomower/wiki. 

# Communication with the main MCU (U2)

## U2 connector: for SWD debug

	green: SWDIO
	yellow: SWCLK
	red: 3.3V
	black: GND

You'll need to supply 3.3V to the MCU to be able to communicate with it. One way is to use the 3.3V line from the UART1 port.