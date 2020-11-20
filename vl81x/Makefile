all: vl81x_fw.py

%.py: %.ksy
	kaitai-struct-compiler -t python $<

clean:
	rm -f vl81x_fw.py

.PHONY: all clean
