import os
import panel as pn
from dotenv import load_dotenv

from database.models import Base, engine
from agents.pdf_agent import PDFQueryAgent
from agents.seller_agent import SellerAgent
from agents.general_agent import GeneralAgent
from agents.code_agent import DHI_CodeBot
from utils.helpers import ensure_uploads_dir
from ui.components import (
    create_chat_interface,
    create_buttons,
    create_file_inputs,
    create_layout,
    update_layout_with_download_button
)

# Initialize Panel extension and load environment variables
pn.extension()
load_dotenv()

# Ensure database tables exist
Base.metadata.create_all(bind=engine)

# Global state variables
current_csv_filename = None
current_pdf_filename = None
filtered_df = None
filtered_csv_path = None
pdf_query_agent = None
seller_agent = None
general_agent = None
dhi_codebot_agent = None

async def chat_callback(contents: str, user: str, instance: pn.chat.ChatInterface):
    """Main callback function for chat interface"""
    if general_agent:
        return general_agent.query(contents)
    elif seller_agent:
        return seller_agent.query(contents)
    elif pdf_query_agent:
        return pdf_query_agent.query(contents)
    elif dhi_codebot_agent:
        return dhi_codebot_agent.query(contents)
    else:
        return "❌ No valid agent initialized."

# Create UI components
chat_interface = create_chat_interface(callback=chat_callback)
buttons = create_buttons()
upload_csv_button, upload_pdf_button = create_file_inputs()
layout = create_layout(buttons)

def handle_csv_upload(event):
    """Handle CSV file upload"""
    global seller_agent, current_csv_filename
    file = event.new
    if file:
        # Get the filename from the widget's metadata
        filename = upload_csv_button.filename
        current_csv_filename = filename
        
        # Ensure uploads directory exists
        file_path = os.path.join(ensure_uploads_dir(), filename)
        
        # Save the file with its original name
        with open(file_path, "wb") as f:
            f.write(file)
        
        seller_agent = SellerAgent(csv_path=file_path)
        chat_interface.send(f"CSV file '{filename}' uploaded and SellerAgent is ready for queries.", user="System", respond=False)

def handle_pdf_upload(event):
    """Handle PDF file upload"""
    global pdf_query_agent, current_pdf_filename
    file = event.new
    if file:
        # Get the filename from the widget's metadata
        filename = upload_pdf_button.filename
        current_pdf_filename = filename
        
        # Ensure uploads directory exists
        file_path = os.path.join(ensure_uploads_dir(), filename)
        
        # Save the file with its original name
        with open(file_path, "wb") as f:
            f.write(file)
        
        chat_interface.send(f"PDF file '{filename}' uploaded. Processing...", user="System", respond=False)
        pdf_query_agent = PDFQueryAgent(pdf_path=file_path)
        chat_interface.send(f"PDF '{filename}' is ready for queries.", user="System", respond=False)

# Set up event handlers for file uploads
upload_csv_button.param.watch(handle_csv_upload, 'value')
upload_pdf_button.param.watch(handle_pdf_upload, 'value')

def on_button_click(event):
    """Handle button click events"""
    global layout, chat_interface, general_agent, seller_agent, pdf_query_agent, dhi_codebot_agent
    
    # Clear the layout and remove buttons after a click
    new_layout = []
    
    if event.obj.name == "Amazon Ads Queries":
        general_agent = GeneralAgent(chat_interface=chat_interface)
        new_layout.append(chat_interface)
    elif event.obj.name == "Seller Queries":
        seller_agent = SellerAgent()  # Initialize without CSV - user will upload
        new_layout.append(upload_csv_button)
        new_layout.append(chat_interface)
    elif event.obj.name == "PDF Queries":
        new_layout.append(upload_pdf_button)
        new_layout.append(chat_interface)
    elif event.obj.name == "Code Generation":
        dhi_codebot_agent = DHI_CodeBot()
        new_layout.append(chat_interface)

    layout.objects = new_layout  # Hide buttons and update layout

# Link button click events
for button in buttons.objects[1:5]:
    button.on_click(on_button_click)

# Initialize with only buttons visible
layout.objects = [buttons]

# Make the app servable
layout.servable()