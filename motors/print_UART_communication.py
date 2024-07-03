import pandas as pd

# df = pd.read_csv("./motors/U13C_UART_WITH_MOTOR.csv", keep_default_na=False)
df = pd.read_csv("./motors/U13C_UART_NO_MOTOR.csv", keep_default_na=False)
df = pd.read_csv("./motors/U13C_UART_WITH_MOTOR_MANUAL_BRAKING.csv", keep_default_na=False)

currentChannel = df.values[0][0]
print(f"{currentChannel}: ", end="")
for row in df.values:
  if row[-1] == "":
    if row[0] == currentChannel:
      print(row[-2][2:], end="")
    else:
      print("", end="\n")
      print(f"{row[0]}: ", end="")
      print(row[-2][2:], end="")
    currentChannel = row[0]

print("", end="\n")