Summary:	A GNU source-level debugger for C, C++ and Fortran
Name:		gdb
Version:	7.7
Release:	1
License:	GPL v3
Group:		Development/Debuggers
Source0:	http://ftp.gnu.org/gnu/gdb/%{name}-%{version}.tar.bz2
# Source0-md5:	271a18f41858a7e98b28ae4eb91287c9
Patch1:		%{name}-pretty-print-by-default.patch
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	libtool
BuildRequires:	ncurses-devel
BuildRequires:	readline-devel
BuildRequires:	texinfo
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Gdb is a full featured, command driven debugger. Gdb allows you to
trace the execution of programs and examine their internal state at
any time. Gdb works for C and C++ compiled with the GNU C compiler
gcc.

%prep
%setup -q
%patch1 -p1

sed -i -e 's|@GDB_DATADIR_PATH@|@GDB_DATADIR@|' gdb/Makefile.in

rm -f gdb/ada-exp.c gdb/ada-lex.c gdb/c-exp.c gdb/cp-name-parser.c gdb/f-exp.c
rm -f gdb/jv-exp.c gdb/m2-exp.c gdb/objc-exp.c gdb/p-exp.c

%build
cp -f /usr/share/automake/config.* .
%configure \
	--disable-nls					\
	--disable-shared				\
	--with-cpu=%{_target_cpu}			\
	--with-python					\
	--with-pythondir=%{py_sitedir}			\
	--with-separate-debug-dir=/usr/lib/debug	\
	--with-system-readline				\
	--without-included-gettext			\
	--without-included-regex			\
	--without-x
%{__make}
%{__make} info

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_infodir}

%{__make} install install-info	\
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /usr/sbin/postshell
-/usr/sbin/fix-info-dir -c %{_infodir}

%postun	-p /usr/sbin/postshell
-/usr/sbin/fix-info-dir -c %{_infodir}

%files
%defattr(644,root,root,755)
%doc gdb/{ChangeLog,NEWS,PROBLEMS,README}
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_libdir}/libinproctrace.so
%{_datadir}/%{name}
%{_mandir}/man1/*
%{_infodir}/gdb*.info*
%{_infodir}/stabs*.info*

