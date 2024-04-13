from flask import Flask, request, render_template, send_file
import os
from pyresparser import ResumeParser
import pandas as pd
import tempfile
import zipfile

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the uploads directory exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def process_resume(resume_file):
    # Save the resume file to a temporary location
    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_file:
        temp_file.write(resume_file.read())
        temp_file_path = temp_file.name

    # Process the resume from the temporary file
    data = ResumeParser(temp_file_path).get_extracted_data()
    name = data.get("name", "Not found")
    email = data.get("email", "Not found")
    ph_no = data.get("mobile_number", "Not found")
    skills = ", ".join(data.get("skills", []))
    
    # Check if company_names is a list before joining
    company_names = data.get("company_names", [])
    if isinstance(company_names, list):
        company_names = ", ".join(company_names)
    else:
        company_names = "Not found"
        
    college_name = data.get("college_name", "Not found")

    # Delete the temporary file
    os.unlink(temp_file_path)

    return [name, email, ph_no, skills, company_names, college_name]


def process_zip(zip_file):
    resume_data = []
    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        for filename in zip_ref.namelist():
            with zip_ref.open(filename) as resume_file:
                resume_data.append(process_resume(resume_file))
    return resume_data

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file part"
    
    file = request.files['file']
    
    if file.filename == '':
        return "No selected file"
    
    if file:
        filename = file.filename
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        # Process the uploaded zip file
        resume_data = process_zip(file_path)

        # Create a DataFrame with the extracted data
        df = pd.DataFrame(resume_data, columns=['Name', 'Email', 'Phone Number', 'Skills', 'Companies', 'College'])

        # Save DataFrame to Excel
        excel_file_path = os.path.join(tempfile.gettempdir(), 'extracted_data.xlsx')
        df.to_excel(excel_file_path, index=False)
        
        # Serve the Excel file for download
        
        return send_file(excel_file_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)

















# from flask import Flask, request, render_template, send_file
# import os
# from pyresparser import ResumeParser
# import pandas as pd
# import tempfile

# app = Flask(__name__)

# UPLOAD_FOLDER = 'uploads'
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# # Ensure the uploads directory exists
# if not os.path.exists(UPLOAD_FOLDER):
#     os.makedirs(UPLOAD_FOLDER)

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/upload', methods=['POST'])
# def upload_file():
#     if 'file' not in request.files:
#         return "No file part"
    
#     file = request.files['file']
    
#     if file.filename == '':
#         return "No selected file"
    
#     if file:
#         filename = file.filename
#         file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
#         file.save(file_path)
        
#         # Process the uploaded PDF file
#         data = ResumeParser(file_path).get_extracted_data()

#         name = data.get("name", "Not found")
#         email = data.get("email", "Not found")
#         ph_no = data.get("mobile_number", "Not found")
#         skills = ", ".join(data.get("skills", []))
#         company_names = ", ".join(data.get("company_names", []))
#         college_name = data.get("college_name", "Not found")

#         # Create a DataFrame with the extracted data
#         df = pd.DataFrame({
#             'Name': [name],
#             'Email': [email],
#             'Phone Number': [ph_no],
#             'Skills': [skills],
#             'Companies': [company_names],
#             'College': [college_name]
#         })

#         # Save DataFrame to Excel
#         excel_file_path = os.path.join(tempfile.gettempdir(), 'extracted_data.xlsx')
#         df.to_excel(excel_file_path, index=False)
        
#         # Serve the Excel file for download
#         return send_file(excel_file_path, as_attachment=True)

# if __name__ == '__main__':
#     app.run(debug=True)






















# import os
# from pyresparser import ResumeParser
# import warnings

# warnings.filterwarnings("ignore", category=UserWarning)

# # Path to the PDF file you want to process
# file_path = r"C:\Users\Anvith\Downloads\SampleResume\Sample2\ANVITH_PENDEKATLA.pdf"

# # Process the specified PDF file
# data = ResumeParser(file_path).get_extracted_data()

# name = data.get("name", "Not found")
# email = data.get("email", "Not found")
# ph_no = data.get("mobile_number", "Not found")
# skills = data.get("skills", [])
# company_names = data.get("company_names", [])
# college_name = data.get("college_name", "Not found")

# print("Resume:", os.path.basename(file_path))
# print("Name:", name)
# print("Email:", email)
# print("Phone Number:", ph_no)
# print("Skills:", ", ".join(skills))

# # Check if company_names is not None before joining
# if company_names:
#     print("Companies:", ", ".join(company_names))
# else:
#     print("Companies: Not found")

# print("College:", college_name)
# print("---------------------------------------")























# import os
# import pandas as pd
# from pyresparser import ResumeParser
# import warnings

# warnings.filterwarnings("ignore", category=UserWarning)

# # Path to the folder containing resumes
# folder_path = r"C:\Users\Anvith\Downloads\SampleResume\Sample2"

# # Initialize an empty list to store data from each resume
# resume_data = []

# # Iterate through all files in the folder
# for filename in os.listdir(folder_path):
#     if filename.endswith((".pdf", ".doc", ".docx")):
#         file_path = os.path.join(folder_path, filename)
#         data = ResumeParser(file_path).get_extracted_data()

#         name = data.get("name", "Not found")
#         email = data.get("email", "Not found")
#         ph_no = data.get("mobile_number", "Not found")
#         skills = ", ".join(data.get("skills", []))
        
#         # Check if company_names is a list before joining
#         company_names = data.get("company_names", [])
#         if isinstance(company_names, list):
#             company_names = ", ".join(company_names)
#         else:
#             company_names = "Not found"
        
#         college_name = data.get("college_name", "Not found")

#         # Append the data to the list
#         resume_data.append([name, email, ph_no, skills, company_names, college_name])

# # Create a DataFrame from the list
# df = pd.DataFrame(resume_data, columns=['Name', 'Email', 'Phone Number', 'Skills', 'Companies', 'College'])

# # Write the DataFrame to an Excel file
# excel_file_path = r"C:\Users\Anvith\Downloads\SampleResume\resumes_data.xlsx"
# df.to_excel(excel_file_path, index=False)

# print("Excel file created successfully:", excel_file_path)
