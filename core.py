#!/usr/bin/env python3
import subprocess
import datetime
import time
from functools import partial


def execute(cmd):
    with subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        universal_newlines=True,
        text=True,
        close_fds=True,
        shell=True,
    ) as proc:
        for line in iter(proc.stdout.readline, b""):
            yield line
            if (r := proc.poll()) is not None:
                if r != 0:
                    raise subprocess.CalledProcessError(r, cmd)
                break


def wait_until(end: datetime.datetime) -> None:
    while True:
        diff = (end - datetime.datetime.now()).total_seconds()
        if diff <= 0.1:
            return
        time.sleep(diff / 2)


def time_tomorrow(hour: int, minute: int, second: int) -> datetime.datetime:
    alarm_time = datetime.datetime.now().replace(
        hour=hour, minute=minute, second=second, microsecond=0
    )
    if alarm_time <= datetime.datetime.now():
        alarm_time += datetime.timedelta(hours=24)

    return alarm_time


def wake(device: str, music_dir: str):
    print("mez-chan: wake up sleepy head!")
    query = f"mpv --audio-device={device} {music_dir}"
    for line in execute(query):
        print(line, end="")

while True:
    wait_until(time_tomorrow(9, 0, 0))
    wake(
        "pulse/alsa_output.usb-BEHRINGER_UMC204HD_192k-00.analog-surround-40",
        "/media/music/Pink\\ Floyd/",
    )
