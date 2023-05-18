from sqlalchemy import create_engine
from sqlalchemy import text
import pandas as pd
import os

# Load the database connection string from an environment variable.
# This is a secure way to configure the application - by not hardcoding the credentials in your source code.
connection_string = f'mysql+pymysql://{os.getenv("USERNAME")}:{os.getenv("PASSWORD")}@{os.getenv("HOST")}:{os.getenv("PORT")}/{os.getenv("DATABASE")}'

# Load the name of the database table from an environment variable.
TABLE_NAME = os.environ["TABLE_NAME"]
TABLE_NAME2 = os.environ["TABLE_NAME2"]

# Create an SQLAlchemy Engine that will interact with the database server.
# The connection string includes the type of the database and the connection details.
# The connect_args parameter allows for additional connection arguments to be passed.
# Here, we're configuring the engine to connect over SSL using certificate, key, and CA certificate
# that we've loaded from environment variables.
engine = create_engine(
  connection_string, connect_args={"ssl": {
    "ssl_ca": os.environ["SSL_CA"],
  }})
"""
@app.route('/')
@app.route('/<int:page_num>')
"""


# Define a function to load recent posts from the database.
def load_recent_posts(per_page, offset, labels):

  # The SQL query string is initially a SELECT statement on the table in TABLE_NAME.
  query = f"SELECT posttitle, postbody, postdate, postauthor, postlabels, postid FROM {TABLE_NAME} "

  # Add a WHERE clause to the query if labels is 1, indicating a filter for "blind" posts only.
  if labels == 1:
    query += "WHERE postlabels LIKE '%blind%' AND postlabels NOT LIKE '%reveal%' "

  # Add a WHERE clause to the query if labels is 2, indicating a filter for "reveal" posts only.
  elif labels == 2:
    query += "WHERE postlabels LIKE '%reveal%' "

  # Add an ORDER BY clause to sort by postunixtime in descending order, and a LIMIT clause to limit the number of results.
  # OFFSET clause is used to skip the number of rows before starting to return rows from the SQL query. Important for pagination.
  query += f"ORDER BY postunixtime DESC LIMIT {per_page} OFFSET {offset}"

  # Connect to the database and execute the query.
  with engine.connect() as conn:
    result = conn.execute(text(query))
    rows = result.fetchall()  # Fetch all rows returned by the query.

  posts = []  # List to store post data.

  # The names of the columns in the result.
  column_names = [
    'posttitle', 'postbody', 'postauthor', 'postdate', 'postlabels', 'postid'
  ]

  # For each row in the result set...
  for row in rows:
    # ...extract the data from the row into a list, in the same order as the column names...
    row_data = [
      row.posttitle, row.postbody, row.postdate, row.postauthor,
      row.postlabels, row.postid
    ]
    # ...zip the column names and the row data together into a dictionary...
    row_dict = dict(zip(column_names, row_data))
    # ...and append the dictionary to the list of posts.
    posts.append(row_dict)

  # Return the list of posts.
  return posts


"""
@app.route('/')
@app.route('/<int:page_num>')
"""


# Define a function to get the total number of recent posts that satisfy a certain condition, specified by labels.
def get_total_recent_posts(labels):

  # Initialize the SQL query string with a COUNT(*) statement, which counts the number of rows in TABLE_NAME.
  query = f"SELECT COUNT(*) FROM {TABLE_NAME} "

  # Add a WHERE clause to the query if labels is 1, indicating a condition for "blind" posts only.
  if labels == 1:
    query += "WHERE postlabels LIKE '%blind%' AND postlabels NOT LIKE '%reveal%' "

  # Add a WHERE clause to the query if labels is 2, indicating a condition for "reveal" posts only.
  elif labels == 2:
    query += "WHERE postlabels LIKE '%reveal%' "

  # Connect to the database and execute the query.
  with engine.connect() as conn:
    result = conn.execute(text(query))

    # Fetch the first row of the result (which is the count) and get the first column (index 0), which is the count itself.
    count = result.fetchone()[0]

  # Return the count.
  return count


"""
@app.route('/post/<int:post_id>')
"""


# Define a function to get a post by its ID.
def get_post_by_id(id):
  # Connect to the database.
  with engine.connect() as conn:
    # Execute a SQL query to select all columns of the row where the post id matches the given id.
    result = conn.execute(
      text(f"SELECT * FROM {TABLE_NAME} WHERE postid = {id}"))

  # Fetch the first row of the result, which should be the desired post.
  this_row = result.fetchone()

  # Define the column names, which will be the keys of the returned dictionary.
  column_names = [
    'postlink', 'postpreview', 'archivedate', 'archivelink', 'postcount',
    'archiveyear', 'postid', 'postchecklink', 'posthastitle', 'posttitle',
    'posthasbody', 'postbody', 'postauthor', 'posttime', 'postdate',
    'postlabels', 'posthasimages', 'postimagescount', 'postimageslinks',
    'posthasvideos', 'postvideoscount', 'postvideoslinks', 'postunixtime',
    'month'
  ]

  # Extract the data from the row into a list, in the same order as the column names.
  this_row_data = [
    this_row.postlink, this_row.postpreview, this_row.archivedate,
    this_row.archivelink, this_row.postcount, this_row.archiveyear,
    this_row.postid, this_row.postchecklink, this_row.posthastitle,
    this_row.posttitle, this_row.posthasbody, this_row.postbody,
    this_row.postauthor, this_row.posttime, this_row.postdate,
    this_row.postlabels, this_row.posthasimages, this_row.postimagescount,
    this_row.postimageslinks, this_row.posthasvideos, this_row.postvideoscount,
    this_row.postvideoslinks, this_row.postunixtime, this_row.month
  ]

  # Zip the column names and the row data together into a dictionary.
  this_row_dict = dict(zip(column_names, this_row_data))

  # Return the dictionary of posts.
  return this_row_dict


