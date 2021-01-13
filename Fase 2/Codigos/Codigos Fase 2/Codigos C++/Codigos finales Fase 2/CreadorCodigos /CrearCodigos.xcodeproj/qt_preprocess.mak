#############################################################################
# Makefile for building: CrearCodigos.app/Contents/MacOS/CrearCodigos
# Generated by qmake (3.1) (Qt 5.15.1)
# Project:  CrearCodigos.pro
# Template: app
# Command: /usr/local/opt/qt/bin/qmake -o CrearCodigos.xcodeproj/project.pbxproj CrearCodigos.pro -spec macx-xcode
#############################################################################

MAKEFILE      = project.pbxproj

EQ            = =

MOC       = /usr/local/Cellar/qt/5.15.1/bin/moc
UIC       = /usr/local/Cellar/qt/5.15.1/bin/uic
LEX       = flex
LEXFLAGS  = 
YACC      = yacc
YACCFLAGS = -d
DEFINES       = -DQT_DEPRECATED_WARNINGS -DQT_NO_DEBUG -DQT_WIDGETS_LIB -DQT_GUI_LIB -DQT_CORE_LIB
INCPATH       = -I. -I/usr/local/include/opencv -I/usr/local/include -I/usr/local/Cellar/qt/5.15.1/lib/QtWidgets.framework/Headers -I/usr/local/Cellar/qt/5.15.1/lib/QtGui.framework/Headers -I/usr/local/Cellar/qt/5.15.1/lib/QtCore.framework/Headers -I. -I/Applications/Xcode.app/Contents/Developer/Platforms/MacOSX.platform/Developer/SDKs/MacOSX10.15.sdk/System/Library/Frameworks/OpenGL.framework/Headers -I/Applications/Xcode.app/Contents/Developer/Platforms/MacOSX.platform/Developer/SDKs/MacOSX10.15.sdk/System/Library/Frameworks/AGL.framework/Headers -I. -I/usr/local/Cellar/qt/5.15.1/mkspecs/macx-clang -F/usr/local/Cellar/qt/5.15.1/lib
DEL_FILE  = rm -f
MOVE      = mv -f

preprocess: compilers
clean preprocess_clean: compiler_clean

mocclean: compiler_moc_header_clean compiler_moc_objc_header_clean compiler_moc_source_clean

mocables: compiler_moc_header_make_all compiler_moc_objc_header_make_all compiler_moc_source_make_all

check: first

benchmark: first

compilers: moc_predefs.h moc_mainwindow.cpp ui_mainwindow.h
compiler_rcc_make_all:
compiler_rcc_clean:
compiler_moc_predefs_make_all: moc_predefs.h
compiler_moc_predefs_clean:
	-$(DEL_FILE) moc_predefs.h
moc_predefs.h: /usr/local/Cellar/qt/5.15.1/mkspecs/features/data/dummy.cpp
	/Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/bin/clang++ -pipe -stdlib=libc++ -O2 -std=gnu++11 -Wall -Wextra -dM -E -o moc_predefs.h /usr/local/Cellar/qt/5.15.1/mkspecs/features/data/dummy.cpp

compiler_moc_header_make_all: moc_mainwindow.cpp
compiler_moc_header_clean:
	-$(DEL_FILE) moc_mainwindow.cpp
moc_mainwindow.cpp: mainwindow.h \
		/usr/local/Cellar/qt/5.15.1/lib/QtWidgets.framework/Headers/QMainWindow \
		/usr/local/Cellar/qt/5.15.1/lib/QtWidgets.framework/Headers/QFileDialog \
		/usr/local/Cellar/qt/5.15.1/lib/QtCore.framework/Headers/QDir \
		/usr/local/Cellar/qt/5.15.1/lib/QtCore.framework/Headers/QFile \
		/usr/local/Cellar/qt/5.15.1/lib/QtGui.framework/Headers/QCloseEvent \
		/usr/local/Cellar/qt/5.15.1/lib/QtWidgets.framework/Headers/QMessageBox \
		/usr/local/Cellar/qt/5.15.1/lib/QtCore.framework/Headers/QSettings \
		/usr/local/include/opencv2/opencv.hpp \
		moc_predefs.h \
		/usr/local/Cellar/qt/5.15.1/bin/moc
	/usr/local/Cellar/qt/5.15.1/bin/moc $(DEFINES) --include '/Users/joseguerra/Desktop/CreadorCodigos /moc_predefs.h' -I/usr/local/Cellar/qt/5.15.1/mkspecs/macx-clang -I'/Users/joseguerra/Desktop/CreadorCodigos ' -I/usr/local/include/opencv -I/usr/local/include -I/usr/local/Cellar/qt/5.15.1/lib/QtWidgets.framework/Headers -I/usr/local/Cellar/qt/5.15.1/lib/QtGui.framework/Headers -I/usr/local/Cellar/qt/5.15.1/lib/QtCore.framework/Headers -I/Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/include/c++/v1 -I/Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/lib/clang/12.0.0/include -I/Applications/Xcode.app/Contents/Developer/Platforms/MacOSX.platform/Developer/SDKs/MacOSX10.15.sdk/usr/include -I/Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/include -F/usr/local/Cellar/qt/5.15.1/lib mainwindow.h -o moc_mainwindow.cpp

compiler_moc_objc_header_make_all:
compiler_moc_objc_header_clean:
compiler_moc_source_make_all:
compiler_moc_source_clean:
compiler_uic_make_all: ui_mainwindow.h
compiler_uic_clean:
	-$(DEL_FILE) ui_mainwindow.h
ui_mainwindow.h: mainwindow.ui \
		/usr/local/Cellar/qt/5.15.1/bin/uic
	/usr/local/Cellar/qt/5.15.1/bin/uic mainwindow.ui -o ui_mainwindow.h

compiler_rez_source_make_all:
compiler_rez_source_clean:
compiler_yacc_decl_make_all:
compiler_yacc_decl_clean:
compiler_yacc_impl_make_all:
compiler_yacc_impl_clean:
compiler_lex_make_all:
compiler_lex_clean:
compiler_clean: compiler_moc_predefs_clean compiler_moc_header_clean compiler_uic_clean 

