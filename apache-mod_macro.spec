#Module-Specific definitions
%define mod_name mod_macro
%define mod_conf 30_%{mod_name}.conf
%define mod_so %{mod_name}.so

Summary:	DSO module for the apache web server
Name:		apache-%{mod_name}
Version:	1.2.1
Release:	1
Group:		System/Servers
License:	BSD-style
URL:		http://www.coelho.net/mod_macro/
Source0:	http://www.cri.ensmp.fr/~coelho/mod_macro/%{mod_name}-%{version}.tar.gz
Source1:	%{mod_conf}
Requires(pre): rpm-helper
Requires(postun): rpm-helper
Requires(pre):	apache-conf >= 2.2.0
Requires(pre):	apache >= 2.2.0
Requires:	apache-conf >= 2.2.0
Requires:	apache >= 2.2.0
BuildRequires:	apache-devel >= 2.2.0
BuildRequires:	file
Epoch:		1

%description
mod_macro allows the definition and use of macros within apache
runtime configuration files. The syntax is a natural extension to
apache html-like configuration style.

%prep
%setup -q -n %{mod_name}-%{version}

cp %{SOURCE1} %{mod_conf}

# strip away annoying ^M
find . -type f|xargs file|grep 'CRLF'|cut -d: -f1|xargs perl -p -i -e 's/\r//'
find . -type f|xargs file|grep 'text'|cut -d: -f1|xargs perl -p -i -e 's/\r//'

%build
%{_bindir}/apxs -c mod_macro.c

%install
install -d %{buildroot}%{_libdir}/apache-extramodules
install -d %{buildroot}%{_sysconfdir}/httpd/modules.d

install -m0755 .libs/*.so %{buildroot}%{_libdir}/apache-extramodules/
install -m0644 %{mod_conf} %{buildroot}%{_sysconfdir}/httpd/modules.d/

# fix strange permissions
chmod 644 *

%post
if [ -f %{_var}/lock/subsys/httpd ]; then
    %{_initrddir}/httpd restart 1>&2;
fi

%postun
if [ "$1" = "0" ]; then
    if [ -f %{_var}/lock/subsys/httpd ]; then
	%{_initrddir}/httpd restart 1>&2
    fi
fi

%files
%doc CHANGES INSTALL README mod_macro.html
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/modules.d/%{mod_conf}
%attr(0755,root,root) %{_libdir}/apache-extramodules/%{mod_so}


%changelog
* Sat Feb 11 2012 Oden Eriksson <oeriksson@mandriva.com> 1:1.1.11-4mdv2012.0
+ Revision: 772684
- rebuild

* Tue May 24 2011 Oden Eriksson <oeriksson@mandriva.com> 1:1.1.11-3
+ Revision: 678343
- mass rebuild

* Sun Oct 24 2010 Oden Eriksson <oeriksson@mandriva.com> 1:1.1.11-2mdv2011.0
+ Revision: 588028
- rebuild

* Sun Oct 17 2010 Oden Eriksson <oeriksson@mandriva.com> 1:1.1.11-1mdv2011.0
+ Revision: 586380
- 1.1.11

* Mon Mar 08 2010 Oden Eriksson <oeriksson@mandriva.com> 1:1.1.10-6mdv2010.1
+ Revision: 516146
- rebuilt for apache-2.2.15

* Sat Aug 01 2009 Oden Eriksson <oeriksson@mandriva.com> 1:1.1.10-5mdv2010.0
+ Revision: 406615
- rebuild

* Tue Jan 06 2009 Oden Eriksson <oeriksson@mandriva.com> 1:1.1.10-4mdv2009.1
+ Revision: 326082
- rebuild

* Mon Jul 14 2008 Oden Eriksson <oeriksson@mandriva.com> 1:1.1.10-3mdv2009.0
+ Revision: 235052
- rebuild

* Thu Jun 05 2008 Oden Eriksson <oeriksson@mandriva.com> 1:1.1.10-2mdv2009.0
+ Revision: 215606
- fix rebuild

* Sat May 10 2008 Oden Eriksson <oeriksson@mandriva.com> 1:1.1.10-1mdv2009.0
+ Revision: 205389
- 1.1.10

* Fri Mar 07 2008 Oden Eriksson <oeriksson@mandriva.com> 1:1.1.8-5mdv2008.1
+ Revision: 181802
- rebuild

* Mon Feb 18 2008 Thierry Vignaud <tv@mandriva.org> 1:1.1.8-4mdv2008.1
+ Revision: 170735
- rebuild
- fix "foobar is blabla" summary (=> "blabla") so that it looks nice in rpmdrake
- kill re-definition of %%buildroot on Pixel's request

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

* Sat Sep 08 2007 Oden Eriksson <oeriksson@mandriva.com> 1:1.1.8-3mdv2008.0
+ Revision: 82614
- rebuild


* Sat Mar 10 2007 Oden Eriksson <oeriksson@mandriva.com> 1.1.8-2mdv2007.1
+ Revision: 140718
- rebuild

* Thu Nov 09 2006 Oden Eriksson <oeriksson@mandriva.com> 1:1.1.8-1mdv2007.0
+ Revision: 79463
- Import apache-mod_macro

* Sat Aug 26 2006 Oden Eriksson <oeriksson@mandriva.com> 1:1.1.8-1mdv2007.0
- 1.1.8

* Mon Jul 03 2006 Oden Eriksson <oeriksson@mandriva.com> 1:1.1.7-1mdv2007.0
- 1.1.7
- drop the advertizing patch, better fix upstream

* Fri Dec 16 2005 Oden Eriksson <oeriksson@mandriva.com> 1:1.1.6-2mdk
- rebuilt against apache-2.2.0

* Mon Nov 28 2005 Oden Eriksson <oeriksson@mandriva.com> 1:1.1.6-1mdk
- fix versioning

* Sun Jul 31 2005 Oden Eriksson <oeriksson@mandriva.com> 2.0.54_1.1.6-2mdk
- fix deps

* Fri Jun 03 2005 Oden Eriksson <oeriksson@mandriva.com> 2.0.54_1.1.6-1mdk
- rename the package
- the conf.d directory is renamed to modules.d
- use new rpm-4.4.x pre,post magic

* Sun Mar 20 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 2.0.53_1.1.6-4mdk
- use the %1

* Mon Feb 28 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 2.0.53_1.1.6-3mdk
- fix %%post and %%postun to prevent double restarts
- fix bug #6574

* Wed Feb 16 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 2.0.53_1.1.6-2mdk
- spec file cleanups, remove the ADVX-build stuff

* Tue Feb 08 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 2.0.53_1.1.6-1mdk
- rebuilt for apache 2.0.53

* Wed Sep 29 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 2.0.52_1.1.6-1mdk
- built for apache 2.0.52

* Fri Sep 17 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 2.0.51_1.1.6-1mdk
- built for apache 2.0.51

* Wed Sep 01 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 2.0.50_1.1.6-1mdk
- 1.1.6

* Tue Jul 13 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 2.0.50_1.1.5-1mdk
- built for apache 2.0.50
- remove redundant provides

* Tue Jun 15 2004 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.49_1.1.5-1mdk
- built for apache 2.0.49

