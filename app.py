from flask import Flask, render_template, request, url_for
from database import get_gender_data, load_recent_posts, get_post_by_id, load_filtered_posts, get_total_recent_posts, get_total_filtered_posts, load_limited_recent_posts, load_limited_filtered_posts
from barchart import create_bar_chart
from citation import generate_citations

app = Flask(__name__)


# The app route decorator maps the URL '/' and '/<int:page_num>' to the function home_func.
@app.route('/')
@app.route('/<int:page_num>')
# This function is called when the user navigates to the root URL or a URL with a page number.
# The default page number is 1.
def home_func(page_num=1):
  # Define the number of posts to display per page.
  per_page = 6
  # Calculate the offset based on the page number, which is useful for pagination in database queries.
  offset = (page_num - 1) * per_page

  # Get the label from the request's query parameters. If none is provided, the default is 3 ('All' posts).
  labels = int(request.args.get('labels', 3))

  # Load the recent posts based on the per page limit, offset, and labels.
  BLINDS = load_recent_posts(per_page, offset, labels)
  # Get the total number of recent posts with the specified labels.
  TOTAL_BLINDS = get_total_recent_posts(labels)
  # Render and return an HTML page (index.html), passing the posts, page number, per page limit,
  # total posts count, current path, and labels as context variables to the template.
  return render_template('root/index.html',
                         posts=BLINDS,
                         page_num=page_num,
                         per_page=per_page,
                         total=TOTAL_BLINDS,
                         current_path=request.path,
                         labels=labels)


# The app route decorator maps the URL '/post/<int:post_id>' to the function view_post.
@app.route('/post/<int:post_id>')
def view_post(post_id):
  # Retrieves a post by its ID.
  post = get_post_by_id(post_id)
  # Renders the 'post.html' template and passes the retrieved post to it.
  return render_template('post/post.html', post=post)


# The app route decorator maps the URL '/search' and '/search/<int:page_num>' to the function search_func,
# allowing both POST and GET methods.
@app.route('/search', methods=['POST', 'GET'])
@app.route('/search/<int:page_num>', methods=['POST', 'GET'])
def search_func(page_num=1):
  # Checks if the request method is POST.
  if request.method == 'POST':
    # Retrieves the search query and the labels from the form data.
    search_query = request.form['search_query']
    labels = request.form.get('labels', 3)
    # If labels are not provided, sets the default to 3.
    labels = int(labels) if labels else 3
  else:
    # If the request method is not POST, retrieves the search query and labels from the URL parameters.
    search_query = request.args.get('search_query', '')
    labels = int(request.args.get('labels', 3))

  # Defines the number of posts to display per page.
  per_page = 6
  # Calculates the offset based on the page number for pagination.
  offset = (page_num - 1) * per_page

  # Retrieves the posts based on the search query, number of posts per page, offset, and labels.
  BLINDS = load_filtered_posts(search_query, per_page, offset, labels)
  # Gets the total number of posts based on the search query and labels.
  TOTAL_BLINDS = get_total_filtered_posts(search_query, labels)
  # Renders the 'index.html' template, passing the posts, page number, number of posts per page,
  # total number of posts, search query, and labels to it.
  return render_template('root/index.html',
                         posts=BLINDS,
                         page_num=page_num,
                         per_page=per_page,
                         total=TOTAL_BLINDS,
                         search_query=search_query,
                         labels=labels)


# The app route decorator maps the URL '/data' to the function data_func,
# allowing both GET and POST methods.
@app.route('/data', methods=['GET', 'POST'])
def data_func():
  # Defines the limit and offset for the data retrieval.
  no_limit = 100_000
  no_offset = 0

  # Checks if the request method is POST.
  if request.method == 'POST':
    # Retrieves the search query, toggle state, and labels from the form data.
    search_query = request.form.get('search_query', '')
    toggle = request.args.get('toggle', '0') == '1'
    labels = request.form.get('labels', 3)
    # If labels are not provided, sets the default to 3.
    labels = int(labels) if labels else 3
  else:
    # If the request method is not POST, retrieves the search query, toggle state, and labels from the URL parameters.
    search_query = request.args.get('search_query', '')
    toggle = request.args.get('toggle', '0') == '1'
    labels = int(request.args.get('labels', 3))

  # Retrieves the posts based on the limit, offset, and labels.
  BLINDS = load_limited_recent_posts(no_limit, no_offset, labels)
  # Creates a bar chart based on the retrieved posts and the toggle state.
  values, counts = create_bar_chart(BLINDS, toggle)

  # Renders the 'data.html' template, passing the values, counts, toggle state, current path, search query, and labels to it.
  return render_template('data/data.html',
                         values=values,
                         counts=counts,
                         toggle=toggle,
                         current_path=request.path,
                         search_query=search_query,
                         labels=labels)


