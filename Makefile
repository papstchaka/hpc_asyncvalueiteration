TARNAME = async_value_iteration# chose a name for tar archive
HOST = localhost# host name of receiving operating system
USER = chaka# username on receiving operating system
PORT = 2222# port to use, should stay 2222


all:
	@echo "This is a dummy to prevent running make without explicit target!"

clean: remove_tarfile
	$(MAKE) -C src/ clean

pack: clean
	tar -czf $(TARNAME).tar.gz src/ Makefile

unpack:
	mkdir $(TARNAME)
	tar -zxvf $(TARNAME).tar.gz -C $(TARNAME)
	rm Makefile $(TARNAME).tar.gz
	cd $(TARNAME)

send: pack
	scp -P $(PORT) $(TARNAME).tar.gz $(USER)@$(HOST):~/

compile: clean
	$(MAKE) -C src/ compile

test:
	$(MAKE) -C src/ test

remove_tarfile:
	rm -f $(TARNAME).tar.gz

# to extract Makefile to be able to unpack files
# tar -zxvf ($TARNAME).tar.gz Makefile