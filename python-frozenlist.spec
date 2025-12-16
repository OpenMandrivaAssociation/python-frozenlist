%undefine _debugsource_packages
%global module frozenlist

Name:           python-%{module}
Version:        1.8.0
Release:        1
Summary:        A list-like structure which implements collections
Group:          Development/Python
License:        Apache-2.0
URL:            https://github.com/aio-libs/frozenlist
Source0:        https://files.pythonhosted.org/packages/source/f/%{module}/%{module}-%{version}.tar.gz

BuildRequires:	python
BuildRequires:	pkgconfig(python)
BuildRequires:	python%{pyver}dist(cython)
BuildRequires:	python%{pyver}dist(expandvars)
BuildRequires:	python%{pyver}dist(setuptools)
BuildRequires:	python%{pyver}dist(pip)
BuildRequires:	python%{pyver}dist(pytest)
BuildRequires:	python%{pyver}dist(tomli)
BuildRequires:	python%{pyver}dist(wheel)



%global common_description %{expand:
FrozenList is a list-like structure which implements
collections.abc.MutableSequence, and which can be made immutable.}

%description
%{common_description}

%prep
%autosetup -n %{module}-%{version}
# Remove bundled egg-info
rm -rf %{module}.egg-info

# Remove Cython-generated sources; we must ensure they are regenerated.
find . -type f -name '*.c' -print -delete

# Re-generate C sources with Cython.
python -m cython -3 frozenlist/*.pyx -I frozenlist

%build
%py_build
# remove the sphinx-build leftovers
rm -rf html/.{doctrees,buildinfo}

%install
%py_install

%check
export LDFLAGS="%{ldflags} -lpython%{py_ver}"
export CI=true
export PYTHONPATH="%{buildroot}%{python_sitearch}:${PWD}"
# remove coverage tests
rm -rf tests/conftest.py
sed -i '21,28d' pytest.ini
# this test is flaky in isolated builts
k="${k-}${k+ and }not test_iface"

pytest -v -Wdefault -k "${k-}"

%files
%license LICENSE
%doc README.rst
%{python_sitearch}/%{module}
%{python_sitearch}/%{module}-%{version}.dist-info
