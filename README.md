# MetaHuman DNA to JSON Converter for Maya

## Overview

This is a **Maya 2023** based Python application designed to **load MetaHuman DNA files** and **convert them to JSON format**. The application provides an intuitive user interface for Maya, allowing users to load DNA files, select a desired data layer, and save the file in JSON format. 

The application utilizes the [**MetaHuman-DNA-Calibration**](https://github.com/EpicGames/MetaHuman-DNA-Calibration) API, developed by **Epic Games**, which allows for the manipulation, modification, and calibration of **MetaHuman DNA files**. The DNA files store the rigging and animation data necessary to drive high-quality MetaHuman facial rigs.

## Features

- **Load DNA Files**: Open DNA files using a file dialog within Maya.
- **Select Data Layers**: Choose from multiple available data layers (e.g., `DataLayer_All`, `DataLayer_Behavior`, etc.) when loading DNA files.
- **Save as JSON**: Convert and save the DNA data to a JSON format using the **MetaHuman-DNA-Calibration** API.
- **User-Friendly Interface**: A simple, streamlined PyQt-based interface embedded in Maya.

## Requirements

- **Maya 2023** or later.
- **MetaHuman-DNA-Calibration API** (found here: [https://github.com/EpicGames/MetaHuman-DNA-Calibration](https://github.com/EpicGames/MetaHuman-DNA-Calibration)).
- **PySide2**: This application uses the PySide2 framework for building the UI.

## Installation and Setup

1. **Install PySide2**:
    - Run the following command to install PySide2 if it’s not already available:
      ```bash
      pip install PySide2
      ```

2. **Clone the MetaHuman-DNA-Calibration repository**:
    - Clone the MetaHuman-DNA-Calibration repository from GitHub:
      ```bash
      git clone https://github.com/EpicGames/MetaHuman-DNA-Calibration.git
      ```

3. **Set up the API in Maya**:
    - Follow the setup instructions provided in the MetaHuman-DNA-Calibration repository to ensure the API is accessible from Maya.

4. **Run the Script**:
    - Load the provided Python script in Maya’s Script Editor and run it. Use the following function call to open the UI:
      ```python
      show_dna_converter_in_maya()
      ```

## Usage

1. **Open the UI**: In Maya’s Script Editor, execute the function `show_dna_converter_in_maya()` to launch the application.
   
2. **Load a DNA File**: 
   - Use the "Browse" button to select a `.dna` file.
   
3. **Select a DataLayer**:
   - Choose one of the available DataLayers from the dropdown:
     - `DataLayer_All`
     - `DataLayer_Behavior`
     - `DataLayer_Definition`
     - `DataLayer_Geometry`
     - `DataLayer_Descriptor`
     - `DataLayer_AllWithoutBlendShapes`

4. **Convert and Save as JSON**:
   - Click "Convert and Save as JSON" to select the location where you want to save the `.json` file.

5. **Success Notification**:
   - Once the file is successfully converted and saved, a success message will appear.

## Supported Data Layers

The application supports the following **DataLayers** from the MetaHuman-DNA-Calibration API:

- **DataLayer_All**: Loads all available data.
- **DataLayer_Behavior**: Loads only the behavioral (dynamic) data.
- **DataLayer_Definition**: Loads static data, including joint names, blend shapes, and mappings.
- **DataLayer_Geometry**: Loads mesh and geometry data.
- **DataLayer_Descriptor**: Loads basic metadata about the character.
- **DataLayer_AllWithoutBlendShapes**: Loads everything except blend shapes.

## Example Code Snippets

- **Loading a DNA File**:
    ```python
    reader = load_dna("path/to/dnafile.dna", DataLayer_All)
    ```

- **Saving DNA as JSON**:
    ```python
    save_dna_json(reader, "path/to/output.json", DataLayer_All)
    ```

## Known Issues

- Ensure that the **MetaHuman-DNA-Calibration API** is set up correctly within Maya.
- The application depends on the availability of **FileStream**, **BinaryStreamReader**, **JSONStreamWriter**, and other components provided by the API.

## License

This project makes use of the **MetaHuman-DNA-Calibration** API by Epic Games. Please refer to the [MetaHuman-DNA-Calibration repository](https://github.com/EpicGames/MetaHuman-DNA-Calibration) for licensing information and terms of use.
