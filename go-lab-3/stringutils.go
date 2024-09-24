package main

func reverseRow(str string) string {

	var strReverse string = ""

	for i := len(str) - 1; i >= 0; i-- {
		strReverse = strReverse + string(str[i])
	}

	return strReverse
}
