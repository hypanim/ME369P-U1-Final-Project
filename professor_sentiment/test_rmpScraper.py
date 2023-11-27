from universityScraper import universityScraper
from professorScraper import professorScraper
import os
from pathlib import Path
import pickle

testScraper1 = universityScraper()
testScraper1.getProfessors()

testScraper2 = professorScraper()
testScraper2.getReviews()
