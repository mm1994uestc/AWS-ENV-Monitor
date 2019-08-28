#
# Softdog v1.21
# (C) Christophe Dupre 1998

CC	= gcc
BINNAME	= softdog
STRIP   = strip
#INCLUDE	= 
OPTIMIZE	= -O2 -fomit-frame-pointer -fno-strength-reduce
#DEBUG	= -g -DDEBUG
CFLAGS	= -Wall $(DEBUG) $(INCLUDE) $(OPTIMIZE)\
          -DDEVICE=\"$(DEVICE)\" -DMY_MAJOR=$(MAJOR) -DMY_MINOR=$(MINOR)\
          -DBINNAME=\"$(BINNAME)\"

# Installation paths
BINDIR	=/sbin
MANDIR	=/usr/man/man8

# Install program and options
INSTALL	=install 
BININSTALLOPTS	= -m0555
MANINSTALLOPTS	= -m0644
#INSTALL = cp

# mknod program
MKNOD	=mknod 

# Watchdog device info
DEVICE	=/dev/watchdog
MAJOR	=10
MINOR	=130
TYPE	=c

all: softdog

softdog: softdog.o
	$(CC) $(CFLAGS) -o $(BINNAME) $<
	$(STRIP) $(BINNAME)

install: softdog installbin installman installdev
installbin:
	$(INSTALL) $(BININSTALLOPTS) $(BINNAME) $(BINDIR)
installman:
	$(INSTALL) $(MANINSATALLOPTS) softdog.8 $(MANDIR)
installdev:
	rm -f $(DEVICE)
	$(MKNOD) $(DEVICE) $(TYPE) $(MAJOR) $(MINOR)
	
clean:
	rm -f *.[oas] *~ core $(BINNAME) 
