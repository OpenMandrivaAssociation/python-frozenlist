# Created by pyp2rpm-3.3.5
%global pypi_name frozenlist

Name:           python-%{pypi_name}
Version:        1.3.1
Release:        1
Summary:        A list-like structure which implements collections
Group:          Development/Python
License:        Apache 2
URL:            https://github.com/aio-libs/frozenlist
Source0:        https://files.pythonhosted.org/packages/source/f/%{pypi_name}/%{pypi_name}-%{version}.tar.gz

BuildRequires:  python3-devel
BuildRequires:  python3dist(setuptools)
BuildRequires:  python3dist(cython)

%global common_description %{expand:
FrozenList is a list-like structure which implements
collections.abc.MutableSequence, and which can be made immutable.}

%description
%{common_description}

%prep
%autosetup -n %{pypi_name}-%{version}
# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info

# Remove Cython-generated sources; we must ensure they are regenerated.
find . -type f -name '*.c' -print -delete

# Re-generate C sources with Cython.
python3 -m cython -3 frozenlist/*.pyx -I frozenlist

%build
%py3_build
# remove the sphinx-build leftovers
rm -rf html/.{doctrees,buildinfo}

%install
%py3_install

%check
%{__python3} setup.py test

%files -n python-%{pypi_name}
%license LICENSE
%doc README.rst
%{python3_sitearch}/%{pypi_name}
%{python3_sitearch}/%{pypi_name}-%{version}-py%{python3_version}.egg-info
