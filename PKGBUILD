# PKGBUILD

# Maintainer: Daniele Fucini <dfucini@gmail.com>

pkgname=library_manager
pkgver=2.0.2.r0.gded7a5f
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
sha256sums=('95f970a6739235d6c8cc06118abe99e028e2288ca6b60ee1bd0e919a6953b608'
            'bc8e17d581a09b7831bf6ed83843367728a17addabca13c1e2bccfbfde8ea243')

pkgver() 
{  
   git describe --long --tags | sed 's/\([^-]*-g\)/r\1/;s/-/./g'
}

package()
{
   install -Dm755 "${srcdir}/${pkgname}.py" "${pkgdir}/usr/bin/${pkgname}"
}
