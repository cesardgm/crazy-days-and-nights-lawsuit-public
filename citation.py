from datetime import datetime
"""
@app.route('/lawsuit')
"""


def generate_citations(title, author, url):
  # Extract the website from the URL by removing the protocol and everything after the first slash
  website = url.split('//')[-1].split('/')[0]

  # Get today's date and format it as "dd Mon. YYYY"
  access_date = datetime.today().strftime('%d %b. %Y')

  # Construct the MLA citation
  mla_citation = f'"{title}". {website}, by {author}, {url}. Accessed {access_date}.'

  # Define the publication date and format it as "YYYY, Month dd"
  publication_date = datetime(2023, 5, 14).strftime('%Y, %B %d')

  # Construct the APA citation
  apa_citation = f'{author}. ({publication_date}). {title}. {website}. Available at: {url}'

  # Pack both citations into a dictionary
  citations = {"mla": mla_citation, "apa": apa_citation}

  return citations
