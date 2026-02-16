import serial
import time

SUBTITLES = "SUB"
NAVIGATE_UP = "NUP"
NAVIGATE_LEFT = "NLT"
NAVIGATE_RIGHT = "NRT"
NAVIGATE_DOWN = "NDN"
NAVIGATE_CONFIRM = "SEL"
PAUSE = "PAU"
PLAY = "PLA"
OSD = "OSD"
STOP = "STP"
POWER_ON = "PON"
POWER_OFF = "POF"
MUTE = "MUT"
NEXT_TRACK = "NXT"
PREVIOUS_TRACK = "PRE"
FAST_FORWARD = "FWD"
REWIND = "REV"

SUBS_ENGLISH = [SUBTITLES, NAVIGATE_DOWN, NAVIGATE_CONFIRM, SUBTITLES]

class MagnetarApi:

    def __init__(
            self,
            host: str,
            port: int,
            baud_rate: int
    ):
        self.url = f"socket://{host}:{str(port)}"
        self.baud_rate = baud_rate
        self.expected_resp = "ack\r\n".encode()

    def send_command(self, command_list: list[str]) -> list[str]:

        resp = []

        with serial.serial_for_url(
                url=self.url,
                stopbits=1,
                bytesize=8,
                baudrate=self.baud_rate,
                timeout=1
        ) as ser:

            for c in command_list:
                command = "#{0}\r\n".format(c)
                b = command.encode()
                ser.write(b)
                resp.append(ser.readline().decode())
                time.sleep(0.4)

        return resp