import sys

algorithms = set(["regex", "xpath"])
websites = set(["rtvslo.si", "overstock.com", "mimovrste.com"])
pages = set(["1","2"])

wpnames = {website : [] for website in websites}
wpnames["rtvslo.si"].append("Audi A6 50 TDI quattro_ nemir v premijskem razredu - RTVSLO.si.html")
wpnames["rtvslo.si"].append("Volvo XC 40 D4 AWD momentum_ suvereno med najboljše v razredu - RTVSLO.si.html")
wpnames["overstock.com"].append("jewelry01.html")
wpnames["overstock.com"].append("jewelry02.html")
wpnames["mimovrste.com"].append("item01.html")
wpnames["mimovrste.com"].append("item02.html")

if __name__ == "__main__":
	if len(sys.argv) > 3:
		passed = True
		if sys.argv[1] not in algorithms:
			passed = False
			print("Unknown algorithm: " + sys.argv[1])
			print("Possible values are: [" + "|".join(algorithms) + "]")
		if sys.argv[2] not in websites:
			passed = False
			print("Unknown website: " + sys.argv[2])
			print("Possible values are: [" + "|".join(websites) + "]")
		if sys.argv[3] not in pages:
			passed = False
			print("Unknown webpage number: " + sys.argv[3])
			print("Possible values are: [" + "|".join(pages) + "]")
		
		if passed:
			npage = int(sys.argv[3])-1
			jsonOutput = ""
			systemInput = None			

			if sys.argv[1] == "regex":
				import regex as alg
				systemInput = alg.stringify_file(sys.argv[2]+"/"+wpnames[sys.argv[2]][npage])
			elif sys.argv[1] == "xpath":
				import xpath as alg
				systemInput = alg.get_root(sys.argv[2]+"/"+wpnames[sys.argv[2]][npage])
			
			if sys.argv[2] == "rtvslo.si":
				jsonOutput = alg.rtvslo(systemInput)
			elif sys.argv[2] == "overstock.com":
				jsonOutput = alg.overstock(systemInput)
			elif sys.argv[2] == "mimovrste.com":
				jsonOutput = alg.mimovrste(systemInput)

			print(jsonOutput)
	else:
		print("Not enough parameters")
		print("Function should be called with three parameters")
		print("main.py #algorithm #website #page")
		print("where")
		print("#algorithm = [" + "|".join(algorithms) + "]")
		print("#website   = [" + "|".join(websites) + "]")
		print("#page      = [" + "|".join(pages) + "]")
