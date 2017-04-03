from eventor_toolkit import Eventor

e = Eventor("APIKEY")
results = e.results_per_organisation(646, 17395)
print(results)
