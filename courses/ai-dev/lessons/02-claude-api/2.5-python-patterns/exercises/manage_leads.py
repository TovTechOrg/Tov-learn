leads = [
    {"name": "דנה לוי", "company": "בנק לאומי", "title": "מנהלת שיווק דיגיטלי"},
    {"name": "יוסי כהן", "company": "אל על", "title": "Data Analyst"},
    {"name": "אביגיל שרון", "company": "Wix", "title": "Senior Product Manager"},
    {"name": "משה פרץ", "company": "תנובה", "title": "סמנכ\"ל תפעול"}
]

for lead in leads:
    
    print(f"שם: {lead['name']}, חברה: {lead['company']}, תפקיד: {lead['title']}")

    if ("Manager" in lead['title']) or ("מנהל" in lead['title']):
        print(">> ליד בעדיפות גבוהה")
