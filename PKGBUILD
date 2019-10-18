# PKGBUILD

# Maintainer: Daniele Fucini <dfucini@gmail.com>

pkgname=library_manager
pkgver=2.7.6.r1.g49c7e66
pkgrel=1
pkgdesc="Manage Library database"
arch=("any")
url="https://github.com/Fuxino/library_manager"
license=("GPL3")
makedepends=("python-setuptools"
             "git")
depends=("python3"
         "mariadb"
         "python-mysql-connector"
         "python-pyqt5")
optdepends=('python-isbnlib: check if isbn inserted is valid')
conflicts=('library_manager-dev')
source=(git+https://github.com/Fuxino/${pkgname}.git)
sha256sums=('SKIP')

pkgver() 
{  
   cd ${pkgname}
   git describe --long --tags | sed 's/\([^-]*-g\)/r\1/;s/-/./g'
}

build()
{
   cd ${srcdir}/${pkgname}
   python3 setup.py build
}

package()
{
   cd ${srcdir}/${pkgname}
   python3 setup.py install --root=${pkgdir} --optimize=1 --skip-build
}
