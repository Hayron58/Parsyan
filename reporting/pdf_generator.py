```python
       import pandas as pd
       from fpdf import FPDF
       
       class ReportGenerator:
           def generate_excel(self, data):
               df = pd.DataFrame(data)
               excel_path = 'companies_report.xlsx'
               df.to_excel(excel_path, index=False)
               return excel_path
           
           def generate_pdf(self, data):
               pdf = FPDF()
               pdf.add_page()
               
               # Заголовок
               pdf.set_font('Arial', 'B', 16)
               pdf.cell(0, 10, 'Отчет по компаниям', 0, 1, 'C')
               
               # Данные
               pdf.set_font('Arial', '', 12)
               for company in data:
                   pdf.cell(0, 10, f"Название: {company['name']}", 0, 1)
                   pdf.cell(0, 10, f"Адрес: {company['address']}", 0, 1)
                   pdf.cell(0, 10, f"Телефон: {company['phone']}", 0, 1)
                   if company.get('website'):
                       pdf.cell(0, 10, f"Сайт: {company['website']}", 0, 1)
                   pdf.cell(0, 10, '', 0, 1)
               
               pdf_path = 'companies_report.pdf'
               pdf.output(pdf_path)
               return pdf_path
