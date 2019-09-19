# PKGBUILD

# Maintainer: Daniele Fucini <dfucini@gmail.com>

pkgname=library_manager
pkgver=2.3.2.r0.g5a881e2
pkgrel=1
pkgdesc="Manage Library database"
arch=("any")
url="https://github.com/Fuxino/library_manager"
license=("GPL3")
makedepends=("git")
depends=("python3"
         "mariadb"
         "python-mysql-connector"
         "python-pyqt5")
source=(git+https://github.com/Fuxino/${pkgname}.git)
sha256sums=('SKIP')

pkgver() 
{  
   cd "$pkgname"
   git describe --long --tags | sed 's/\([^-]*-g\)/r\1/;s/-/./g'
}

package()
{
   install -Dm755 "${srcdir}/${pkgname}/${pkgname}.py" "${pkgdir}/usr/bin/${pkgname}"
   install -Dm644 "${srcdir}/${pkgname}/Icon.png" "${pkgdir}/usr/share/icons/hicolor/32x32/apps/${pkgname}.png"
}
