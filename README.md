# GCSData
for showing the data using QThread

# Components

1.  Imports: 
   -   sys  ,   time  : Standard Python modules.
   -   pymavlink.mavutil  : For handling MAVLink messages.
   -   PyQt5.QtWidgets  : For creating the GUI components.
   -   PyQt5.QtCore  : For threading and signals/slots mechanism.

2.    GCSData   Class: 
   -  Inherits from   QMainWindow  :  This is the main window of the PyQt5 application.
   -    __init__   Method: 
     - Initializes the   QMainWindow   and sets up the GUI with   setUI()  .
     - Initializes the   MavData   thread and connects its signal to the   update_labels   method. Starts the thread.
   -    setUI   Method: 
     - Sets the window title and size.
     - Creates and positions   QLabel   widgets for displaying airspeed, groundspeed, yaw, and heading.
   -    update_labels   Method: 
     - Updates the labels with the received MAVLink data.
     - Converts airspeed from meters per second to kilometers per hour (multiplying by 3.6).
   -    closeEvent   Method: 
     - Ensures that the thread is properly stopped and cleaned up when the window is closed.

3.    MavData   Class: 
   -  Inherits from   QThread  :  This runs in a separate thread to handle MAVLink data reception without blocking the UI.
   -    __init__   Method: 
     - Initializes connection parameters and sets up the connection string.
     - Defines a flag   running   to control the thread's operation.
   -    run   Method: 
     - Establishes a MAVLink connection using the provided connection string.
     - Continuously receives MAVLink messages and emits a signal with the data if the message type is   VFR_HUD  .
     - Catches and prints exceptions to handle errors.
   -    stop   Method: 
     - Sets the   running   flag to   False   to stop the thread's loop.

4.  Main Application Execution: 
   -    if __name__ == "__main__":   :
     - Ensures that the code only runs when executed directly, not when imported as a module.
   -  Create and run the application: 
     - Creates a   QApplication   instance.
     - Creates and shows the   GCSData   window.
     - Enters the application’s main event loop with   app.exec_()  .

# Flow of Execution

1.  Initialization: 
   -   GCSData   is instantiated with the IP address and port for the MAVLink connection.
   - The   MavData   thread is started to handle data reception.

2.  GUI Setup: 
   -   GCSData   sets up the UI with labels to display the data.

3.  Data Reception: 
   -   MavData   runs in a separate thread, continuously receiving MAVLink messages.
   - When a   VFR_HUD   message is received, it emits the   data_received   signal.

4.  Updating UI: 
   - The   update_labels   method in   GCSData   receives the signal and updates the GUI labels with the received data.

5.  Shutdown: 
   - When the user closes the application window, the   closeEvent   method ensures the thread is stopped and cleaned up.

# Summary

This script creates a PyQt5 application to visualize MAVLink VFR_HUD data. It utilizes threading to handle data reception separately from the UI to keep the interface responsive. The   MavData   class handles the connection and data processing, while the   GCSData   class manages the user interface and updates it with the received data.
