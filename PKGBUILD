# PKGBUILD

# Maintainer: Daniele Fucini <dfucini@gmail.com>

pkgname=library_manager
pkgver=2.7.0.r0.g75ca716
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
source=(git+https://github.com/Fuxino/${pkgname}.git)
sha256sums=('SKIP')

pkgver() 
{  
   cd "$pkgname"
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
   install -Dm644 "${srcdir}/${pkgname}/${pkgname}/icons/Icon.png" "${pkgdir}/usr/share/icons/hicolor/32x32/apps/${pkgname}.png"

   python3 setup.py install --root=${pkgdir} --optimize=1 --skip-build
}
