import mysql.connector
import random, string, os, qrcode
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# --- RUPEE SYMBOL FIX: FONT REGISTRATION ---
# This part is essential. It tells ReportLab how to find and use the Rupee symbol.
# Ensure 'DejaVuSans.ttf' is in the same directory as this script.
try:
    pdfmetrics.registerFont(TTFont('DejaVu', 'DejaVuSans.ttf'))
except:
    print("FATAL ERROR: DejaVuSans.ttf font not found. Please download it and place it in the script's folder.")
    exit()

# ---------- MySQL Connection ----------
def get_connection():
    """Establishes a connection to the MySQL database."""
    try:
        return mysql.connector.connect(
            host="localhost",
            user="root",              # Change if different
            password="",  # Put your MySQL root password
            database="airline_tickets"
        )
    except mysql.connector.Error as err:
        print(f"Error connecting to database: {err}")
        exit()

# ---------- Utilities ----------
def random_pnr(): return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
def random_ticket_number(): return "176" + ''.join(random.choices(string.digits, k=10))
def make_qr(data, filename):
    img = qrcode.make(data, border=2)
    img.save(filename)
def auto_seat(index, flight_class):
    if flight_class.lower() == 'first': row, seat_char = 2 + (index // 2), chr(ord('A') + (index % 2))
    elif flight_class.lower() == 'business': row, seat_char = 8 + (index // 4), chr(ord('A') + (index % 4))
    else: row, seat_char = 20 + (index // 6), chr(ord('A') + (index % 6))
    return f"{row}{seat_char}"

# ---------- Database Queries (No Changes Needed) ----------
def list_flights():
    conn = get_connection(); cur = conn.cursor()
    cur.execute("SELECT id, flight_number, from_city, to_city, travel_date FROM flights"); flights = cur.fetchall()
    conn.close(); return flights

def get_flight_details(flight_id):
    conn = get_connection(); cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM flights WHERE id=%s", (flight_id,)); flight = cur.fetchone()
    conn.close(); return flight

def get_class_details(flight_id, class_name):
    conn = get_connection(); cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM classes WHERE flight_id=%s AND class_name=%s", (flight_id, class_name)); cls = cur.fetchone()
    conn.close(); return cls

# ---------- Beautified Ticket PDF Generator ----------
def generate_ticket_pdf(flight, class_info, passengers):
    pnr = random_pnr(); booking_date = datetime.now()
    for i, p in enumerate(passengers):
        p["eticket"] = random_ticket_number()
        if not p.get("seat"): p["seat"] = auto_seat(i, class_info['class_name'])
    mock_fares_inr = {"First": 215000.00, "Business": 125000.00, "Economy": 40500.75}
    fare_per_ticket = mock_fares_inr.get(class_info['class_name'], 0.00)
    total_fare = fare_per_ticket * len(passengers); taxes = total_fare * 0.18; grand_total = total_fare + taxes

    os.makedirs("output", exist_ok=True); pdf_file = f"output/E-Ticket_{flight['flight_number']}_{pnr}.pdf"
    c = canvas.Canvas(pdf_file, pagesize=A4); width, height = A4
    
    emirates_red = colors.HexColor("#D82036"); dark_grey = colors.HexColor("#333333"); light_grey = colors.HexColor("#EAEAEA")
    
    # --- 1. HEADER ---
    c.setFillColor(emirates_red); c.rect(0, height - 40, width, 40, fill=1, stroke=0)
    c.setFillColor(colors.white); c.setFont("Helvetica-Bold", 16); c.drawString(30, height - 28, "Emirates")
    c.setFillColor(colors.white); c.setFont("Helvetica-Bold", 18); c.drawRightString(width - 30, height - 28, "E-Ticket Receipt")
    
    # --- 2. BOOKING REFERENCE ---
    last_y = height - 80 # Initialize Y cursor
    c.setFillColor(dark_grey); c.setFont("Helvetica", 11); c.drawString(30, last_y, "Prepared for:")
    c.setFont("Helvetica-Bold", 12); c.drawString(30, last_y - 15, passengers[0]['name'].upper())
    c.setFont("Helvetica", 11); c.drawRightString(width - 30, last_y, "BOOKING REFERENCE (PNR):")
    c.setFont("Helvetica-Bold", 16); c.setFillColor(emirates_red); c.drawRightString(width - 30, last_y - 20, pnr)
    last_y -= 45
    c.setStrokeColor(light_grey); c.line(30, last_y, width - 30, last_y)

    # --- 3. ITINERARY (WITH FINAL DETAILS) ---
    last_y -= 40
    c.setFillColor(dark_grey); c.setFont("Helvetica-Bold", 14); c.drawString(30, last_y, "Your Itinerary")
    last_y -= 115
    c.setStrokeColor(colors.grey); c.roundRect(30, last_y, width - 60, 110, 5, stroke=1, fill=0)
    
    # === FINAL DETAIL: Added plane_number and tail_number ===
    c.setFont("Helvetica-Bold", 11)
    c.drawString(50, last_y + 85, f"Flight {flight['flight_number']} ({flight['plane_number']} | Tail: {flight['tail_number']})")
    
    c.setFont("Helvetica", 11); c.drawString(50, last_y + 60, "From:"); c.drawString(width/2, last_y + 60, "To:")
    c.setFont("Helvetica-Bold", 18); c.drawString(50, last_y + 40, flight['from_city']); c.drawString(width/2, last_y + 40, flight['to_city'])
    c.setFont("Helvetica", 11); c.drawString(50, last_y + 20, f"Departure: {flight['departure_time']} (Term. {flight['from_terminal']})"); c.drawString(width/2, last_y + 20, f"Arrival: {flight['arrival_time']} (Term. {flight['to_terminal']})")
    c.setFillColor(dark_grey); c.roundRect(width-135, last_y+82, 105, 20, 10, fill=1, stroke=0); c.setFillColor(colors.white); c.setFont("Helvetica-Bold", 11); c.drawCentredString(width-82.5, last_y+87, f"Class: {class_info['class_name']}")
    last_y -= 20

    # --- 4. PASSENGER DETAILS ---
    last_y -= 40
    c.setFillColor(dark_grey); c.setFont("Helvetica-Bold", 14); c.drawString(30, last_y, "Passenger Information")
    last_y -= 15
    passenger_data = [["PASSENGER", "E-TICKET NUMBER", "SEAT", "BAGGAGE ALLOWANCE"]]
    for p in passengers: passenger_data.append([p['name'].upper(), p['eticket'], p['seat'], f"Checked: {class_info['baggage_checkin']} | Cabin: {class_info['baggage_cabin']}"])
    table_height = (len(passengers) + 1) * 25
    passenger_table = Table(passenger_data, colWidths=[175, 125, 55, 165], rowHeights=25)
    passenger_table.setStyle(TableStyle([('BACKGROUND', (0,0), (-1,0), dark_grey), ('TEXTCOLOR',(0,0),(-1,0),colors.white), ('ALIGN', (0,0), (-1,-1), 'CENTER'), ('VALIGN', (0,0), (-1,-1), 'MIDDLE'), ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'), ('FONTSIZE', (0,0), (-1,0), 9), ('BOTTOMPADDING', (0,0), (-1,0), 8), ('ALIGN', (0,1), (0,-1), 'LEFT'), ('FONTNAME', (0,1), (-1,-1), 'Helvetica'), ('FONTSIZE', (0,1), (-1,-1), 9), ('GRID', (0,0), (-1,-1), 0.5, colors.grey)]))
    passenger_table.wrapOn(c, width, height); passenger_table.drawOn(c, 30, last_y - table_height)
    last_y -= (table_height + 10)

    # --- 5. FARE DETAILS ---
    last_y -= 30
    c.setFillColor(dark_grey); c.setFont("Helvetica-Bold", 14); c.drawString(30, last_y, "Fare & Payment Details")
    last_y -= 25
    c.setFont('Helvetica', 10); c.drawString(45, last_y, "Base Fare"); c.drawString(45, last_y - 20, "Taxes & Surcharges")
    c.setFont('DejaVu', 10); c.drawRightString(width-100, last_y, f"₹{fare_per_ticket:,.2f} x {len(passengers)}"); c.drawRightString(width-40, last_y, f"₹{total_fare:,.2f}"); c.drawRightString(width-40, last_y - 20, f"₹{taxes:,.2f}")
    last_y -= 35
    c.setDash(2, 2); c.setStrokeColor(colors.lightgrey); c.line(45, last_y, width-40, last_y); c.setDash(1,0)
    last_y -= 20
    c.setFont('Helvetica-Bold', 11); c.drawString(45, last_y, "Total Amount Paid (INR)")
    c.setFont('DejaVu', 11); c.drawRightString(width-40, last_y, f"₹{grand_total:,.2f}")
    last_y -= 30

    # --- 6. BOARDING INFORMATION & QR CODE ---
    qr_file = "e_ticket_qr.png"; make_qr(f"PNR:{pnr}|{passengers[0]['name']}|{flight['flight_number']}", qr_file)
    c.drawImage(qr_file, 45, last_y - 90, width=80, height=80, mask='auto'); os.remove(qr_file)
    c.setFont("Helvetica-Bold", 12); c.drawString(150, last_y, "Boarding Information")
    c.setFont("Helvetica", 9)
    c.drawString(150, last_y - 20, f"Lead Passenger: {passengers[0]['name'].upper()}")
    c.drawString(150, last_y - 35, f"Flight / Seat: {flight['flight_number']} / {passengers[0]['seat']}")
    c.drawString(150, last_y - 50, f"Date / Class: {flight['travel_date']} / {class_info['class_name']}")
    c.drawString(150, last_y - 65, "This is not a boarding pass. Please check-in online or at the airport.")
    last_y -= 100
    
    # --- 7. TERMS & CONDITIONS ---
    c.setFillColor(dark_grey); c.setFont("Helvetica-Bold", 10); c.drawString(30, last_y, "Important Information & Conditions of Carriage")
    last_y -= 15
    styles = getSampleStyleSheet()
    terms = """
    <b>Check-in:</b> Online check-in is available 48 hours before departure. Airport check-in counters close 60 minutes prior to departure for Economy Class and 45 minutes for Business/First Class. You must possess a valid passport, visa, and this e-ticket receipt. Failure to present required documents may result in denial of boarding.
    <br/><br/>
    <b>Baggage:</b> Baggage allowance is specified above. Excess baggage is subject to additional charges. Cabin baggage is limited to one piece (7kg). Valuable items, important documents, and medication should be carried in cabin baggage.
    <br/><br/>
    <b>Dangerous Goods:</b> For safety reasons, dangerous goods must not be carried in checked or cabin baggage. This includes but is not limited to: explosives, compressed gases, flammable liquids, and radioactive materials. A full list is available on our website.
    """
    p = Paragraph(terms, style=ParagraphStyle(name='Terms', fontSize=8, fontName='Helvetica', leading=11, textColor=colors.darkgrey))
    p.wrapOn(c, width-60, 150)
    p.drawOn(c, 30, last_y - p.height)

    c.save()
    print(f"\nSuccessfully generated final, perfected e-ticket: {pdf_file}")

# ---------- Main CLI (No Changes) ----------
def main():
    flights = list_flights()
    if not flights: print("No flights available at this time."); return
    print("\n--- Available Emirates Flights ---")
    for f in flights: print(f"ID {f[0]}: {f[1]} from {f[2]} to {f[3]} on {f[4]}")
    try: flight_id = int(input("\nEnter the ID of the flight you wish to book: "));
    except ValueError: print("Invalid input."); return
    flight = get_flight_details(flight_id)
    if not flight: print("Flight not found."); return
    class_name = input("Enter Class (Economy/Business/First): ").strip().title()
    class_info = get_class_details(flight_id, class_name)
    if not class_info: print(f"The '{class_name}' class is not available."); return
    try:
        num_passengers = int(input("Number of passengers: "))
        if num_passengers <= 0: raise ValueError
    except ValueError: print("Invalid number."); return
    passengers = []
    for i in range(num_passengers):
        print(f"\n--- Passenger {i+1} Details ---")
        name = input(f"Full Name: ").strip(); age = int(input(f"Age: "))
        seat = input(f"Preferred Seat (e.g., 20A) or leave blank for auto-assign: ").strip().upper()
        passengers.append({"name": name, "age": age, "seat": seat})
    generate_ticket_pdf(flight, class_info, passengers)

if __name__ == "__main__":
    main()
