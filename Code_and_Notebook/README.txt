NASSAU CANDY DISTRIBUTOR
Factory Reallocation & Shipping Optimization Recommendation System
README

1. PROJECT OVERVIEW
This project is a data analytics and decision-support prototype for exploring
factory allocation and shipping optimization opportunities for Nassau Candy
Distributor.

The dashboard analyzes available order data, compares geographic distance
scenarios for candidate factories, displays preliminary recommendations, and
highlights data-quality and operational risks.

Important: This is a decision-support prototype. Distance estimates are not
verified road distances, shipping-time reductions, cost savings, or profit
forecasts. Factory changes must not be implemented without operational review
and approval.

2. PROJECT FOLDER STRUCTURE
Recommended structure:

file nusa/
|
|-- Code_and_Notebook/
|   |-- app.py
|   |-- app_backup.py
|   |-- requirements.txt
|   |-- Nassau_Factory_Optimization.ipynb
|   |-- README.txt
|
|-- Data_and_Exports/
|   |-- orders.csv
|   |-- recommendations.csv
|   |-- factory_locations.csv
|   |-- factory_mapping.csv
|   |-- destination_coverage.csv
|   |-- Other analysis and recommendation exports
|
|-- Dashboard_Screenshots/
|-- Project_Report/
    |-- Research paper
    |-- Executive summary
    |-- Final report (if applicable)

3. REQUIREMENTS
- Python 3.10 or another version compatible with the installed dependencies
- Streamlit
- pandas
- NumPy
- Plotly

The exact dependencies should be checked in requirements.txt.

4. DATA FILES
The dashboard expects these five CSV files in the Data_and_Exports folder:
- orders.csv
- recommendations.csv
- factory_locations.csv
- factory_mapping.csv
- destination_coverage.csv

The app.py file is configured to load them from the sibling Data_and_Exports
folder. In app.py, use:

    DATA_DIR = Path(__file__).parent.parent / "Data_and_Exports"

This path assumes app.py is inside Code_and_Notebook and Data_and_Exports is
next to Code_and_Notebook. If the folders are arranged differently, update
DATA_DIR accordingly.

Do not rename files unless you also update the paths in app.py. Ensure the CSV
files contain the columns required by the application.

5. HOW TO INSTALL
Open VS Code and open the Code_and_Notebook folder.

Open the integrated terminal in that folder and run:

    python -m venv .venv

Activate the environment on Windows:

    .venv\Scripts\activate

Install the required packages:

    pip install -r requirements.txt

If requirements.txt is incomplete, install the packages used by app.py:

    pip install streamlit pandas numpy plotly

6. HOW TO RUN THE DASHBOARD
From the Code_and_Notebook folder, run:

    streamlit run app.py

Then open the local address shown in the terminal, usually:

    http://localhost:8501

To stop the dashboard, return to the terminal and press Ctrl+C.

7. DASHBOARD MODULES
The current application contains four tabs:

- Factory Simulator:
  Compare candidate factories and estimated geographic distance differences
  for a selected product.

- What-If Scenarios:
  Compare current factory assignments with available distance-only alternatives.

- Recommendations:
  Review and download the filtered recommendation list. The ranking is
  illustrative and is not an optimized profit calculation.

- Risk & Impact:
  Review potential distance improvements, distance increases, limited evidence,
  and recommendations awaiting validation.

8. IMPORTANT LIMITATIONS
- Geographic distance estimates are not actual road-route distances.
- Shipping lead-time predictions are disabled until source dates and lead-time
  data are validated and a predictive model is properly evaluated.
- Profit impact is not calculated because candidate manufacturing costs,
  shipping costs, factory capacity, and product eligibility have not been
  validated.
- Destination mapping is incomplete. Unmapped records cannot support a reliable
  geographic comparison.
- A shorter straight-line distance does not guarantee faster delivery or lower
  shipping costs.
- Candidate recommendations require human review and final operational approval.

9. TROUBLESHOOTING
Error: "No such file or directory: ... orders.csv"
- Confirm that orders.csv exists in Data_and_Exports.
- Confirm that DATA_DIR in app.py points to the correct folder.
- Confirm the file name and extension are exactly correct.

Error: "ModuleNotFoundError"
- Activate the intended Python environment.
- Run: pip install -r requirements.txt

Error: missing column / KeyError
- Check that the CSV column names match what app.py expects.
- Use the project's intended CSV exports; do not substitute files with different
  schemas without updating and testing the code.

Dashboard changes are not visible:
- Save app.py.
- Refresh the browser.
- If needed, stop Streamlit with Ctrl+C and run it again.

10. FINAL VALIDATION CHECKLIST
[ ] All five required CSV files are present.
[ ] DATA_DIR points to Data_and_Exports.
[ ] requirements.txt dependencies install successfully.
[ ] Dashboard starts without CSV loading errors.
[ ] All four tabs open and filters work.
[ ] Recommendation downloads work.
[ ] Screenshots and final report documents are saved in their intended folders.
[ ] Results and limitations are explained accurately in the final presentation.

Project owner: [Enter your name]
Institution: [Enter your institution]
Submission date: [Enter date]
