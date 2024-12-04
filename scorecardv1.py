import streamlit as st
import pandas as pd
from io import BytesIO
from fpdf import FPDF

# Function to convert the dataframe to a CSV
def convert_df_to_csv(df):
    return df.to_csv(index=False).encode('utf-8')

# Function to generate a PDF
class PDF(FPDF):
    def __init__(self):
        super().__init__()
        self.set_left_margin(21)
        self.set_right_margin(21)

    def header(self):
        self.set_font('Arial', 'B', 14)
        self.cell(0, 10, 'Robert Half Score Card', 0, 1, 'C')
        self.ln(10)

    def chapter_title(self, title):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, title, 0, 1, 'L')
        self.ln(4)

    def chapter_body(self, body):
        self.set_font('Arial', '', 12)
        self.multi_cell(0, 10, body)
        self.ln()

    def add_score_card(self, data):
        self.chapter_title("Overall Rating")
        self.chapter_body(str(data['Overall Rating'][0]))

        self.chapter_title("Feedback Summary")
        self.chapter_body(data['Feedback Summary'][0])

        self.chapter_title("Assessment Date")
        self.chapter_body(str(data['Assessment Date'][0]))

        self.chapter_title("Assessment Time")
        self.chapter_body(str(data['Assessment Time'][0]))

        # Employee ratings
        self.chapter_title("Performance Ratings")
        for criterion, rating in data['Performance Ratings'][0].items():
            self.chapter_body(f"{criterion}: {rating}/10")

        self.chapter_title("Recruitment Feedback")
        self.chapter_body(data['Recruitment Feedback'][0])

        # Employee Names Involved
        self.chapter_title("Involved Staff")
        for name in data['Employee Names']:
            self.chapter_body(name)

def download_pdf(data):
    pdf = PDF()
    pdf.add_page()
    pdf.add_score_card(data)

    pdf_output = BytesIO()
    pdf_str = pdf.output(dest='S').encode('latin1')
    pdf_output.write(pdf_str)
    pdf_output.seek(0)

    return pdf_output.read()

# Main function to run the app
def init_main():
    st.title("Robert Half Score Card Tool")

    st.markdown(
        '[Learn more about Robert Half Staffing Services](https://www.roberthalf.com/)'
    )

    # Customer experience inputs
    overall_rating = st.slider("Rate the overall service (1-5)", 1, 5)
    feedback_summary = st.text_area("Provide a summary of your feedback")
    assessment_date = st.date_input("Select the date of assessment")
    assessment_time = st.time_input("Select the time of assessment")
    recruitment_feedback = st.text_area("Feedback on recruitment process")

    # Section for adding employee names
    st.subheader("Enter Employee Names Involved")

    # Initialize session state for employee names
    if "employee_names" not in st.session_state:
        st.session_state.employee_names = []

    # Input area for employee names
    new_employee_name = st.text_input("Enter the name of an employee:")
    add_employee_button = st.button("Add Employee")

    # Add employee name on button click
    if add_employee_button and new_employee_name:
        st.session_state.employee_names.append(new_employee_name)
        st.success(f"Employee '{new_employee_name}' added!")
        new_employee_name = ""  # Clear input

    # Display current list of employee names
    if st.session_state.employee_names:
        st.markdown("### Employees Involved:")
        for i, name in enumerate(st.session_state.employee_names):
            st.write(f"{i + 1}. {name}")

    # Criteria for scoring
    st.subheader("Rate Employee Performance")
    performance_criteria = [
        "Professionalism",
        "Responsiveness",
        "Attention to Detail",
        "Client Interaction",
        "Problem Solving",
        "Knowledge of Industry"
    ]

    # Collect ratings for each criterion
    performance_ratings = {}
    for criterion in performance_criteria:
        rating = st.slider(f"{criterion}", 0, 10, 5)
        performance_ratings[criterion] = rating

    # Data dictionary
    data = {
        "Overall Rating": [overall_rating],
        "Feedback Summary": [feedback_summary],
        "Assessment Date": [assessment_date],
        "Assessment Time": [assessment_time],
        "Performance Ratings": [performance_ratings],
        "Recruitment Feedback": [recruitment_feedback],
        "Employee Names": st.session_state.employee_names
    }

    df = pd.DataFrame(data)

    # CSV download
    csv = convert_df_to_csv(df)
    st.download_button(
        label="Download data as CSV",
        data=csv,
        file_name='robert_half_score_card.csv',
        mime='text/csv',
    )

    # PDF download
    pdf = download_pdf(data)
    st.download_button(
        label="Download data as PDF",
        data=pdf,
        file_name='robert_half_score_card.pdf',
        mime='application/octet-stream'
    )

if __name__ == '__main__':
    init_main()
