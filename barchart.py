from collections import Counter
"""
@app.route('/data', methods=['GET', 'POST'])
@app.route('/data/search', methods=['POST', 'GET'])
"""


def create_bar_chart(table, toggle):
  # If the toggle is False, we generate data for a yearly count bar chart
  if toggle == False:
    # Extract the archive year from each post
    postyears = [post['archiveyear'] for post in table]

    # Count the number of posts by year using a Counter
    year_counts = Counter(postyears)

    # Get the unique years and their corresponding counts
    years = sorted(year_counts.keys())
    counts = [year_counts[year] for year in years]

    # Calculate the final cumulative sum of the counts
    cum_sum = sum(counts)

    # The x-values for the bar chart are the years
    values = years
    return values, counts, cum_sum

  # If the toggle is True, we generate data for a monthly count bar chart
  else:
    # Extract the month and archive year from each post and create a string in the format "month-year"
    post_year_months = [
      f"{post['month']}-{post['archiveyear']}" for post in table
    ]

    # Count the number of posts by year and month using a Counter
    year_month_counts = Counter(post_year_months)

    # Get the unique year-month combinations and their corresponding counts
    year_months = sorted(year_month_counts.keys(),
                         key=lambda x:
                         (int(x.split('-')[1]), int(x.split('-')[0])
                          ))  # sort by year and then by >

    counts = [year_month_counts[year_month] for year_month in year_months]

    # Calculate the final cumulative sum of the counts
    cum_sum = sum(counts)

    # The x-values for the bar chart are the year-month combinations
    values = year_months
    return values, counts, cum_sum
