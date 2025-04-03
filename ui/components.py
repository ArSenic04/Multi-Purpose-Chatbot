import panel as pn
from typing import Dict, Any, Optional, List
import os

# Global UI components
chat_interface = None
layout = None
download_button = None

def create_chat_interface(callback):
    """Create the chat interface component"""
    global chat_interface
    chat_interface = pn.chat.ChatInterface(callback=callback, callback_user="BOT")
    return chat_interface

def create_buttons():
    """Create the main navigation buttons"""
    return pn.Row(
        pn.layout.HSpacer(),
        pn.widgets.Button(name="Amazon Ads Queries", button_type="primary"),
        pn.widgets.Button(name="Seller Queries", button_type="success"),
        pn.widgets.Button(name="PDF Queries", button_type="warning"),
        pn.widgets.Button(name="Code Generation", button_type="light"),
        pn.layout.HSpacer()
    )

def create_file_inputs():
    """Create file upload components"""
    upload_csv_button = pn.widgets.FileInput(name="Upload CSV", accept=".csv")
    upload_pdf_button = pn.widgets.FileInput(name="Upload PDF", accept=".pdf")
    return upload_csv_button, upload_pdf_button

def create_layout(buttons):
    """Create the main application layout"""
    global layout
    layout = pn.Column(
        pn.layout.VSpacer(),
        pn.Row(
            pn.layout.HSpacer(),
            buttons,
            pn.layout.HSpacer()
        ),
        pn.layout.VSpacer()
    )
    return layout

def update_layout_with_download_button(file_path: str, row_count: int):
    """Update the layout with a download button for filtered data"""
    global layout, download_button, chat_interface
    
    if layout is None:
        return
    
    download_button = pn.widgets.FileDownload(
        file=file_path,
        filename=os.path.basename(file_path),
        button_type="success",
        label=f"Download Filtered Data ({row_count} rows)"
    )
    
    current_objects = list(layout.objects)
    # Find the position of chat_interface
    chat_interface_position = -1
    for i, obj in enumerate(current_objects):
        if isinstance(obj, pn.chat.ChatInterface):
            chat_interface_position = i
            break
    
    # Remove any existing download buttons
    current_objects = [obj for obj in current_objects if not isinstance(obj, pn.widgets.FileDownload)]
    
    # Insert the new download button before chat_interface
    if chat_interface_position != -1:
        current_objects.insert(chat_interface_position, download_button)
    else:
        current_objects.append(download_button)
    
    layout.objects = current_objects