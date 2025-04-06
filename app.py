import streamlit as st
import datetime
import pandas as pd
import os
import base64
import tempfile
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

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

# Function to create PDF using ReportLab
def create_pdf(report_data):
    # Create a BytesIO object to store the PDF
    buffer = BytesIO()
    
    # Create the PDF document
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=18)
    
    # Container for the 'Flowable' objects
    elements = []
    
    # Register a standard font
    styles = getSampleStyleSheet()
    
    # Create custom styles
    title_style = ParagraphStyle(
        'Title',
        parent=styles['Heading1'],
        fontSize=18,
        textColor=colors.Color(184/255, 134/255, 11/255),  # Gold color
        alignment=1,  # Center alignment
        spaceAfter=12
    )
    
    heading_style = ParagraphStyle(
        'Heading',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.Color(44/255, 62/255, 80/255),  # Dark blue
        spaceAfter=6
    )
    
    normal_style = ParagraphStyle(
        'Normal',
        parent=styles['Normal'],
        fontSize=10,
        spaceAfter=6
    )
    
    # Add logo
    try:
        logo_path = "assets/logo.jpg"
        img = Image(logo_path, width=2.5*inch, height=1*inch)
        elements.append(img)
    except:
        pass
    
    # Add company name
    elements.append(Paragraph("AL HAYAH REAL ESTATE INVESTMENT", title_style))
    elements.append(Spacer(1, 0.25*inch))
    
    # Add report title
    elements.append(Paragraph(report_data["Report Name"], heading_style))
    elements.append(Spacer(1, 0.25*inch))
    
    # Create data for the table
    data = [
        ["Client Information", ""],
        ["Client Name:", report_data["Client Name"]],
        ["Unit Type:", report_data["Unit Type"]],
        ["Unit Area:", f"From {report_data['Unit Area From']} to {report_data['Unit Area To']} sq.m"],
        ["Number of Rooms:", str(report_data["Number of Rooms"])],
        ["Finishing Type:", report_data["Finishing Type"]],
        ["Location:", report_data["Location"]],
        ["", ""],
        ["Report Details", ""],
        ["Report Date:", report_data["Report Date"].strftime('%Y-%m-%d')],
        ["Budget:", str(report_data["Budget"])],
        ["Payment Method:", report_data["Payment Method"]],
        ["Delivery Date:", report_data["Delivery Date"].strftime('%Y-%m-%d')],
        ["Sales Person:", report_data["Sales Person"]],
        ["Sales Phone:", report_data["Sales Phone"]]
    ]
    
    # Create the table
    table = Table(data, colWidths=[2*inch, 3*inch])
    
    # Add style to the table
    table_style = TableStyle([
        ('BACKGROUND', (0, 0), (1, 0), colors.Color(184/255, 134/255, 11/255, 0.2)),
        ('BACKGROUND', (0, 8), (1, 8), colors.Color(184/255, 134/255, 11/255, 0.2)),
        ('TEXTCOLOR', (0, 0), (0, -1), colors.Color(44/255, 62/255, 80/255)),
        ('TEXTCOLOR', (0, 0), (1, 0), colors.Color(44/255, 62/255, 80/255)),
        ('TEXTCOLOR', (0, 8), (1, 8), colors.Color(44/255, 62/255, 80/255)),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (0, 0), (1, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, 8), (1, 8), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('GRID', (0, 1), (1, 6), 0.5, colors.grey),
        ('GRID', (0, 9), (1, 14), 0.5, colors.grey),
        ('SPAN', (0, 0), (1, 0)),
        ('SPAN', (0, 8), (1, 8)),
    ])
    
    table.setStyle(table_style)
    elements.append(table)
    
    # Add footer
    elements.append(Spacer(1, 0.5*inch))
    footer_text = f"© {datetime.datetime.now().year} AL HAYAH REAL ESTATE INVESTMENT - All Rights Reserved"
    elements.append(Paragraph(footer_text, normal_style))
    
    # Build the PDF
    doc.build(elements)
    
    # Get the value of the BytesIO buffer
    pdf_bytes = buffer.getvalue()
    buffer.close()
    
    # Create a temporary file to store the PDF
    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp:
        tmp.write(pdf_bytes)
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