"""
@app.route('/search', methods=['POST', 'GET'])
@app.route('/search/<int:page_num>', methods=['POST', 'GET'])
"""


# Define a function to load posts filtered by a given search query, with pagination support.
def load_filtered_posts(input_text, limit, offset, labels):
  # Initialize the SQL query string with a SELECT statement that filters by the search query.
  query = f"SELECT * FROM {TABLE_NAME} WHERE postbody LIKE '%{input_text}%' "

  # Depending on the labels parameter, add a WHERE clause to filter by label type.
  if labels == 1:
    query += "AND postlabels LIKE '%blind%' AND postlabels NOT LIKE '%reveal%' "
  elif labels == 2:
    query += "AND postlabels LIKE '%reveal%' "

  # Append the ORDER BY, LIMIT, and OFFSET clauses for pagination.
  query += f"ORDER BY postunixtime DESC LIMIT {limit} OFFSET {offset}"

  # Connect to the database and execute the SQL query.
  with engine.connect() as conn:
    result = conn.execute(text(query))
    # Fetch all rows of the result.
    rows = result.fetchall()

  # Initialize an empty list to hold the post data.
  posts = []

  # Define the column names, which will be the keys of the returned dictionaries.
  column_names = [
    'postlink', 'postpreview', 'archivedate', 'archivelink', 'postcount',
    'archiveyear', 'postid', 'postchecklink', 'posthastitle', 'posttitle',
    'posthasbody', 'postbody', 'postauthor', 'posttime', 'postdate',
    'postlabels', 'posthasimages', 'postimagescount', 'postimageslinks',
    'posthasvideos', 'postvideoscount', 'postvideoslinks', 'postunixtime',
    'month'
  ]

  # For each row in the result set...
  for row in rows:
    # ...extract the data from the row into a list, in the same order as the column names...
    row_data = [
      row.postlink, row.postpreview, row.archivedate, row.archivelink,
      row.postcount, row.archiveyear, row.postid, row.postchecklink,
      row.posthastitle, row.posttitle, row.posthasbody, row.postbody,
      row.postauthor, row.posttime, row.postdate, row.postlabels,
      row.posthasimages, row.postimagescount, row.postimageslinks,
      row.posthasvideos, row.postvideoscount, row.postvideoslinks,
      row.postunixtime, row.month
    ]
    # ...zip the column names and the row data together into a dictionary...
    row_dict = dict(zip(column_names, row_data))
    # ...and append the dictionary to the list of posts.
    posts.append(row_dict)

  # Return the list of posts.
  return posts


"""
@app.route('/search', methods=['POST', 'GET'])
@app.route('/search/<int:page_num>', methods=['POST', 'GET'])
"""


# Define a function to get the total number of posts that match a given search query and label type.
def get_total_filtered_posts(input_text, labels):
  # Initialize the SQL query string with a SELECT COUNT(*) statement that filters by the search query.
  query = f"SELECT COUNT(*) FROM {TABLE_NAME} WHERE postbody LIKE '%{input_text}%' "

  # Depending on the labels parameter, add an AND clause to further filter by label type.
  if labels == 1:
    query += "AND postlabels LIKE '%blind%' AND postlabels NOT LIKE '%reveal%' "
  elif labels == 2:
    query += "AND postlabels LIKE '%reveal%' "

  # Connect to the database and execute the SQL query.
  with engine.connect() as conn:
    result = conn.execute(text(query))
    # Fetch the first (and only) row of the result and extract the first (and only) column, which is the count.
    count = result.fetchone()[0]

  # Return the count.
  return count


"""
@app.route('/data', methods=['GET', 'POST'])
"""


