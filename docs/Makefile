#
# Makefile
#

VERSION="1.0.0"

all:	clean html man pdf

html:	
	rst2html -gdt --stylesheet-path=style.css manual.rst > pgbackman-manual-$(VERSION).html

man:
	rst2man manual.rst > pgbackman-manual-$(VERSION).man

pdf:
	cat manual.rst | sed s/":scale: 50%"/":scale: 100%"/g > manual.tmp
	rst2pdf --output pgbackman-manual-$(VERSION).pdf manual.tmp
	rm -f manual.tmp

web:
	cp pgbackman-manual-$(VERSION).html www/pgbackman-manual-$(VERSION).html
	cp pgbackman-manual-$(VERSION).pdf www/pgbackman-manual-$(VERSION).pdf
	cp pgbackman-manual-$(VERSION).man www/pgbackman-manual-$(VERSION).man
	cp images/architecture.jpg www/images/architecture.jpg
	cp images/register_restore.jpg www/images/register_restore.jpg

clean:
	rm -f pgbackman-manual-$(VERSION).html
	rm -f pgbackman-manual-$(VERSION).man
	rm -f pgbackman-manual-$(VERSION).pdf
	rm -f *~
	rm -f www/pgbackman-manual-$(VERSION).html
	rm -f www/pgbackman-manual-$(VERSION).man
	rm -f www/pgbackman-manual-$(VERSION).pdf
	rm -f www/*~