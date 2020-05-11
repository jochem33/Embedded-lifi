# import serial
# s = serial.Serial(port='/dev/tty.usbmodemfa141', baudrate=9600)

# s.write('text')
# s.read()
# s.readline()





import sys, os, fcntl, FCNTL, termios, TERMIOS
...

##################################################################
# Establish a serial-port connection w. required settings.
##################################################################
def openSerial(self, portName="/dev/term/a"):
    # The open attempt may fail on account of permissions or on
    # account of somebody's already using the port.
    # Pass such exceptions on to our client.
    try:
        # You probably just want to use the builtin open(), here...
        fd = os.open(portName, FCNTL.O_RDWR, 0)

        # Set up symbolic constants for the list elements returned by
        # tcgetattr.
        [iflag, oflag, cflag, lflag, ispeed, ospeed, cc] = range(7)

        # Set the port baud rate, etc.
        settings = termios.tcgetattr(fd)
        # Set the baud rate.
        settings[ospeed] = TERMIOS.B9600 # Output speed
        settings[ispeed] = TERMIOS.B0    # Input speed (B0 => match output)
        # Go for 8N1 with hardware handshaking.
        settings[cflag] = (((settings[cflag] & ~TERMIOS.CSIZE) |
                            TERMIOS.CS8) & ~TERMIOS.PARENB)
        # NOTE:  This code relies on an UNDOCUMENTED
        # feature of Solaris 2.4. Answerbook explicitly states
        # that CRTSCTS will not work.  After much searching you
        # will discover that termiox ioctl() calls are to
        # be used for this purpose.  After reviewing Sunsolve
        # databases, you will find that termiox's TCGETX/TCSETX
        # are not implemented.  *snarl*
        settings[cflag] = settings[cflag] | TERMIOS.CRTSCTS
        # Don't echo received chars, or do erase or kill input processing.
        settings[lflag] = (settings[lflag] &
                            ~(TERMIOS.ECHO | TERMIOS.ICANON))
        # Do NO output processing.
        settings[oflag] = 0

        # When reading, always return immediately, regardless of
        # how many characters are available.
        settings[cc][TERMIOS.VMIN] = 0
        settings[cc][TERMIOS.VTIME] = 0
        
        # Install the modified line settings.
        termios.tcsetattr(fd, TERMIOS.TCSANOW, settings)

        # Set it up for non-blocking I/O.
        fcntl.fcntl(fd, FCNTL.F_SETFL, FCNTL.O_NONBLOCK)

    except os.error, info:
        # If any of this fails, mention the port name in the
        # exception.
        raise os.error, "Can't open %s: %s" % (portName, info))