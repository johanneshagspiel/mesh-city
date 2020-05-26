from range_key_dict import RangeKeyDict

test = {
	range(0, 100) : {
		range (0, 100) : "hello"
	}
}

test[range(100, 200)] = {range(100,200) : "foo"}

temp = (test[key] for key in test if 100 in key)

print(next(temp))
