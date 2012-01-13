%global git_commit 5874d2a
%global cluster wmeissner

Name:    jffi
Version: 1.0.10
Release: 2%{?dist}
Summary: An optimized Java interface to libffi 

Group:   System Environment/Libraries
License: LGPLv3
URL:     http://github.com/%{cluster}/%{name}
Source0: https://download.github.com/%{cluster}-%{name}-%{version}-0-g%{git_commit}.tar.gz
Patch0:  fix_dependencies_in_build_xml.patch
Patch1:  fix_jar_dependencies.patch
Patch2:  fix_compilation_flags.patch

BuildRequires: java-devel >= 1:1.6.0
BuildRequires: jpackage-utils
BuildRequires: libffi-devel
BuildRequires: ant
BuildRequires: ant-nodeps
BuildRequires: ant-junit
BuildRequires: junit4
Requires: java >= 1:1.6.0
Requires: jpackage-utils

%description
An optimized Java interface to libffi 

%package javadoc
Summary:        Javadocs for %{name}
Group:          Documentation
Requires:       %{name} = %{version}-%{release}
Requires:       jpackage-utils

%description javadoc
This package contains the API documentation for %{name}.

%prep
%setup -q -n %{cluster}-%{name}-%{git_commit}
%patch0
%patch1
%patch2

# ppc{,64} fix
# https://bugzilla.redhat.com/show_bug.cgi?id=561448#c9
sed -i.cpu -e '/m\$(MODEL)/d' jni/GNUmakefile libtest/GNUmakefile
%ifnarch %{ix86} x86_64
rm -rf test/
%endif

# remove random executable bit
chmod 0644 jni/jffi/jffi.h

# remove uneccessary directories
rm -rf archive/ jni/libffi/ jni/win32/ lib/CopyLibs/ lib/junit*

find ./ -name '*.jar' -exec rm -f '{}' \; 
find ./ -name '*.class' -exec rm -f '{}' \; 

%build
mkdir lib/build_lib
build-jar-repository -s -p lib/build_lib junit junit4

ant

%install
mkdir -p $RPM_BUILD_ROOT%{_libdir}/%{name}
mkdir -p $RPM_BUILD_ROOT%{_jnidir}

cp build/jni/libjffi-1.0.so $RPM_BUILD_ROOT%{_libdir}/%{name}/
cp dist/jffi-complete.jar $RPM_BUILD_ROOT%{_libdir}/%{name}/%{name}-%{version}.jar
ln -s %{name}-%{version}.jar $RPM_BUILD_ROOT%{_libdir}/%{name}/%{name}.jar
ln -s %{_libdir}/%{name}/%{name}-%{version}.jar $RPM_BUILD_ROOT%{_jnidir}/%{name}.jar

mkdir -p $RPM_BUILD_ROOT%{_javadocdir}/%{name}
cp -rp dist/javadoc/* $RPM_BUILD_ROOT%{_javadocdir}/jffi

%check
ant test

%files
%{_libdir}/%{name}/
%{_jnidir}/*

%files javadoc
%{_javadocdir}/jffi

%changelog
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
