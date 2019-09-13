# PKGBUILD

# Maintainer: Daniele Fucini <dfucini@gmail.com>

pkgname=query_library
pkgver=1.5.1.r0.gf4c40ef
pkgrel=1
pkgdesc="Query Library database"
arch=("any")
license=("GPL")
depends=("python3"
         "mariadb"
         "python-mysql-connector"
         "python-pyqt5")
makedepends=("git")
source=("$pkgname.py"
        "Books_icon.png")
sha256sums=('f6c89056e9c14a5f0b74173c647085ce4edefa419235846081091c2a44d5f8e5'
            'bc8e17d581a09b7831bf6ed83843367728a17addabca13c1e2bccfbfde8ea243')

pkgver() 
{  
   git describe --long --tags | sed 's/\([^-]*-g\)/r\1/;s/-/./g'
}

package()
{
   install -Dm755 "${srcdir}/${pkgname}.py" "${pkgdir}/usr/bin/${pkgname}"
}
