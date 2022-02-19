"""class for the Wifi and MQTT settings"""


from PySide6.QtWidgets import QDialog, QCheckBox, QFormLayout, QLineEdit, QDialogButtonBox

import meshtastic.serial_interface
from meshtastic.__init__ import BROADCAST_ADDR
from meshtastic.__main__ import setPref


class Wifi_and_MQTT_Form(QDialog):
    """wifi and mqtt form"""

    def __init__(self, parent=None):
        """constructor"""
        super(Wifi_and_MQTT_Form, self).__init__(parent)

        self.parent = parent

        width = 500
        height = 200
        self.setMinimumSize(width, height)
        self.setWindowTitle("Wifi & MQTT Settings")

        self.port = None
        self.interface = None
        self.prefs = None

        # Create widgets

        # WiFi
        self.wifi_ap_mode = QCheckBox()
        self.wifi_ssid = QLineEdit()
        self.wifi_password = QLineEdit()

        # MQTT
        self.mqtt_disabled = QCheckBox()
        self.mqtt_server = QLineEdit()
        self.mqtt_username = QLineEdit()
        self.mqtt_password = QLineEdit()

        # Add a button box
        self.button_box = QDialogButtonBox()
        self.button_box.setStandardButtons(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)


        # create form
        form_layout = QFormLayout()
        form_layout.addRow(self.tr("Enable Wifi AP"), self.wifi_ap_mode)
        form_layout.addRow(self.tr("Wifi SSID"), self.wifi_ssid)
        form_layout.addRow(self.tr("Wifi Password"), self.wifi_password)
        form_layout.addRow(self.tr("MQTT Disabled"), self.mqtt_disabled)
        form_layout.addRow(self.tr("MQTT Server"), self.mqtt_server)
        form_layout.addRow(self.tr("MQTT Username"), self.mqtt_username)
        form_layout.addRow(self.tr("MQTT Password"), self.mqtt_password)
        form_layout.addRow(self.tr(""), self.button_box)
        self.setLayout(form_layout)


    def run(self, port=None, interface=None):
        """load the form"""
        self.port = port
        self.interface = interface
        print(f'port:{port}')
        if self.port:
            print(f'using port:{self.port}')
            self.get_prefs()
            print(f'prefs:{self.prefs}')
            if self.prefs.wifi_ap_mode and self.prefs.wifi_ap_mode is True:
                self.wifi_ap_mode.setChecked(True)
            if self.prefs.wifi_ssid:
                self.wifi_ssid.setText(self.prefs.wifi_ssid)
            else:
                self.wifi_ssid.setText("")
            if self.prefs.wifi_password:
                self.wifi_password.setText(self.prefs.wifi_password)
            else:
                self.wifi_password.setText("")
            if self.prefs.mqtt_disabled and self.prefs.mqtt_disabled is True:
                self.mqtt_disabled.setChecked(True)
            if self.prefs.mqtt_server:
                self.mqtt_server.setText(self.prefs.mqtt_server)
            else:
                self.mqtt_server.setText("")
            if self.prefs.mqtt_username:
                self.mqtt_username.setText(self.prefs.mqtt_username)
            else:
                self.mqtt_username.setText("")
            if self.prefs.mqtt_password:
                self.mqtt_password.setText(self.prefs.mqtt_password)
            else:
                self.mqtt_password.setText("")
            self.show()


    def get_prefs(self):
        """Get preferences from device"""
        try:
            if self.interface is None:
                print('interface was none?')
                self.interface = meshtastic.serial_interface.SerialInterface(devPath=self.port)
            if self.interface:
                self.prefs = self.interface.getNode(BROADCAST_ADDR).radioConfig.preferences
        except Exception as e:
            print(f'Exception:{e}')


    def write_prefs(self):
        """Write preferences to device"""
        try:
            if self.interface:
                print("Writing modified preferences to device")
                prefs = self.interface.getNode(BROADCAST_ADDR).radioConfig.preferences
                setPref(prefs, 'wifi_ap_mode', f'{self.wifi_ap_mode.isChecked()}' )
                setPref(prefs, 'wifi_ssid', self.wifi_ssid.text())
                setPref(prefs, 'wifi_password', self.wifi_password.text())
                setPref(prefs, 'mqtt_disabled', f'{self.mqtt_disabled.isChecked()}' )
                setPref(prefs, 'mqtt_server', self.mqtt_server.text())
                setPref(prefs, 'mqtt_username', self.mqtt_username.text())
                setPref(prefs, 'mqtt_password', self.mqtt_password.text())
                self.interface.getNode(BROADCAST_ADDR).writeConfig()
        except Exception as e:
            print(f'Exception:{e}')


    def reject(self):
        """Cancel without saving"""
        print('CANCEL button was clicked')
        self.parent.my_close()


    def accept(self):
        """Close the form"""
        print('SAVE button was clicked')
        self.write_prefs()