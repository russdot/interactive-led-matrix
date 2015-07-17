
# "Frankenstein" AVR make file

####################################################
### change these to match your programmer!
####################################################

### use these for AVRISP mk II
#AVRDUDE_PROGRAMMERID=avrisp2
#AVRDUDE_PORT= usb 

### use these three options if using FTDI cable, but
### change the port to match your cable!
#AVRDUDE_PROGRAMMERID=avrisp
#AVRDUDE_PORT= /dev/tty.usbserial-XXXXXXX
#AVRDUDE_EXTRA = -b19200 -F


### use these for adafruit programmer
#AVRDUDE_PROGRAMMERID=usbtiny
#AVRDUDE_PORT= usb 



####################################################

PROJECTNAME=video-peggy-twi
MCU=atmega168
F_CPU = 16000000UL

####################################################



PRJSRC=main.c

INC=
# libraries to link in (e.g. -lmylib)
LIBS=
OPTLEVEL=s

#standard printf
PRINTF_LIB_STD = -Wl,-u,vfprintf 

# Minimalistic printf version
PRINTF_LIB_MIN = -Wl,-u,vfprintf -lprintf_min

# Floating point printf version (requires MATH_LIB = -lm below)
PRINTF_LIB_FLOAT = -Wl,-u,vfprintf -lprintf_flt

PRINTF_LIB =  

DEFS = -DF_CPU=$(F_CPU)

MATH_LIB = -lm
SCANF_LIB = 

HEXFORMAT=ihex

####################################################


SIZE = avr-size

HEXSIZE = $(SIZE) --target=$(FORMAT) $(PROJECTNAME).hex
ELFSIZE = $(SIZE) -A $(PROJECTNAME).elf


#  other possible flags: -fno-exceptions  -adhlns=$(<:.c=.lst)     ,-ahlms=
# -gstabs   forces lsting

# compiler
CFLAGS= -c  -I$(INC) -I. -mmcu=$(MCU) -O$(OPTLEVEL) -std=gnu99 \
	-fpack-struct -fshort-enums  -fno-exceptions \
	-funsigned-bitfields -funsigned-char    \
	-Wall             \
	$(DEFS)  \
	-gstabs \
	-Wa,-ahlnsd=$(firstword                  \
	$(filter %.lst, $(<:.c=.lst)))

CSPECFLAGS = -Wstrict-prototypes
	
# c++ specific flags
CPPFLAGS=-fno-exceptions               \
	-Wa,-ahlms=$(firstword         \
	$(filter %.lst, $(<:.cpp=.lst))\
	$(filter %.lst, $(<:.cc=.lst)) \
	$(filter %.lst, $(<:.C=.lst)))

# assembler
ASMFLAGS =-I. $(INC) -mmcu=$(MCU)        \
	-x assembler-with-cpp            \
	-Wa,-gstabs,-ahlms=$(firstword   \
		$(<:.S=.lst) $(<.s=.lst))


# linker
LDFLAGS=-Wl,-Map,$(TRG).map -mmcu=$(MCU) $(PRINTF_LIB) $(MATH_LIB) $(SCANF_LIB) $(LIBS)

##### executables ####
CC=avr-gcc
OBJCOPY=avr-objcopy
OBJDUMP=avr-objdump
SIZE=avr-size
AVRDUDE=avrdude
REMOVE=rm -f

##### automatic target names ####
TRG=$(PROJECTNAME).out
DUMPTRG=$(PROJECTNAME).s

HEXROMTRG=$(PROJECTNAME).hex 
HEXTRG=$(HEXROMTRG) 
		####$(PROJECTNAME).ee.hex

# Define all object files.

# Start by splitting source files by type
#  C++

CPPFILES=$(filter %.cpp, $(PRJSRC))
CCFILES=$(filter %.cc, $(PRJSRC))
BIGCFILES=$(filter %.C, $(PRJSRC))
#  C
CFILES=$(filter %.c, $(PRJSRC))
#  Assembly
ASMFILES=$(filter %.S, $(PRJSRC))


# List all object files we need to create
OBJDEPS=$(CFILES:.c=.o)    \
	$(CPPFILES:.cpp=.o) \
	$(BIGCFILES:.C=.o) \
	$(CCFILES:.cc=.o)  \
	$(ASMFILES:.S=.o)

# Define all lst files.
LST=$(filter %.lst, $(OBJDEPS:.o=.lst))

# All the possible generated assembly 
# files (.s files)
GENASMFILES=$(filter %.s, $(OBJDEPS:.o=.s)) 

.SUFFIXES : .c .cc .cpp .C .o .out .s .S \
	.hex .ee.hex .h .hh .hpp


#.PHONY: writeflash clean stats



# Make targets:
# all, disasm, stats, hex, writeflash/install, clean


	

all: $(TRG)

disasm: $(DUMPTRG) stats

program: all stats writeflash 
#stats

run:all
debug:all

stats: $(TRG)
#	$(OBJDUMP) -h $(TRG)
	$(SIZE) $(TRG) 

hex: $(HEXTRG)

writeflash: hex
ifndef AVRDUDE_PROGRAMMERID
	@echo " "
	@echo "Please edit the Makefile to set up your AVR programmer or FTDI cable"
	@echo " "
else
	$(AVRDUDE) -c $(AVRDUDE_PROGRAMMERID)   \
	 -p $(MCU) -P $(AVRDUDE_PORT) -e $(AVRDUDE_EXTRA)   \
	 -U flash:w:$(HEXROMTRG)
endif


install: writeflash

$(DUMPTRG): $(TRG) 
	$(OBJDUMP) -S  $< > $@


$(TRG): $(OBJDEPS) 
	$(CC) $(LDFLAGS) -o $(TRG) $(OBJDEPS)


#### Generating assembly ####
# asm from C
%.s: %.c
	$(CC) -S $(CFLAGS) $(CSPECFLAGS) $< -o $@

# asm from (hand coded) asm
%.s: %.S
	$(CC) -S $(ASMFLAGS) $< > $@


# asm from C++
.cpp.s .cc.s .C.s :
	$(CC) -S $(CFLAGS) $(CPPFLAGS) $< -o $@


#### Generating object files ####
# object from C
.c.o: 
	$(CC) $(CFLAGS) $(CSPECFLAGS) -c $< -o $@

# object from C++ (.cc, .cpp, .C files)
.cc.o .cpp.o .C.o :
	$(CC) $(CFLAGS) $(CPPFLAGS) -c $<

# object from asm
.S.o :
	$(CC) $(ASMFLAGS) -c $< -o $@


# generate hex files from elf
.out.hex:
	$(OBJCOPY) -j .text                    \
		-j .data                       \
		-O $(HEXFORMAT) $< $@

.out.ee.hex:
	$(OBJCOPY) -j .eeprom                  \
		--change-section-lma .eeprom=0 \
		-O $(HEXFORMAT) $< $@


clean:
	$(REMOVE) $(TRG) $(TRG).map $(DUMPTRG)
	$(REMOVE) $(OBJDEPS)
	$(REMOVE) $(LST) $(GDBINITFILE)
	$(REMOVE) $(GENASMFILES)
	$(REMOVE) $(HEXTRG)
