
dictio = {"A": 1, "B": 2}

dictio["A"]
dictio["B"]

len(dictio)

dictio["Lulu"] = 18
dictio["B"] = 66

del dictio["Lulu"]

dictio.items()
dictio.values()

dictio.update({"A": 4, "B": 22})


d = {
	"Nora": {
		"age": 15,
		"weight": 67,
		"height": 158
	},
	"Gino": {
		"age": 17,
		"weight": 80,
		"height": 160
	}
}


d["Nora"]["age"]
d["Gino"]["weight"]

d["Nora"]["age"] = 16