# The app route decorator maps the URL '/data/search' to the function data_search_func,
# allowing both POST and GET methods.
@app.route('/data/search', methods=['POST', 'GET'])
def data_search_func():
  # Defines the limit and offset for the data retrieval.
  no_limit = 100_000
  no_offset = 0

  # Checks if the request method is POST.
  if request.method == 'POST':
    # Retrieves the search query, toggle state, and labels from the form data.
    search_query = request.form['search_query']
    toggle = request.args.get('toggle', '0') == '1'
    labels = request.form.get('labels', 3)
    # If labels are not provided, sets the default to 3.
    labels = int(labels) if labels else 3
  else:
    # If the request method is not POST, retrieves the search query, toggle state, and labels from the URL parameters.
    search_query = request.args.get('search_query', '')
    toggle = request.args.get('toggle', '0') == '1'
    labels = int(request.args.get('labels', 3))

  # Retrieves the posts based on the search query, limit, offset, and labels.
  BLINDS = load_limited_filtered_posts(search_query, no_limit, no_offset,
                                       labels)
  # Creates a bar chart based on the retrieved posts and the toggle state.
  values, counts = create_bar_chart(BLINDS, toggle)

  # Renders the 'data.html' template, passing the values, counts, toggle state, current path, search query, and labels to it.
  return render_template('data/data.html',
                         values=values,
                         counts=counts,
                         toggle=toggle,
                         current_path=request.path,
                         search_query=search_query,
                         labels=labels)


# This decorator maps the URL '/lawsuit' to the function lawsuit_func.
# So, when the Flask application receives a GET request for the URL '/lawsuit', it calls this function.
@app.route('/lawsuit')
def lawsuit_func():
  # Here, 'title' is set to "Crazy Days and Nights Lawsuit" and 'author' is set to "OpenAI's GPT-4"
  title = "Crazy Days and Nights Lawsuit"
  author = "OpenAI's GPT-4"

  # This function call generates the citations based on the title, author, and the current URL.
  # The generated citations are stored in the 'citations' variable.
  citations = generate_citations(title, author, request.url)

  # The function then renders and returns the 'lawsuit.html' template with the 'citations' variable passed into it.
  return render_template('lawsuit/lawsuit.html', citations=citations)


# This decorator maps the URL '/yougov' to the function yougov_func.
# So, when the Flask application receives a GET request for the URL '/yougov', it calls this function.
@app.route('/yougov')
def yougov_func():
  # This function call retrieves various statistical data related to gender.
  # The returned data is stored in multiple variables.
  (cumulative_frequency, density, male_running_ratio, female_running_ratio,
   row_numbers, gender_table, total, non_zero_total, total_male, total_female,
   non_zero_male, non_zero_female, non_zero_total_posts, non_zero_male_posts,
   non_zero_female_posts) = get_gender_data()

  # This line converts the 'gender_table' dataframe to a dictionary format.
  gender_table = gender_table.to_dict('records')

  # The function then renders and returns the 'yougov.html' template with all the variables passed into it.
  return render_template('yougov/yougov.html',
                         cumulative_frequency=cumulative_frequency,
                         density=density,
                         male_running_ratio=male_running_ratio,
                         female_running_ratio=female_running_ratio,
                         row_numbers=row_numbers,
                         gender_table=gender_table,
                         total=total,
                         total_male=total_male,
                         total_female=total_female,
                         non_zero_total=non_zero_total,
                         non_zero_male=non_zero_male,
                         non_zero_female=non_zero_female,
                         non_zero_total_posts=non_zero_total_posts,
                         non_zero_male_posts=non_zero_male_posts,
                         non_zero_female_posts=non_zero_female_posts)


if __name__ == "__main__":
  app.run(host='0.0.0.0', port=10000, debug=False)
