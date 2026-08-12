#import "@preview/moderner-cv:0.2.1": *
#import "@preview/chic-hdr:0.5.0": *

#let r = yaml("../data/cv.yaml")
#let author= r.profile.firstname + " " + r.profile.lastname

#show: chic.with(
  chic-footer(
    left-side: [#author],
    center-side: [#datetime.today().display("[year]-[month]-[day]")],
    right-side: [#chic-page-number()]
  ),
  chic-separator(0.5pt),
)

#show: moderner-cv.with(
  name: author,
  lang: "en",
  social: (
    // predefined socials: phone, email, github, linkedin, x, bluesky
    email: r.profile.email,
    github: "rsvaliveti",
    linkedin: "rvaliveti",
    // custom socials: (icon, link, body)
    // any fontawesome icon can be used: https://fontawesome.com/search
    website: ("link", "https://rsvaliveti.github.io", "rsvaliveti.github.io"),
    //address: "",
  ),
  image: none,
  paper: "us-letter",
  margin: (
    top: 15mm,
    bottom: 15mm,
    left: 15mm,
    right: 15mm
  ),
  show-footer: false,
)

= Experience

#for job in r.sections.experience {
  cv-entry-multiline(
    date: [#job.start_date -- #job.at("end_date", default: "Present")],
    employer: [#job.organization (#job.location)],
    title: [#job.position],
    [
      #list(..job.highlights)
    ]
  )
}

= Education

#for ed in r.sections.education {
 cv-entry(
  date: [#ed.start_date -- #ed.at("end_date", default: "Present")],
  employer: [#ed.institution (#ed.location)],
  title: [#ed.degree (#ed.area)],
  [#list(..ed.highlights)]
 )
}

= Awards

#for aw in r.sections.awards {
 cv-line(
  [#aw.start_date -- #aw.at("end_date", default: "")],
  [#aw.title. #aw.summary]
 )
}


// papers, patents

#v(8pt)
= Publications
#v(8pt)

#bibliography(
   "../data/papers.bib",
   title: none,
   full: true,
   group: "papers",
   style: "_csl/ieee-cv.csl", // The CSL file enforces reverse-chronological order perfectly!
  )


#v(8pt)
= Patents
#v(8pt)

#bibliography(
   "../data/patents.bib",
   title: none,
   full: true,
   group: "patents",
   style: "_csl/ieee-cv.csl", // The CSL file enforces reverse-chronological order perfectly!
  )

