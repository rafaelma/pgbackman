#
# Makefile
#

VERSION="1.0.0"

all:	clean html man pdf

html:	
	rst2html -gdt --stylesheet-path=style.css manual.rst > pgbackman-manual-$(VERSION).html
	rst2html -gdt --stylesheet-path=style.css manual_es.rst > pgbackman-manual-$(VERSION)_es.html

man:
	rst2man manual.rst > pgbackman-manual-$(VERSION).man
	rst2man manual_es.rst > pgbackman-manual-$(VERSION)_es.man

pdf:
	cat manual.rst | sed s/":scale: 50%"/":scale: 100%"/g > manual.tmp
	rst2pdf --output pgbackman-manual-$(VERSION).pdf manual.tmp
	rm -f manual.tmp
	cat manual_es.rst | sed s/":scale: 50%"/":scale: 100%"/g > manual_es.tmp
	rst2pdf --output pgbackman-manual-$(VERSION)_es.pdf manual_es.tmp
	rm -f manual_es.tmp
web:
	cp pgbackman-manual-$(VERSION).html www/pgbackman-manual-$(VERSION).html
	cp pgbackman-manual-$(VERSION).pdf www/pgbackman-manual-$(VERSION).pdf
	cp pgbackman-manual-$(VERSION).man www/pgbackman-manual-$(VERSION).man
	cp pgbackman-manual-$(VERSION)_es.html www/pgbackman-manual-$(VERSION)_es.html
	cp pgbackman-manual-$(VERSION)_es.pdf www/pgbackman-manual-$(VERSION)_es.pdf
	cp pgbackman-manual-$(VERSION)_es.man www/pgbackman-manual-$(VERSION)_es.man
	cp images/architecture.jpg www/images/architecture.jpg
	cp images/register_restore.jpg www/images/register_restore.jpg
	cp images/components.jpg www/images/components.jpg

clean:
	rm -f pgbackman-manual-$(VERSION)*.html
	rm -f pgbackman-manual-$(VERSION)*.man
	rm -f pgbackman-manual-$(VERSION)*.pdf
	rm -f *~
	rm -f www/pgbackman-manual-$(VERSION)*.html
	rm -f www/pgbackman-manual-$(VERSION)*.man
	rm -f www/pgbackman-manual-$(VERSION)*.pdf
	rm -f www/*~