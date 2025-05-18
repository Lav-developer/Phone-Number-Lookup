# Phone-Number-Lookup

Description
Phone Number Lookup is a web application built with Streamlit that allows users to search for detailed information about phone numbers, including carrier, location, timezone, number type, and a calculated spam score. Users can also contribute to an in-memory database to enrich phone number data. The app prioritizes privacy by storing data only in-memory during the session.
Try it live at phone-check.streamlit.app.
Features

Phone Number Analysis: Retrieve details like country, city, carrier, timezone, and number type (e.g., Mobile, VoIP) using the phonenumbers library.
Spam Score Calculation: Estimates the likelihood of a number being spam based on patterns like repetitive or sequential digits.
Data Contribution: Users can add or update phone number details, including name, carrier, and city.
Search History: View past searches with expandable details.
JSON Export: Download search results as a JSON file.
Privacy-Focused: All data is stored in-memory, ensuring no persistent storage.

Installation
To run the project locally, follow these steps:
Prerequisites

Python 3.8+
Git

Steps

Clone the repository:git clone https://github.com/Lav-developer/Phone-Number-Lookup.git


Navigate to the project directory:cd Phone-Number-Lookup


Create a virtual environment (optional but recommended):python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate


Install dependencies:pip install -r requirements.txt


Run the Streamlit app:streamlit run app.py


Open your browser and visit http://localhost:8501.

Usage

Search Phone Numbers:
Enter a phone number (e.g., +1234567890) in the "Search Phone Number" section.
Click "Search" to view details like carrier, location, timezone, number type, and spam score.
Download results as a JSON file.


Contribute Data:
In the "Contribute Phone Number Data" section, enter a phone number, carrier, and optional name/city.
Submit to update or add to the in-memory database.


View Search History:
Check the "Your Search History" section to review past searches with expandable details.



Contributing
Contributions are welcome! To contribute:

Fork the repository.
Create a new branch:git checkout -b feature/your-feature


Make your changes and commit:git commit -m "Add your feature"


Push to your branch:git push origin feature/your-feature


Open a pull request on GitHub.

Please ensure your code follows the project's coding style and includes appropriate tests.
License
This project is licensed under the MIT License. See the LICENSE file for details.
Contact
For questions or feedback, reach out to:

Developer: Lav Kush
Portfolio: lav-developer.netlify.app
GitHub: Lav-developer

Acknowledgments

Built with Streamlit and phonenumbers.
Hosted on Streamlit Community Cloud.


