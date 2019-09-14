# PKGBUILD

# Maintainer: Daniele Fucini <dfucini@gmail.com>

pkgname=library_manager
pkgver=2.0.1.r0.g8b59188
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
sha256sums=('3ff05cc5501845532aed146fc661b0405836e60a62bc1b91b56d67681bb751a1'
            'bc8e17d581a09b7831bf6ed83843367728a17addabca13c1e2bccfbfde8ea243')

pkgver() 
{  
   git describe --long --tags | sed 's/\([^-]*-g\)/r\1/;s/-/./g'
}

package()
{
   install -Dm755 "${srcdir}/${pkgname}.py" "${pkgdir}/usr/bin/${pkgname}"
}
