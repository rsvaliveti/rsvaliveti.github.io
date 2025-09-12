---
title: Self-organizing Doubly-linked Lists

# Authors
# A YAML list of author names
# If you created a profile for a user (e.g. the default `admin` user at `content/authors/admin/`), 
# write the username (folder name) here, and it will be replaced with their full name and linked to their profile.
authors:
- R. S. Valiveti
- B. J. Oommen

# Author notes (such as 'Equal Contribution')
# A YAML list of notes for each author in the above `authors` list
author_notes: []

date: '1993-01-01'

# Date to publish webpage (NOT necessarily Bibtex publication's date).
publishDate: '2024-10-19T02:19:31.655670Z'

# Publication type.
# A single CSL publication type but formatted as a YAML list (for Hugo requirements).
publication_types:
- article-journal

# Publication name and optional abbreviated publication name.
publication: ''
publication_short: ''

#doi: https://doi.org/10.1006/jagm.1993.1005

abstract: In this paper, we study the problem of maintaining a doubly-linked list
  (DLL) in approximately optimal order, with respect to the mean search time. We study
  two types of DLL reorganization strategies. Move-To-End (MTE) [12] and SWAP [14]
  are two memoryless DLL heuristics obtained from natural extensions of the well-known
  singly-linked-list (SLL) heuristics, move-to-front and transposition, respectively.
  We first derive a general sufficient condition which permits comparison of any two
  DLL heuristics. We use this condition as a guideline to identify families of access
  distributions for which SWAP yields a lower expected cost than the MTE. We have
  also presented an absorbing DLL heuristic. The strategy requires one additional
  memory location and is analogous to the scheme presented in [15]. The reorganization
  is achieved by moving each element exactly once to its final position in the reorganized
  list. The scheme is stochastically absorbing and it is shown to be optimal for a
  restricted family of distributions. Thus, for these distributions, the probability
  of the scheme converging to the optimal list order can be made as close to unity
  as desired.

# Summary. An optional shortened abstract.
summary: ''

tags: []

# Display this page in a list of Featured pages?
featured: false

# Links
url_pdf: ''
url_code: ''
url_dataset: ''
url_poster: ''
url_project: ''
url_slides: ''
url_source: ''
url_video: ''

# Custom links (uncomment lines below)
# links:
# - name: Custom Link
#   url: http://example.org

# Publication image
# Add an image named `featured.jpg/png` to your page's folder then add a caption below.
image:
  caption: ''
  focal_point: ''
  preview_only: false

# Associated Projects (optional).
#   Associate this publication with one or more of your projects.
#   Simply enter your project's folder or file name without extension.
#   E.g. `projects: ['internal-project']` links to `content/project/internal-project/index.md`.
#   Otherwise, set `projects: []`.
projects: []
links:
- name: URL
  url: http://www.sciencedirect.com/science/article/pii/S0196677483710059
---

Add the **full text** or **supplementary notes** for the publication here using Markdown formatting.
