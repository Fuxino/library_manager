# PKGBUILD

# Maintainer: Daniele Fucini <dfucini@gmail.com>

pkgname=library_manager
pkgver=2.0.2.r5.g2dc1983
pkgrel=1
pkgdesc="Manage Library database"
arch=("any")
license=("GPL3")
depends=("python3"
         "mariadb"
         "python-mysql-connector"
         "python-pyqt5")
makedepends=("git")
source=("${pkgname}.py"
        "Icon.png")
sha256sums=('65da832bfa77f7ca483d3c63e08de70bf2b85cef7354c6d677abbed361df7f14'
            'a75190bd2440b95842b2c9b16024f64b4cf448967d1936b60234371a0a7a5bb6')

pkgver() 
{  
   git describe --long --tags | sed 's/\([^-]*-g\)/r\1/;s/-/./g'
}

package()
{
   install -Dm755 "${srcdir}/${pkgname}.py" "${pkgdir}/usr/bin/${pkgname}"
   install -Dm644 "${srcdir}/Icon.png" "${pkgdir}/usr/share/icons/hicolor/32x32/apps/${pkgname}.png"
}