# Define a function to load a limited number of recent posts, with pagination support and optional label type filtering.
def load_limited_recent_posts(per_page, offset, labels=3):
  # Initialize the SQL query string with a SELECT statement.
  base_query = f"SELECT archiveyear, month FROM {TABLE_NAME} "
  filter_query = ""

  # Depending on the labels parameter, set the WHERE clause to filter by label type.
  if labels == 1:
    filter_query = "WHERE postlabels LIKE '%blind%' AND postlabels NOT LIKE '%reveal%' "
  elif labels == 2:
    filter_query = "WHERE postlabels LIKE '%reveal%' "

  # Append the WHERE clause (if any) and the LIMIT and OFFSET clauses to the SELECT statement.
  final_query = base_query + filter_query + f"LIMIT {per_page} OFFSET {offset}"

  # Connect to the database and execute the SQL query.
  with engine.connect() as conn:
    result = conn.execute(text(final_query))
    # Fetch all rows of the result.
    rows = result.fetchall()

  # Initialize an empty list to hold the post data.
  posts = []

  # Define the column names, which will be the keys of the returned dictionaries.
  column_names = ['archiveyear', 'month']

  # For each row in the result set...
  for row in rows:
    # ...extract the data from the row into a list, in the same order as the column names...
    row_data = [row.archiveyear, row.month]
    # ...zip the column names and the row data together into a dictionary...
    row_dict = dict(zip(column_names, row_data))
    # ...and append the dictionary to the list of posts.
    posts.append(row_dict)

  # Return the list of posts.
  return posts


"""
@app.route('/data/search', methods=['POST', 'GET'])
"""


# Function to load a limited number of posts filtered by the search text (input_text), with pagination and optional labels.
def load_limited_filtered_posts(input_text, limit, offset, labels=3):
  # Base SQL query to select data from the table based on a text match within the 'postbody' field.
  base_query = f"SELECT archiveyear, month FROM {TABLE_NAME} WHERE postbody LIKE '%{input_text}%' "
  filter_query = ""

  # Depending on the labels parameter, an additional filtering condition is appended to the query.
  if labels == 1:
    # Filter for posts labeled 'blind' but not 'reveal'.
    filter_query = "AND postlabels LIKE '%blind%' AND postlabels NOT LIKE '%reveal%' "
  elif labels == 2:
    # Filter for posts labeled 'reveal'.
    filter_query = "AND postlabels LIKE '%reveal%' "

  # The final query combines the base and filter queries and adds the LIMIT and OFFSET for pagination.
  final_query = base_query + filter_query + f"LIMIT {limit} OFFSET {offset}"

  # Connecting to the database and executing the SQL query.
  with engine.connect() as conn:
    result = conn.execute(text(final_query))
    # Fetching all rows from the result.
    rows = result.fetchall()

  # Initialize an empty list to store the post data.
  posts = []
  # List of column names, which will serve as keys in our returned dictionaries.
  column_names = ['archiveyear', 'month']

  # For each row in the result set...
  for row in rows:
    # ...extract the data for 'archiveyear' and 'month'...
    row_data = [row.archiveyear, row.month]
    # ..create a dictionary with keys as column names and corresponding row data as values...
    row_dict = dict(zip(column_names, row_data))
    # ...append the dictionary to the list of posts....abs
    posts.append(row_dict)

  # Return the list of posts.
  return posts


"""
app.route('/yougov')
"""


def get_gender_data():
  # Define the columns needed from the table
  cols = [
    "name", "gender", "frequency", "density", "cumulative_frequency",
    "male_flag", "female_flag", "male_frequency", "female_frequency",
    "male_running_ratio_by_frequency", "female_running_ratio_by_frequency"
  ]

  # Formulate the SQL query
  query = f"SELECT {', '.join(cols)} FROM {TABLE_NAME2} WHERE frequency >= 0"

  # Connect to the database and execute the SQL query, store the result in a pandas dataframe
  with engine.connect() as conn:
    df = pd.read_sql(query, conn)

  # Sort the dataframe by the cumulative frequency in ascending order
  df.sort_values(by='cumulative_frequency', ascending=True, inplace=True)

  # Compute total population statistics: total number, total male, total female
  total = len(df)
  total_male = df['male_flag'].sum()
  total_female = df['female_flag'].sum()

  # Filter out rows with zero frequency
  df2 = df[df['frequency'] > 0]

  # Compute statistics for the filtered population: total number, total male, total female
  non_zero_total = len(df2)
  non_zero_male = df2['male_flag'].sum()
  non_zero_female = df2['female_flag'].sum()

  # Compute post statistics for the filtered population: total posts, total male posts, total female posts
  non_zero_total_posts = df2['frequency'].sum()
  non_zero_male_posts = df2['male_frequency'].sum()
  non_zero_female_posts = df2['female_frequency'].sum()

  # Prepare lists for plotting: cumulative frequency, density, male running ratio, female running ratio, row numbers
  cumulative_frequency = df2['cumulative_frequency'].tolist()
  density = df2['density'].tolist()
  male_running_ratio = df2['male_running_ratio_by_frequency'].tolist()
  female_running_ratio = df2['female_running_ratio_by_frequency'].tolist()
  row_numbers = (df2.index + 1).tolist()

  # Prepare data for the gender table: index, name, gender, frequency, density
  df2['index'] = (df2.index + 1).tolist()
  gender_table = df2[['index', 'name', 'gender', 'frequency',
                      'density']].copy()

  # Return all the computed and prepared data
  return (cumulative_frequency, density, male_running_ratio,
          female_running_ratio, row_numbers, gender_table, total,
          non_zero_total, total_male, total_female, non_zero_male,
          non_zero_female, non_zero_total_posts, non_zero_male_posts,
          non_zero_female_posts)
