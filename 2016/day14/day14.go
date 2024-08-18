package day14

import (
	"crypto/md5"
	"encoding/hex"
	"slices"
	"strconv"
)

const NumKeysNeeded = 64
const MaxIndexDistance = 1000
const NumStretchRounds = 2016

type indexInfo struct {
	hash   string
	threes []rune
	fives  []rune
}

type Cache struct {
	salt     string
	items    []indexInfo
	itemsExt []indexInfo
}

func FindRepeats(hash string, length int) []rune {
	symbols := []rune(hash)
	if len(symbols) < length {
		panic("unexpected hash size!")
	}

	result := []rune{}
	for offset := length - 1; offset < len(symbols); offset++ {
		ok := true
		for j := 1; j < length; j++ {
			if symbols[offset-j] != symbols[offset] {
				ok = false
				break
			}
		}
		if ok && !slices.Contains(result, symbols[offset]) {
			result = append(result, symbols[offset])
		}
	}
	return result
}

func (c *Cache) isKeyValid(index int) bool {
	c.storeIndex(index)
	threes := c.items[index].threes
	if len(threes) > 0 {
		for i := 0; i < MaxIndexDistance; i++ {
			index++
			c.storeIndex(index)
			fives := c.items[index].fives
			ok := slices.Contains(fives, threes[0])
			if ok {
				return true
			}
		}
	}
	return false
}

func (c *Cache) isKeyValidExt(index int) bool {
	c.storeIndex(index)
	threes := c.itemsExt[index].threes
	if len(threes) > 0 {
		for i := 0; i < MaxIndexDistance; i++ {
			index++
			c.storeIndex(index)
			fives := c.itemsExt[index].fives
			ok := slices.Contains(fives, threes[0])
			if ok {
				return true
			}
		}
	}
	return false
}

func (c *Cache) storeIndex(index int) {
	for index >= len(c.items) {
		key := c.salt + strconv.Itoa(index)
		hashBytes := md5.Sum([]byte(key))
		hashStr := hex.EncodeToString(hashBytes[:])
		threes := FindRepeats(hashStr, 3)
		fives := FindRepeats(hashStr, 5)
		c.items = append(c.items, indexInfo{
			hashStr,
			threes,
			fives,
		})
		hashStrExt := hashStr
		for i := 0; i < NumStretchRounds; i++ {
			hashBytes = md5.Sum([]byte(hashStrExt))
			hashStrExt = hex.EncodeToString(hashBytes[:])
		}
		threesExt := FindRepeats(hashStrExt, 3)
		fivesExt := FindRepeats(hashStrExt, 5)
		c.itemsExt = append(c.itemsExt, indexInfo{
			hashStrExt,
			threesExt,
			fivesExt,
		})
	}
}

func cacheInit(salt string) *Cache {
	return &Cache{salt, []indexInfo{}, []indexInfo{}}
}

func GenerateKeys(salt string, ext bool) (index int) {

	cache := cacheInit(salt)

	numFound := 0
	for numFound < NumKeysNeeded {
		var ok bool
		if !ext {
			ok = cache.isKeyValid(index)
		} else {
			ok = cache.isKeyValidExt(index)
		}
		if !ok {
			index++
			continue
		}
		numFound++
		if numFound < NumKeysNeeded {
			index++
		}
	}

	return
}
