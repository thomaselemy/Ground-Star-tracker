import tkinter as tk
import tkinter.ttk as ttk
import serial.tools.list_ports
import serial
# --- functions ---
#port = event.widget.get()
def serial_ports():
    return [p.device for p in serial.tools.list_ports.comports()]


# when the user selects one serial port from the combobox, this function will execute
def on_select(event=None):
    global ser
    COMPort = cb.get()
    string_separator = "-"
    COMPort = COMPort.split(string_separator, 1)[0]  # remove everything after '-' character
    #COMPort = COMPort[:-1]  # remove last character of the string (which is a space)
    ser = serial.Serial(port=COMPort, baudrate=9600, timeout=0)
    # readSerial() #start reading shit. DELETE. later to be placed in a button
    # get selection from event
    # print("event.widget:", event.widget.get())
    # or get selection directly from combobox
    print("opened port")

    print(COMPort)

    # ser = Serial(serialPort , baudRate, timeout=0, writeTimeout=0) #ensure non-blocking

# --- main ---

root = tk.Tk()

cb = ttk.Combobox(root, values=serial_ports())
cb.pack()
# assign function to combobox
cb.bind('<<ComboboxSelected>>', on_select)
#port = event.widget.get()
#SerialObj = serial.Serial(str(port), 9600) #open serial port
root.mainloop()