# Motor control

A digital signal analyser was used to capture the Serial communication between U13C and the main MCU (U2). There are three captures: 1) one with the motor disconnected, 2) one with the motor connected, and 3) one where the motor was turning and the wheel was held two times to try braking it. This is when running the factory test.

The sal captures need to be opened with Saleae's [Logic](https://www.saleae.com/pages/downloads) software.

## Motor IDs

- right: `0b00` or `0x00`
- left: `0b01` or `0x01`
- middle(a.k.a blade): `0b11` or `0x03`

## Commands

### Main MCU

Buffer format

`header[1] header[0] motor_id 00 command_id 00 checksum speed[1] 00 speed[0] 00`

Example:

`D5 E5 00 00 02 00 4F 09 00 C4 00`

The checksum is calculated as follows:

`checksum = (motor_id + command_id + speed[1] + speed[0]) & 0x7F`

### Motor MCU (right motor)

Buffer format

`header[1] header[0] motor_id? speed[1] command_id? speed[0] checksum current[1] 00 current[0] motor_status?`

Example:

`D5 E5 00 09 02 91 55 00 00 37 02`

The checksum is calculated as follows:

`checksum = (motor_id + speed[1] + command_id + speed[0] + motor_status + current[1] + current[0]) & 0x7F`

I am not yet sure about the `motor_id`, `command_id`, and `motor_status`. As the following is reported when no motor is connected:

`D5 E5 00 00 06 00 1B 00 10 00 05`

## Initialize motor

Main MCU:

```
D5E5000004000400000000
D5E5000000000000000000
```

Motor MCU's reply (if everything is fine):

```
D5E500000B000D00000002
```

Then, Main MCU sends:

```
D5E5000001000100000000
```

Motor MCU's reply (if everything is fine):

```
D5E500000B000D00000002
```

After what, the Main MCU can send commands.
