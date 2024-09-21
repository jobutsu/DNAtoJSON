import os
import json
import maya.cmds as cmds
import maya.OpenMayaUI as omui
from PySide2 import QtWidgets, QtCore
from shiboken2 import wrapInstance
from dna import (
    DataLayer_All,
    DataLayer_Behavior,
    DataLayer_Definition,
    DataLayer_Geometry,
    DataLayer_Descriptor,
    DataLayer_AllWithoutBlendShapes,
    FileStream,  # File stream for reading/writing DNA files
    Status,  # Class to check the status of the process
    BinaryStreamReader,  # Binary reader for DNA files
    JSONStreamWriter  # JSON writer for DNA files
)


# Helper function to get Maya's main window
def get_maya_main_window():
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(int(main_window_ptr), QtWidgets.QWidget)


class DNAConverterApp(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(DNAConverterApp, self).__init__(parent)
        self.setWindowTitle('DNA to JSON Converter')
        self.setGeometry(300, 300, 400, 150)

        # Create the layout and central widget
        central_widget = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(central_widget)

        # DNA file selection
        self.file_label = QtWidgets.QLabel('DNA File:')
        self.file_path_edit = QtWidgets.QLineEdit()
        self.browse_button = QtWidgets.QPushButton('Browse...')
        self.browse_button.clicked.connect(self.open_file_dialog)

        # DataLayer Combo Box
        self.data_layer_label = QtWidgets.QLabel('Select DataLayer:')
        self.data_layer_combo = QtWidgets.QComboBox()
        self.data_layer_combo.addItems([
            "DataLayer_All",
            "DataLayer_Behavior",
            "DataLayer_Definition",
            "DataLayer_Geometry",
            "DataLayer_Descriptor",
            "DataLayer_AllWithoutBlendShapes"
        ])

        # Save/Convert Button
        self.save_button = QtWidgets.QPushButton('Convert and Save as JSON')
        self.save_button.clicked.connect(self.save_as_json)

        # Add widgets to layout
        layout.addWidget(self.file_label)
        layout.addWidget(self.file_path_edit)
        layout.addWidget(self.browse_button)
        layout.addWidget(self.data_layer_label)
        layout.addWidget(self.data_layer_combo)
        layout.addWidget(self.save_button)

        # Set the central widget
        self.setCentralWidget(central_widget)

    def open_file_dialog(self):
        file_dialog = QtWidgets.QFileDialog(self)
        dna_file, _ = file_dialog.getOpenFileName(self, 'Open DNA File', '', 'DNA Files (*.dna);;All Files (*)')
        if dna_file:
            self.file_path_edit.setText(dna_file)

    def save_as_json(self):
        dna_file = self.file_path_edit.text()
        if not dna_file or not os.path.exists(dna_file):
            QtWidgets.QMessageBox.warning(self, "Error", "Please select a valid DNA file.")
            return

        selected_data_layer = self.data_layer_combo.currentText()
        data_layer = self.get_data_layer(selected_data_layer)

        # Load the DNA file
        try:
            reader = self.load_dna(dna_file, data_layer)
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Error", f"Failed to load DNA file: {str(e)}")
            return

        # Ask where to save the JSON file
        file_dialog = QtWidgets.QFileDialog(self)
        json_file, _ = file_dialog.getSaveFileName(self, 'Save as JSON', '', 'JSON Files (*.json);;All Files (*)')
        if json_file:
            if not json_file.endswith(".json"):
                json_file += ".json"
            try:
                # Save the DNA file as JSON
                self.save_dna_json(reader, json_file, data_layer)
                QtWidgets.QMessageBox.information(self, "Success",
                                                  f"DNA file successfully saved as JSON at: {json_file}")
            except Exception as e:
                QtWidgets.QMessageBox.critical(self, "Error", f"Failed to save DNA as JSON: {str(e)}")

    def get_data_layer(self, selected_data_layer):
        """Return the appropriate DataLayer based on the selection"""
        return {
            "DataLayer_All": DataLayer_All,
            "DataLayer_Behavior": DataLayer_Behavior,
            "DataLayer_Definition": DataLayer_Definition,
            "DataLayer_Geometry": DataLayer_Geometry,
            "DataLayer_Descriptor": DataLayer_Descriptor,
            "DataLayer_AllWithoutBlendShapes": DataLayer_AllWithoutBlendShapes,
        }.get(selected_data_layer, DataLayer_All)

    def load_dna(self, dnafiletoload, data_layer):
        """Function to load the DNA file using the selected DataLayer"""
        stream = FileStream(dnafiletoload, FileStream.AccessMode_Read, FileStream.OpenMode_Binary)
        reader = BinaryStreamReader(stream, data_layer)
        reader.read()
        if not Status.isOk():
            status = Status.get()
            raise RuntimeError(f"Error loading DNA: {status.message}")
        return reader

    def save_dna_json(self, reader, jsonfiletosave, data_layer=DataLayer_All):
        """Function to save the DNA file as a JSON using JSONStreamWriter"""
        print("Saving JSON: " + jsonfiletosave)
        stream = FileStream(jsonfiletosave, FileStream.AccessMode_Write, FileStream.OpenMode_Binary)
        writer = JSONStreamWriter(stream)
        writer.setFrom(reader, data_layer)
        writer.write()

        if not Status.isOk():
            status = Status.get()
            raise RuntimeError(f"Error saving DNA: {status.message}")


# Show the widget within Maya
def show_dna_converter_in_maya():
    # Check if the window already exists
    global window
    try:
        window.close()  # Close the previous window if it exists
    except:
        pass

    # Create a new window
    window = DNAConverterApp(parent=get_maya_main_window())
    window.show()


# To display the UI in Maya, simply call this function:
show_dna_converter_in_maya()
