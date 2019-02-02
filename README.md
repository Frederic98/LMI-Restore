# LMI-Restore

This is the github repository for the LMI re-store project at the Mechatronics lab at Fontys.

To run the software:
1. Start the server `python3 LMI_Server/server.py`
2. Start the client `python3 LMI_GUI/main.py`

The motion controller is programmed with Mbed: https://os.mbed.com/users/Frederic98/code/LMI_restore_V2/

Initially, the G-code was sent over the ethernet interface to the nucleo. This, however, seemed a bit unstable with the connection dropping after a couple of commands.
For this reason, it was replaced by the USB UART port (available at the programming USB connector).