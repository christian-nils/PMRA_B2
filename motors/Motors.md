# Motor control

A digital signal analyser was used to capture the Serial communication between U13C and the main MCU (U2). There are three captures: 1) one with the motor disconnected, 2) one with the motor connected, and 3) one where the motor was turning and the wheel was held two times to try braking it. This is when running the factory test.

The sal captures need to be opened with Saleae's [Logic](https://www.saleae.com/pages/downloads) software.

Some very valuable information (about message types, flags, etc.) was found by [Nekraus](https://github.com/nekraus) and posted on Discord.

## Motor IDs

- right: `0b00` or `0x00`
- left: `0b01` or `0x01`
- middle(a.k.a blade): `0b11` or `0x03`

## Commands

### Main MCU

Buffer format

`header[1] header[0] motor_id data[3] cmd_id data[2] checksum data[1] 00 data[0] 00`


#### Command types (`cmd_id`):

- `msg_id == 0x02`: set motor speed


#### Data buffer

| `cmd_id`      | data[3]     | data[2]     | data[1]     | data[0]     |
| ------------- | ------------- |------------- |------------- |------------- |
| `0x02` | 0x00     | 0x00     | speed[1]     | speed[0]     |


Message example (request speed = `2500 rpm`): `D5 E5 00 00 02 00 4F 09 00 C4 00`

The checksum is calculated as follows:

`checksum = (motor_id + cmd_id + data[3] + data[2] + data[1] + data[0]) & 0x7F`

#### Motor initialization:

1. Main MCU sends one message (`cmd_id=0x04`) followed by a message (`cmd_id=0x00`).
2. Wait for Motor MCU reply (should be a message (`msg_id=0x0b`))
3. Sends one message (`cmd_id=0x01`)
4. Wait for Motor MCU reply (should be a message (`msg_id=0x0b`))
5. Send instructions

Example with the right motor:

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

### Motor MCU

#### General buffer format

`header[1] header[0] motor_id data[3] msg_id data[2] checksum data[1] flags data[0] motor_status`

#### Message types (`msg_id`):

- `msg_id == 0x00`: motor ticks
- `msg_id == 0x02`: motor speed and current
- `msg_id == 0x03`: motor raw current
- `msg_id == 0x04`: motor raw voltage + temperature (?) 
- `msg_id == 0x06`: error message (check `flags` for details)
- `msg_id == 0x0b`: OK (everything is fine)

#### Flags (`flags`):


| **Bit position** | 7 | 6 | 5 | 4 | 3 | 2 | 1 | 0 |
|-|-|-|-|-|-|-|-|-|
| **Meaning** | - | timeout from the main µC | timeout from the main µC | hall sensors shortcut or disconnected | requested speed not reached | - | - | overcurrent |


#### Data buffer

| `msg_id`      | data[3]     | data[2]     | data[1]     | data[0]     |
| ------------- | ------------- |------------- |------------- |------------- |
| `0x00` | ticks[3]     | ticks[2]     | ticks[1]     | ticks[0]     |
| `0x02` | speed[1]     | speed[0]     | current[1]     | current[0]     |


#### Checksum (`checksum`)

The checksum is calculated as follows:

`checksum = (motor_id + msg_id + data[3] + data[2] + data[1] + data[0] + motor_status + flags) & 0x7F` 