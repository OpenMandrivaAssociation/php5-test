Summary:	Simple test suite for testing php5
Name:		php5-test
Version:	5.1.6
Release:	%mkrel 6
Group:		System/Servers
URL:		http://www.php.net
License:	PHP License
BuildRequires:	php-devel >= 5.1.6
Requires:	php-bz2
Requires:	php-calendar
Requires:	php-cli >= 5.1.6
Requires:	php-ctype
Requires:	php-curl
Requires:	php-dba
Requires:	php-dbase
Requires:	php-devel >= 5.1.6
Requires:	php-dom
Requires:	php-exif
Requires:	php-filepro
Requires:	php-ftp
Requires:	php-gd
Requires:	php-gettext
Requires:	php-gmp
Requires:	php-hash
Requires:	php-iconv
Requires:	php-imap
Requires:	php-ini >= 5.1.6
Requires:	php-ldap
Requires:	php-mbstring
Requires:	php-mcal
Requires:	php-mcrypt
Requires:	php-mhash
Requires:	php-mssql
Requires:	php-mysql
Requires:	php-mysqli
Requires:	php-odbc
Requires:	php-pcntl
Requires:	php-pcre
Requires:	php-pdo
Requires:	php-pdo_dblib
Requires:	php-pdo_mysql
Requires:	php-pdo_odbc
Requires:	php-pdo_pgsql
Requires:	php-pdo_sqlite
Requires:	php-pgsql
Requires:	php-posix
Requires:	php-pspell
Requires:	php-readline
Requires:	php-recode
Requires:	php-session
Requires:	php-shmop
Requires:	php-simplexml
Requires:	php-snmp
Requires:	php-soap
Requires:	php-sockets
Requires:	php-sqlite
Requires:	php-sysvmsg
Requires:	php-sysvsem
Requires:	php-sysvshm
Requires:	php-tidy
Requires:	php-tokenizer
Requires:	php-xml
Requires:	php-xmlreader
Requires:	php-xmlrpc
Requires:	php-xmlwriter
Requires:	php-xsl
# extra packages in main
#Requires:	php-cups
#Requires:	php-dbx
#Requires:	php-dio

#Requires:	php-eaccelerator
#Requires:	php-fam
#Requires:	php-fileinfo
#Requires:	php-idn
#Requires:	php-mailparse
#Requires:	php-sasl
#Requires:	php-ssh2
#Requires:	php-tclink
#Requires:	php-translit
#Requires:	php-xattr
#Requires:	php-xdebug
#Requires:	php-yp
BuildArch:	noarch
BuildRoot:	%{_tmppath}/%{name}-%{version}-buildroot

%description
This is a simple test suite for testing php5

%prep

%setup -c -T

%build

cat > php5-test << EOF
#!/bin/bash

TMPF=\`mktemp -d \$TMPDIR/php5-test-XXXXXX\`
mkdir -p \$TMPF/tmp
echo "Using directory \$TMPF to run tests"
cd \$TMPF
cp -a /usr/src/php-devel/* .
find extensions -type f -name '*.phpt' > bundled_extensions.txt
extra_extensions=\`find /usr/share/doc/php-* -type d -name 'tests' | grep -v pear | sed -e 's/\/tests//'\`
mkdir -p extra_extensions
cp -rp \$extra_extensions extra_extensions/
find extra_extensions -type f -name '*.phpt' > extra_extensions.txt

echo "==============================================================================="
echo "Running standard tests"
TEST_PHP_EXECUTABLE='/usr/bin/php' /usr/bin/php run-tests.php -q -d session.save_path="\$TMPF/tmp"

echo "==============================================================================="
echo "Running tests for the bundled extensions"
TEST_PHP_EXECUTABLE='/usr/bin/php' /usr/bin/php run-tests.php -d session.save_path="\$TMPF/tmp" -d soap.wsdl_cache_dir="\$TMPF/tmp" -l bundled_extensions.txt
echo "==============================================================================="
echo "Done... You must now evaluate any failed test."
echo "The failed tests are saved into the bundled_extensions.txt file"
echo "To run these tests again execute:"
echo "TEST_PHP_EXECUTABLE='/usr/bin/php' /usr/bin/php run-tests.php -d session.save_path=\"\$TMPF/tmp\" -d soap.wsdl_cache_dir=\"\$TMPF/tmp\" -l bundled_extensions.txt"

echo "==============================================================================="
echo "Running tests (if any) for the extra extensions"
TEST_PHP_EXECUTABLE='/usr/bin/php' /usr/bin/php run-tests.php -d session.save_path="\$TMPF/tmp" -d soap.wsdl_cache_dir="\$TMPF/tmp" -l extra_extensions.txt
echo "==============================================================================="
echo "Done... You must now evaluate any failed test."
echo "The failed tests are saved into the extra_extensions.txt file"
echo "To run these tests again execute:"
echo "TEST_PHP_EXECUTABLE='/usr/bin/php' /usr/bin/php run-tests.php -d session.save_path=\"\$TMPF/tmp\" -d soap.wsdl_cache_dir=\"\$TMPF/tmp\" -l extra_extensions.txt"

echo "==============================================================================="
echo " All tests has now been run."
echo " You must manually clean the created test directory, like so:"
echo " rm -rf \$TMPF"
echo "==============================================================================="

EOF

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot} 

install -d %{buildroot}%{_bindir}

install -m0755 php5-test %{buildroot}%{_bindir}

cat > README.MDK << EOF
The Mandriva PHP test suite
---------------------------

To run the test suite simply execute the %{_bindir}/php5-test 
script.

EOF

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files 
%defattr(-,root,root)
%doc README.MDK
%attr(0755,root,root) %{_bindir}/php5-test



%changelog
* Fri Sep 04 2009 Thierry Vignaud <tvignaud@mandriva.com> 5.1.6-6mdv2010.0
+ Revision: 430690
- rebuild

* Fri Aug 01 2008 Thierry Vignaud <tvignaud@mandriva.com> 5.1.6-5mdv2009.0
+ Revision: 258993
- rebuild

* Thu Jul 24 2008 Thierry Vignaud <tvignaud@mandriva.com> 5.1.6-4mdv2009.0
+ Revision: 246865
- rebuild

* Mon Feb 18 2008 Thierry Vignaud <tvignaud@mandriva.com> 5.1.6-2mdv2008.1
+ Revision: 171036
- rebuild
- fix "foobar is blabla" summary (=> "blabla") so that it looks nice in rpmdrake

* Wed Jan 02 2008 Olivier Blin <oblin@mandriva.com> 5.1.6-1mdv2008.1
+ Revision: 140723
- restore BuildRoot

  + Thierry Vignaud <tvignaud@mandriva.com>
    - kill re-definition of %%buildroot on Pixel's request
    - import php5-test


* Sun Aug 27 2006 Oden Eriksson <oeriksson@mandriva.com> 5.1.6-1
- updated for latest php-5.1.6

* Fri Jun 10 2005 Oden Eriksson <oeriksson@mandriva.com> 5.0.4-1mdk
- initial Mandriva package
