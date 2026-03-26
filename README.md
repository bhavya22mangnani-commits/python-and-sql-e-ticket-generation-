# python-and-sql-e-ticket-generation-
A Python-based automation tool that generates professional Emirates-style PDF e-tickets using MySQL, ReportLab, and QR Code integration.
A robust Python application designed to automate the creation of high-fidelity airline e-ticket receipts. This project demonstrates the integration of relational databases with dynamic PDF document generation.

 Key Features
Database Integration: Fetches real-time flight and class availability from a MySQL backend.

Professional PDF Layouts: Uses ReportLab to build complex document structures, including tables, gradients, and custom branding.

Smart Automation: * Automatic PNR and ticket number generation.

Algorithmic seat assignment based on travel class.

Flight duration calculation and IATA code mapping.

Security & Verification: Generates unique QR Codes for each ticket containing passenger metadata.

Localization: Built-in support for the Indian Rupee (₹) symbol using custom TTF font registration.

 Tech Stack
Language: Python 3.x

Database: MySQL (via mysql-connector)

PDF Engine: ReportLab

Imaging: QRcode, Pillow

Utilities: Datetime, Random, String

3. A "Quick Start" Snippet (Optional Add-on)
To make your repo even more professional, add a small "Requirements" section so others can run it:

 Prerequisites
MySQL Server: Ensure you have the airline_tickets database configured.

Font File: Place DejaVuSans.ttf in the root directory to render currency symbols.
