import wikipedia as wiki
import re
from tensorflow_hub import load
import numpy as np

from wikipedia import PageError

threshold = 0.4
excluded_headings = ["see also", "notes", "references", "external links", "further reading"]


def init_model():
    module_url = "https://tfhub.dev/google/universal-sentence-encoder-large/5"
    global model
    model = load( module_url )


def embed(input):
    return model( input )

def subsection_helper(pg_content):
    orig = "==="
    repl = "+++"
    for _ in range( 8 ):
        pg_content = pg_content.replace( orig, repl )
        orig += "="
        repl += "+"
    return pg_content

def Candidate_intros(pages):  # takes a list values that will be given by similarity command of pre trained models
    candidate_secs = dict()
    section_to_content=dict()
    avgNumberofSections = 0
    for p, similarity_value in pages:

        try:
            pg_content = wiki.page( p ).content
        except PageError:
            print( p, file=open( "./ProblemWords.txt", "a" ) )
        except Exception as e:
            try:
                pg_content = wiki.page( e.options[0] ).content
            except Exception:
                continue

        if pg_content == "":
            continue

        pattern = '(?<=\n== )[^=]*(?= ==\n)'  # pattern to extract section headings
        # pattern = '[^=]*(?=\n)'  # pattern to extract introductory paragraph
        temp = re.findall( pattern, pg_content )
        pg_content=subsection_helper( pg_content )
        section_content_pattern='(?<= ==\n)[^=]*(?=)'
        section_content=re.findall(section_content_pattern,pg_content)
        assert len( section_content ) == len( temp )

        for s,con in zip(temp,section_content):
            if s.lower() in excluded_headings:
                continue
            avgNumberofSections += 1
            try:
                candidate_secs[s] += similarity_value
            except KeyError:
                candidate_secs[s] = similarity_value

            section_to_content[s] = con.strip()

    avgNumberofSections /= len( pages )
    return candidate_secs, int( avgNumberofSections ), section_to_content


def viableCandidate(word1, word2):
    vector1 = embed( [word1] )
    vector2 = embed( [word2] )
    return True if np.inner( vector1, vector2 ) > threshold else False
