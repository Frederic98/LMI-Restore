# LMI-Restore

This is the github repository for the LMI re-store project at the Mechatronics lab at Fontys.

To run the software:
1. Start the server `python3 LMI_Server/server.py`
2. Start the client `python3 LMI_GUI/main.py`

The motion controller is programmed with Mbed: https://os.mbed.com/users/Frederic98/code/LMI_restore_V2/.  
The host talks to it using [g-code](https://reprap.org/wiki/G-code). It uses the existing codes where possible (G0/G1 to move to a position, G28 to home...) or a custom code when this doesn't exist yet. (M200 to set the velocity for an axis. Normally, this is done with Fxxx in a G0/G1 command to set the total velocity of all axes combined when they are all synchronized. This, however, is not the case in this project, so another command had to be added to set the velocity of a specific axis)

Initially, the G-code was sent over the ethernet interface to the nucleo. This, however, seemed a bit unstable with the connection dropping after a couple of commands.
For this reason, it was replaced by the USB UART port (available at the programming USB connector).
