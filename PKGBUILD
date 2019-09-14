# PKGBUILD

# Maintainer: Daniele Fucini <dfucini@gmail.com>

pkgname=library_manager
pkgver=1.1.0.r0.g4a0833f
pkgrel=1
pkgdesc="Manage Library database"
arch=("any")
license=("GPL")
depends=("python3"
         "mariadb"
         "python-mysql-connector"
         "python-pyqt5")
makedepends=("git")
source=("$pkgname.py"
        "Books_icon.png")
sha256sums=('61ca8b297fc6a0907c065b5ea33944e365fa3a11954e89be30daaa19a8370b69'
            'bc8e17d581a09b7831bf6ed83843367728a17addabca13c1e2bccfbfde8ea243')

pkgver() 
{  
   git describe --long --tags | sed 's/\([^-]*-g\)/r\1/;s/-/./g'
}

package()
{
   install -Dm755 "${srcdir}/${pkgname}.py" "${pkgdir}/usr/bin/${pkgname}"
}
