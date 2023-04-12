from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle

# Create a new PDF document
doc = SimpleDocTemplate("table.pdf", pagesize=landscape(letter))

# Define the table data
data = [
    ["Name", "Age", "Gender"],
    ["John Smith", "30", "Male"],
    ["Jane Doe", "25", "Female"],
    ["Bob Johnson", "35", "Male"],
]

lx = {
    "-NJJKiMDcRvSG-tAGJY5": {
        "adminDate": "15-12-2022",
        "adminTime": "11:22",
        "approvedByHod": "Benedict S",
        "branch": "CSE",
        "date": "15-12-2022",
        "deanStatus": "Denied",
        "designation": "Non Teaching",
        "email": "arunvibrant@gmail.com",
        "hodStatus": "Approved",
        "key": "-NJJKiMDcRvSG-tAGJY5",
        "month": "December",
        "name": "Mr. K. Arunraj",
        "photoUrl": "https://lh3.googleusercontent.com/a/AEdFTp4Y0m424z8QJk5pnk5Mwkw2d4dWaVsOTCGHg7XQ=s96-c",
        "reason": "going to cinema",
        "time": "11:22",
        "workCompletion": "Yes",
    },
    "-NJJLq0NZntOZCp4MCAC": {
        "adminDate": "15-12-2022",
        "adminTime": "11:27",
        "approvedByHod": "Benedict S",
        "branch": "CSE",
        "date": "15-12-2022",
        "deanStatus": "Approved",
        "designation": "Non Teaching",
        "email": "arunvibrant@gmail.com",
        "hodStatus": "Approved",
        "key": "-NJJLq0NZntOZCp4MCAC",
        "month": "December",
        "name": "Mr. K. Arunraj",
        "photoUrl": "https://lh3.googleusercontent.com/a/AEdFTp4Y0m424z8QJk5pnk5Mwkw2d4dWaVsOTCGHg7XQ=s96-c",
        "reason": "personal",
        "time": "11:27",
        "workCompletion": "Yes",
    },
    "-NJJSdMKhylcc8yByyVC": {
        "adminDate": "15-12-2022",
        "adminTime": "11:56",
        "approvedByHod": "Benedict S",
        "branch": "CSE",
        "date": "15-12-2022",
        "deanStatus": "Approved",
        "designation": "Non Teaching",
        "email": "ramdanvanth@gmail.com",
        "hodStatus": "Approved",
        "key": "-NJJSdMKhylcc8yByyVC",
        "month": "December",
        "name": "Mr.A.Ramkumar",
        "photoUrl": "https://lh3.googleusercontent.com/a/AEdFTp5U551nSUJagFuDU9IpXo7lpSNFRbW1Frhx2JK7=s96-c",
        "reason": "personal",
        "time": "11:57",
        "workCompletion": "Yes",
    },
    "-NJJkwvnEwCVv7riMrgf": {
        "adminDate": "15-12-2022",
        "adminTime": "13:21",
        "approvedByHod": "Benedict S",
        "branch": "CSE",
        "date": "15-12-2022",
        "deanStatus": "Approved",
        "designation": "Non Teaching",
        "email": "ramdanvanth@gmail.com",
        "hodStatus": "Approved",
        "key": "-NJJkwvnEwCVv7riMrgf",
        "month": "December",
        "name": "Mr.A.Ramkumar",
        "photoUrl": "https://lh3.googleusercontent.com/a/AEdFTp5U551nSUJagFuDU9IpXo7lpSNFRbW1Frhx2JK7=s96-c",
        "reason": "personal work",
        "time": "13:21",
        "workCompletion": "Yes",
    },
    "-NJOfOPSbEwVvF2tS01l": {
        "adminDate": "16-12-2022",
        "adminTime": "12:14",
        "approvedByHod": "Benedict S",
        "branch": "CSE",
        "date": "16-12-2022",
        "deanStatus": "Approved",
        "designation": "Teaching",
        "email": "ssspcg01@gmail.com",
        "hodStatus": "Approved",
        "key": "-NJOfOPSbEwVvF2tS01l",
        "month": "December",
        "name": "Sankaran S",
        "photoUrl": "https://lh3.googleusercontent.com/a/AEdFTp6G0QL39ElfIYQH7I5s0jy6vhqzvMcjGYzk0OVU=s96-c",
        "reason": "traveling",
        "time": "12:15",
        "workCompletion": "Yes",
    },
    "-NJOftrnqy1Wm36ymmU6": {
        "adminDate": "16-12-2022",
        "adminTime": "12:18",
        "approvedByHod": "Benedict S",
        "branch": "CSE",
        "date": "16-12-2022",
        "deanStatus": "Denied",
        "designation": "Teaching",
        "email": "ssspcg01@gmail.com",
        "hodStatus": "Approved",
        "key": "-NJOftrnqy1Wm36ymmU6",
        "month": "December",
        "name": "Sankaran S",
        "photoUrl": "https://lh3.googleusercontent.com/a/AEdFTp6G0QL39ElfIYQH7I5s0jy6vhqzvMcjGYzk0OVU=s96-c",
        "reason": "Christmas eve",
        "time": "12:18",
        "workCompletion": "Yes",
    },
    "-NJOg-Dx32t3FuFtiYUd": {
        "adminDate": "16-12-2022",
        "adminTime": "12:17",
        "approvedByHod": "Benedict S",
        "branch": "CSE",
        "date": "16-12-2022",
        "deanStatus": "Approved",
        "designation": "Non Teaching",
        "email": "subashinip14@gmail.com",
        "hodStatus": "Approved",
        "key": "-NJOg-Dx32t3FuFtiYUd",
        "month": "December",
        "name": "Subashini",
        "photoUrl": "https://lh3.googleusercontent.com/a/AEdFTp51xkjgVHbhdtfN3qs_pqnto3qFQhF7b0OfPhDS=s96-c",
        "reason": "personal work",
        "time": "12:17",
        "workCompletion": "Yes",
    },
    "-NJOg6W-i-NygLtjG2jV": {
        "adminDate": "16-12-2022",
        "adminTime": "12:18",
        "approvedByHod": "Benedict S",
        "branch": "CSE",
        "date": "16-12-2022",
        "deanStatus": "Denied",
        "designation": "Non Teaching",
        "email": "arasuannauniversity@gmail.com",
        "hodStatus": "Approved",
        "key": "-NJOg6W-i-NygLtjG2jV",
        "month": "December",
        "name": "Dr. E.S THIRUNAVUKKARASU",
        "photoUrl": "https://lh3.googleusercontent.com/a/AEdFTp7Qv0SRJYPuyRYXDC4_XYF9Ubh3tyQIYHQ0TeXe=s96-c",
        "reason": "Personal work",
        "time": "12:20",
        "workCompletion": "Yes",
    },
}
# Define the table width and height
history = []
for item in lx.values():
    history.append(
        [
            item.get("name"),
            item.get("branch"),
            item.get("deanStatus"),
            item.get("date"),
            item.get("time"),
        ]
    )

table = Table(history)

# width, height = landscape(letter)
# table = Table(lx)
#
# Set the table style
style = TableStyle(
    [
        ("BACKGROUND", (0, 0), (-1, 0), colors.gray),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 14),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
        ("BACKGROUND", (0, -1), (-1, -1), colors.beige),
        ("GRID", (0, 0), (-1, -1), 1, colors.black),
    ]
)
table.setStyle(style)

# Add the table to the PDF document
doc.build([table])
