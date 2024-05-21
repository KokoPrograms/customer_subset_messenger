<<<<<<< HEAD
# README.txt

## Targeted Marketing Messenger

### Submission for the Snowflake Arctic & Streamlit "The Future of AI is Open" Hackathon

---

### Overview

Targeted Marketing Messenger is an innovative application designed to enhance your marketing strategy by precisely segmenting customers and crafting tailored promotional messages. Leveraging Snowflake's Arctic LLM and Streamlit, this app allows you to query customer data, generate insightful SQL queries, and create personalized promotional messages to drive engagement and sales.

### Features

- **Customer Segmentation**: Easily find specific customer segments based on your criteria using natural language input.
- **SQL Query Generation**: The app translates natural language requests into accurate SQL queries, providing explanations in plain English.
- **Data Exploration**: Use interactive tabs to view customer subsets, spending breakdowns, and order history.
- **Promotional Messaging**: Craft personalized promotional messages and send them directly to your selected customer segments.

### How to Use

1. **Find Customers**:
   - Enter criteria to filter customers (e.g., "Find customers who spent over $200 in the last 6 months").
   - Click 'Find Customers' to apply the filter.
   - The app will generate an SQL query and explain it in plain English.

2. **Explore Data**:
   - Use the tabs to view customer subsets, spending breakdowns, and order history.
   - Click on a name in the customer list to view individual spending statistics and order history.

3. **Create Promotional Messages**:
   - Input promotional details (e.g., "Enjoy 10% off during happy hour from 4-6 PM").
   - Click 'Generate Message' to draft a message to send to your selected customers.
   - Edit if needed, then click 'Send Messages' to finalize.

4. **Menu**:
   - Click 'Menu' in the sidebar to view the product catalog.

### Searchable Parameters

- `Order Date`
- `Total Amount Spent`
- `Sales Channel`
    - (`Store`, `Market`, `Catering`)
- `Quantity of Items`
- `Price per Item`
- `Total Price per Item`
- `Product Category`
    - (`Pierogi`, `Main`, `Soup`, `Side`, `Dessert`, `Kompot`)

#### Example Queries

1. **Top Catering Spenders During Last Holiday Season**:
   - Find the top catering spenders during the last holiday season and send them a message to book early for this year.
   - Subset Criteria: "Find customers who spent the most on catering last holiday season."
   - Promotion Information: "Book early to grab your preferred date for this year!"

2. **Recent Customers with High Spending**:
   - Identify customers who spent over $500 in the last 3 months and send them a thank you message.
   - Subset Criteria: "Find customers who spent over $500 in the last 3 months."
   - Promotion Information: "Thank you for your recent purchases! Enjoy a 10% discount on your next visit."

3. **Customers with Multiple Orders**:
   - Find customers who placed more than 3 orders in the last year and offer them a loyalty discount.
   - Subset Criteria: "Find customers who placed more than 3 orders in the last year."
   - Promotion Information: "Thank you for being a loyal customer! Enjoy a 15% discount on your next order."

### Snowflake Arctic LLM Functions

1. Generates SQL queries based on customer subset criteria.
2. Explains the SQL query used in plain english for verification.
3. Drafts promotional messages based on provided information.

### Installation

1. Clone the repository.
2. Navigate to the project directory.
3. Create the conda environment: `conda env create -f environment.yml`
4. Activate the conda environment: `conda activate subset-messenger`
5. Generate new sales data (optional): `python3 generate_data.py`
6. Run the Streamlit app: `streamlit run app.py`

### Acknowledgments

This project was developed as part of the Snowflake Arctic & Streamlit "The Future of AI is Open" Hackathon. Special thanks to the organizers for providing the opportunity to explore and innovate with these powerful tools.

### Contact

Feel free to contact me at kamiltdembinski@gmail.com.

Thanks for checking out this demo!
- Kamil
=======
# subset-messenger
Snowflake Arctic &amp; Streamlit "The Future of AI is Open" Hackathon Submission
>>>>>>> origin/main
