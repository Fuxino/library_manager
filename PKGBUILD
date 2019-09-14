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
sha256sums=('cb793e03a767b9db81d0b53f19f0157bbce97e5e3aa6be2d15f83e2a06e6242d'
            'bc8e17d581a09b7831bf6ed83843367728a17addabca13c1e2bccfbfde8ea243')

pkgver() 
{  
   git describe --long --tags | sed 's/\([^-]*-g\)/r\1/;s/-/./g'
}

package()
{
   install -Dm755 "${srcdir}/${pkgname}.py" "${pkgdir}/usr/bin/${pkgname}"
}
