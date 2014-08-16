%global commit_hash 52af1f2
%global tag_hash f2d7914
%global sofile_version 1.2

Name:    jffi
Version: 1.2.6
Release: 8%{?dist}
Summary: An optimized Java interface to libffi 

Group:   System Environment/Libraries
License: LGPLv3+ or ASL 2.0
URL:     http://github.com/jnr/%{name}/
Source0: https://github.com/jnr/%{name}/tarball/%{version}/jnr-%{name}-%{version}-0-g%{commit_hash}.tar.gz
Patch0:  jffi-fix-dependencies-in-build-xml.patch
Patch1:  jffi-add-built-jar-to-test-classpath.patch
Patch2:  jffi-fix-compilation-flags.patch

BuildRequires: java-devel
BuildRequires: jpackage-utils
BuildRequires: libffi-devel

BuildRequires: ant
BuildRequires: ant-junit
BuildRequires: junit

Requires: jpackage-utils

%description
An optimized Java interface to libffi 

%prep
%setup -q -n jnr-%{name}-%{tag_hash}
%patch0
%patch1
%patch2

# ppc{,64} fix
# https://bugzilla.redhat.com/show_bug.cgi?id=561448#c9
sed -i.cpu -e '/m\$(MODEL)/d' jni/GNUmakefile libtest/GNUmakefile

# remove uneccessary directories
rm -rf archive/* jni/libffi/ jni/win32/ lib/CopyLibs/ lib/junit*

find ./ -name '*.jar' -exec rm -f '{}' \; 
find ./ -name '*.class' -exec rm -f '{}' \; 

%build
build-jar-repository -s -p lib/ junit

ant -Duse.system.libffi=1

%install
mkdir -p $RPM_BUILD_ROOT%{_libdir}/%{name}
mkdir -p $RPM_BUILD_ROOT%{_jnidir}/

cp -p dist/%{name}-complete.jar $RPM_BUILD_ROOT%{_jnidir}/%{name}.jar

install -d -m 755 $RPM_BUILD_ROOT%{_mavenpomdir}
install -pm 644 pom.xml  \
        $RPM_BUILD_ROOT%{_mavenpomdir}/JPP-%{name}.pom

%add_maven_depmap JPP-%{name}.pom %{name}.jar

%check
# skip tests on s390 until https://bugzilla.redhat.com/show_bug.cgi?id=1084914 is resolved
%ifnarch s390
# don't fail on unused parameters... (TODO: send patch upstream)
sed -i 's|-Werror||' libtest/GNUmakefile
ant -Duse.system.libffi=1 test
%endif

%files -f .mfiles
%doc COPYING.GPL COPYING.LESSER LICENSE
%{_jnidir}/%{name}.jar
%{_mavenpomdir}/JPP-%{name}.pom

%changelog
* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.6-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Thu Jun 12 2014 Alexander Kurtakov <akurtako@redhat.com> 1.2.6-7
- Fix FTBFS.

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.6-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Apr 07 2014 Dan Horák <dan[at]danny.cz> - 1.2.6-5
- skip tests on s390 until https://bugzilla.redhat.com/show_bug.cgi?id=1084914 is resolved

* Fri Mar 28 2014 Michael Simacek <msimacek@redhat.com> - 1.2.6-4
- Use Requires: java-headless rebuild (#1067528)

* Sun Aug 11 2013 Mat Booth <fedora@matbooth.co.uk> - 1.2.6-3
- Remove BR on ant-nodeps, fixes FTBFS rhbz #992622

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Feb 05 2013 Bohuslav Kabrda <bkabrda@redhat.com> - 1.2.6-1
- Updated to version 1.2.6.

* Wed Dec 19 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.0.10-4
- revbump after jnidir change

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Aug 02 2011  Mo Morsi <mmorsi@redhat.com> - 1.0.10-1
- Updated to most recent upstream release

* Wed Jun 01 2011  Mo Morsi <mmorsi@redhat.com> - 1.0.9-1
- Updated to most recent upstream release

* Mon Oct 25 2010  <mmorsi@redhat.com> - 1.0.2-1
- Updated to most recent upstream release

* Wed Apr 14 2010  <mmorsi@redhat.com> - 0.6.5-4
- added Mamoru Tasaka's fix for ppc{,64} to prep

* Mon Mar 08 2010  <mmorsi@redhat.com> - 0.6.5-3
- fixes to jffi from feedback
- don't strip debuginfo, remove extraneous executable bits,

* Tue Feb 23 2010  <mmorsi@redhat.com> - 0.6.5-2
- fixes to jffi compilation process
- fixes to spec to conform to package guidelines

* Wed Feb 17 2010  <mmorsi@redhat.com> - 0.6.5-1
- bumped version
- fixed package to comply to fedora guidelines

* Tue Jan 19 2010  <mmorsi@redhat.com> - 0.6.2-1
- Initial build.
