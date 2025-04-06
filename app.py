import streamlit as st
import datetime
import pandas as pd
import os
import base64
import tempfile
from io import BytesIO
from fpdf import FPDF

# Set page configuration
st.set_page_config(
    page_title="Client Call Report for Real Estate Purchase",
    page_icon="🏢",
    layout="wide"
)

# Custom CSS to make the app look better
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;500;600;700&display=swap');
    
    * {
        font-family: 'Montserrat', sans-serif;
    }
    
    h1, h2, h3 {
        color: #2c3e50;
    }
    
    .main-header {
        font-size: 36px;
        font-weight: bold;
        color: #b8860b;
        text-align: center;
        margin-bottom: 30px;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
    }
    
    .logo-container {
        text-align: center;
        margin-bottom: 20px;
    }
    
    .report-container {
        background-color: #f8f9fa;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }
    
    .stButton button {
        background-color: #b8860b;
        color: white;
        font-weight: bold;
    }
    
    .stButton button:hover {
        background-color: #a67c00;
    }
    
    .pdf-download {
        text-align: center;
        margin-top: 20px;
    }
    
    .gold-text {
        color: #b8860b;
    }
</style>
""", unsafe_allow_html=True)

# Display logo
st.markdown(
    """
    <div class="logo-container">
        <img src="data:image/jpeg;base64,{}" width="400">
    </div>
    """.format(
        base64.b64encode(open("assets/logo.jpg", "rb").read()).decode()
    ),
    unsafe_allow_html=True,
)

# Title with custom styling
st.markdown('<h1 class="main-header">AL HAYAH REAL ESTATE INVESTMENT</h1>', unsafe_allow_html=True)

# Function to create PDF using FPDF
def create_pdf(report_data):
    class PDF(FPDF):
        def header(self):
            # Logo
            try:
                self.image("assets/logo.jpg", 10, 8, 70)
            except:
                pass
            # Title
            self.set_font('Arial', 'B', 20)
            self.set_text_color(184, 134, 11)  # Gold color
            self.cell(0, 20, 'AL HAYAH REAL ESTATE INVESTMENT', 0, 1, 'C')
            # Line break
            self.ln(10)
        
        def footer(self):
            # Position at 1.5 cm from bottom
            self.set_y(-15)
            # Arial italic 8
            self.set_font('Arial', 'I', 8)
            # Text color in gray
            self.set_text_color(128)
            # Page number
            self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')
            # Copyright
            self.set_y(-20)
            self.cell(0, 10, f'© {datetime.datetime.now().year} AL HAYAH REAL ESTATE INVESTMENT - All Rights Reserved', 0, 0, 'C')
    
    # Create PDF instance
    pdf = PDF()
    pdf.add_page()
    
    # Report title
    pdf.set_font('Arial', 'B', 16)
    pdf.set_text_color(44, 62, 80)  # Dark blue
    pdf.cell(0, 10, report_data["Report Name"], 0, 1, 'C')
    pdf.ln(5)
    
    # Content
    pdf.set_font('Arial', '', 12)
    pdf.set_text_color(0, 0, 0)
    
    # Left column
    col_width = 95
    row_height = 10
    
    # Client information section
    pdf.set_font('Arial', 'B', 14)
    pdf.set_text_color(44, 62, 80)
    pdf.cell(0, 10, 'Client Information', 0, 1)
    pdf.ln(2)
    
    pdf.set_font('Arial', 'B', 12)
    pdf.set_text_color(0, 0, 0)
    
    # Two columns layout
    y_position = pdf.get_y()
    
    # Left column
    pdf.set_xy(10, y_position)
    pdf.cell(col_width, row_height, 'Client Name:', 0, 0)
    pdf.set_font('Arial', '', 12)
    pdf.cell(col_width, row_height, report_data["Client Name"], 0, 1)
    
    pdf.set_x(10)
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(col_width, row_height, 'Unit Type:', 0, 0)
    pdf.set_font('Arial', '', 12)
    pdf.cell(col_width, row_height, report_data["Unit Type"], 0, 1)
    
    pdf.set_x(10)
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(col_width, row_height, 'Unit Area:', 0, 0)
    pdf.set_font('Arial', '', 12)
    pdf.cell(col_width, row_height, f'From {report_data["Unit Area From"]} to {report_data["Unit Area To"]} sq.m', 0, 1)
    
    pdf.set_x(10)
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(col_width, row_height, 'Number of Rooms:', 0, 0)
    pdf.set_font('Arial', '', 12)
    pdf.cell(col_width, row_height, str(report_data["Number of Rooms"]), 0, 1)
    
    pdf.set_x(10)
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(col_width, row_height, 'Finishing Type:', 0, 0)
    pdf.set_font('Arial', '', 12)
    pdf.cell(col_width, row_height, report_data["Finishing Type"], 0, 1)
    
    pdf.set_x(10)
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(col_width, row_height, 'Location:', 0, 0)
    pdf.set_font('Arial', '', 12)
    pdf.cell(col_width, row_height, report_data["Location"], 0, 1)
    
    # Right column
    pdf.set_xy(105, y_position)
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(col_width, row_height, 'Report Date:', 0, 0)
    pdf.set_font('Arial', '', 12)
    pdf.cell(col_width, row_height, report_data["Report Date"].strftime('%Y-%m-%d'), 0, 1)
    
    pdf.set_x(105)
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(col_width, row_height, 'Budget:', 0, 0)
    pdf.set_font('Arial', '', 12)
    pdf.cell(col_width, row_height, str(report_data["Budget"]), 0, 1)
    
    pdf.set_x(105)
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(col_width, row_height, 'Payment Method:', 0, 0)
    pdf.set_font('Arial', '', 12)
    pdf.cell(col_width, row_height, report_data["Payment Method"], 0, 1)
    
    pdf.set_x(105)
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(col_width, row_height, 'Delivery Date:', 0, 0)
    pdf.set_font('Arial', '', 12)
    pdf.cell(col_width, row_height, report_data["Delivery Date"].strftime('%Y-%m-%d'), 0, 1)
    
    pdf.set_x(105)
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(col_width, row_height, 'Sales Person:', 0, 0)
    pdf.set_font('Arial', '', 12)
    pdf.cell(col_width, row_height, report_data["Sales Person"], 0, 1)
    
    pdf.set_x(105)
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(col_width, row_height, 'Sales Phone:', 0, 0)
    pdf.set_font('Arial', '', 12)
    pdf.cell(col_width, row_height, report_data["Sales Phone"], 0, 1)
    
    # Create a temporary file to store the PDF
    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp:
        pdf_output = BytesIO()
        pdf.output(pdf_output)
        pdf_bytes = pdf_output.getvalue()
        
        # Write to the temporary file
        tmp.write(pdf_bytes)
        
        # Return the filename
        return tmp.name, pdf_bytes

# Create a container for the form
with st.container():
    st.markdown('<div class="report-container">', unsafe_allow_html=True)
    
    # Form for data entry
    with st.form(key="real_estate_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            # Report name
            report_name = st.text_input("Report Name", value="Client Call Report for Real Estate Purchase")
            
            # Client name
            client_name = st.text_input("Client Name")
            
            # Unit type selection
            unit_types = [
                "Studio", 
                "Apartment", 
                "Duplex", 
                "Penthouse", 
                "Town House", 
                "Twin House", 
                "Villa", 
                "Chalet", 
                "Commercial Space", 
                "Administrative Space"
            ]
            unit_type = st.selectbox("Unit Type", unit_types)
            
            # Unit area
            col_area1, col_area2 = st.columns(2)
            with col_area1:
                min_area = st.number_input("Unit Area From", min_value=0, value=0)
            with col_area2:
                max_area = st.number_input("To", min_value=0, value=0)
            
            # Number of rooms
            rooms = st.number_input("Number of Rooms", min_value=0, value=0)
            
            # Finishing type
            finishing_types = ["Fully Finished", "Semi-Finished", "Core & Shell"]
            finishing = st.selectbox("Finishing Type", finishing_types)
        
        with col2:
            # Report date
            report_date = st.date_input("Report Date", value=datetime.date.today())
            
            # Area selection
            areas = [
                "Sheikh Zayed",
                "October",
                "October Gardens",
                "Green Belt",
                "Green Revolution",
                "New Cairo",
                "Fifth Settlement",
                "Future City",
                "El Shorouk",
                "Administrative Capital",
                "Ain Sokhna",
                "Red Sea",
                "North Coast"
            ]
            area = st.selectbox("Location", areas)
            
            # Budget
            budget = st.number_input("Budget", min_value=0, value=0)
            
            # Payment method
            payment_methods = ["Cash", "Installment"]
            payment_method = st.selectbox("Payment Method", payment_methods)
            
            # Delivery date
            delivery_date = st.date_input("Delivery Date", value=datetime.date.today() + datetime.timedelta(days=365))
            
            # Sales person name and phone
            sales_name = st.text_input("Sales Person")
            sales_phone = st.text_input("Sales Phone")
        
        # Submit button
        submit_button = st.form_submit_button(label="Generate Report")
    
    st.markdown('</div>', unsafe_allow_html=True)

# Display the report when submitted
if 'submit_button' in locals() and submit_button:
    st.markdown('<div class="report-container">', unsafe_allow_html=True)
    
    st.markdown(f"<h2 style='text-align: center; color: #b8860b;'>{report_name}</h2>", unsafe_allow_html=True)
    
    # Create two columns for the report display
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"**Client Name:** {client_name}")
        st.markdown(f"**Unit Type:** {unit_type}")
        st.markdown(f"**Unit Area:** From {min_area} to {max_area} sq.m")
        st.markdown(f"**Number of Rooms:** {rooms}")
        st.markdown(f"**Finishing Type:** {finishing}")
        st.markdown(f"**Location:** {area}")
    
    with col2:
        st.markdown(f"**Report Date:** {report_date.strftime('%Y-%m-%d')}")
        st.markdown(f"**Budget:** {budget}")
        st.markdown(f"**Payment Method:** {payment_method}")
        st.markdown(f"**Delivery Date:** {delivery_date.strftime('%Y-%m-%d')}")
        st.markdown(f"**Sales Person:** {sales_name}")
        st.markdown(f"**Sales Phone:** {sales_phone}")
    
    # Create a dictionary with the report data
    report_data = {
        "Report Date": report_date,
        "Report Name": report_name,
        "Client Name": client_name,
        "Unit Type": unit_type,
        "Unit Area From": min_area,
        "Unit Area To": max_area,
        "Number of Rooms": rooms,
        "Finishing Type": finishing,
        "Location": area,
        "Budget": budget,
        "Payment Method": payment_method,
        "Delivery Date": delivery_date,
        "Sales Person": sales_name,
        "Sales Phone": sales_phone
    }
    
    # Generate PDF
    pdf_file, pdf_bytes = create_pdf(report_data)
    
    # Create download button
    st.markdown('<div class="pdf-download">', unsafe_allow_html=True)
    st.download_button(
        label="Download Report as PDF",
        data=pdf_bytes,
        file_name=f"real_estate_report_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
        mime="application/pdf",
    )
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Clean up the temporary file
    os.unlink(pdf_file)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Add footer
st.markdown("""
<div style="text-align: center; margin-top: 30px; padding: 20px; background-color: #f8f9fa; border-radius: 10px;">
    <p>© 2025 AL HAYAH REAL ESTATE INVESTMENT - All Rights Reserved</p>
</div>
""", unsafe_allow_html=True)
