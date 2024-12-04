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
        self.cell(0, 10, 'Robert Half Service Feedback', 0, 1, 'C')
        self.ln(10)

    def chapter_title(self, title):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, title, 0, 1, 'L')
        self.ln(4)

    def chapter_body(self, body):
        self.set_font('Arial', '', 12)
        self.multi_cell(0, 10, body)
        self.ln()

    def add_feedback(self, data):
        self.chapter_title("Overall Service Rating")
        self.chapter_body(str(data['Overall Rating'][0]))

        self.chapter_title("Feedback Summary")
        self.chapter_body(data['Feedback Summary'][0])

        self.chapter_title("Assessment Date")
        self.chapter_body(str(data['Assessment Date'][0]))

        self.chapter_title("Assessment Time")
        self.chapter_body(str(data['Assessment Time'][0]))

        self.chapter_title("Service Experience")
        self.chapter_body(data['Service Experience'][0])

        # Service Ratings
        self.chapter_title("Service Ratings")
        for criterion, rating in data['Service Ratings'][0].items():
            self.chapter_body(f"{criterion}: {rating}/10")

def download_pdf(data):
    pdf = PDF()
    pdf.add_page()
    pdf.add_feedback(data)

    pdf_output = BytesIO()
    pdf_str = pdf.output(dest='S').encode('latin1')
    pdf_output.write(pdf_str)
    pdf_output.seek(0)

    return pdf_output.read()

# Main function to run the app
def init_main():
    st.title("Rate Robert Half Staffing Solutions")

    st.markdown(
        '[Learn more about Robert Half Staffing Services](https://www.roberthalf.com/)'
    )

    # Input Fields for Service Feedback
    st.subheader("Service Feedback Form")
    overall_rating = st.slider("Rate your overall experience with Robert Half Staffing Solutions (1-5)", 1, 5)
    feedback_summary = st.text_area("Provide a summary of your feedback")
    assessment_date = st.date_input("Select the date of your assessment")
    assessment_time = st.time_input("Select the time of your assessment")
    service_experience = st.text_area("Describe your experience with Robert Half Staffing Solutions")

    # Criteria for scoring
    st.subheader("Rate Specific Aspects of the Service")
    service_criteria = [
        "Professionalism of Staff",
        "Clarity of Communication",
        "Response Time",
        "Knowledge of Industry",
        "Supportiveness During Recruitment",
        "Helpfulness in Finding Opportunities"
    ]

    # Collect ratings for each criterion
    service_ratings = {}
    for criterion in service_criteria:
        rating = st.slider(f"{criterion}", 0, 10, 5)
        service_ratings[criterion] = rating

    # Normalize data for consistent lengths
    max_length = 1  # Since it's a single user feedback session
    data = {
        "Overall Rating": [overall_rating] * max_length,
        "Feedback Summary": [feedback_summary] * max_length,
        "Assessment Date": [assessment_date] * max_length,
        "Assessment Time": [assessment_time] * max_length,
        "Service Experience": [service_experience] * max_length,
        "Service Ratings": [service_ratings] * max_length,
    }

    # Create DataFrame
    df = pd.DataFrame({
        "Overall Rating": [overall_rating],
        "Feedback Summary": [feedback_summary],
        "Assessment Date": [assessment_date],
        "Assessment Time": [assessment_time],
        "Service Experience": [service_experience],
        "Service Ratings": [service_ratings]
    })

    # CSV download
    csv = convert_df_to_csv(df)
    st.download_button(
        label="Download feedback as CSV",
        data=csv,
        file_name='robert_half_feedback.csv',
        mime='text/csv',
    )

    # PDF download
    pdf = download_pdf(data)
    st.download_button(
        label="Download feedback as PDF",
        data=pdf,
        file_name='robert_half_feedback.pdf',
        mime='application/octet-stream'
    )

if __name__ == '__main__':
    init_main()
