# Makefile
# 4/3/2015 jichi
# Note: The source code MUST be compiled under Korean code page (CP949).
# Or user-defined pre/post filters and userdict will not work.
.PHONY: all clean compile config

BUILD_DIR = build
PREFIX_DIR = install

# Temporary files to put build files
ifeq ($(OS),Windows_NT)
  BOOST_HOME = z:/local/windows/developer/boost/build
else
  BOOST_HOME = $(HOME)/opt/boost
endif

# Tool chain
#CMAKE_GENERATOR = Visual Studio 12 2013
CMAKE_GENERATOR = Visual Studio 10 2010

all: compile
	@echo targets: compile clean

clean:
	rm -Rf $(BUILD_DIR)

compile: config
	cmake --build $(BUILD_DIR) \
	  --config Release \
	  --target install

$(BUILD_DIR):
	mkdir $@

config: $(BUILD_DIR)
	cd $(BUILD_DIR) && cmake \
	  -DCMAKE_BUILD_TYPE=RELEASE \
	  -G "$(CMAKE_GENERATOR)" \
	  -DBOOST_ROOT=$(BOOST_HOME) \
	  -DCMAKE_INSTALL_PREFIX=$(PREFIX_DIR) \
	  $(CURDIR)

# EOF
