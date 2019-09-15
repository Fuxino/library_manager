# PKGBUILD

# Maintainer: Daniele Fucini <dfucini@gmail.com>

pkgname=library_manager
pkgver=2.0.2.r2.g31c39d6
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
        "Icon.ico")
sha256sums=('27bc25751e59548d4c59ebc76a9beae966ba9029a450c860941863f927dedd53'
            'c5f66c0c3b7aa8e2517107aa14734b723341824a75d99687cd2ccf78148829e8')

pkgver() 
{  
   git describe --long --tags | sed 's/\([^-]*-g\)/r\1/;s/-/./g'
}

package()
{
   install -Dm755 "${srcdir}/${pkgname}.py" "${pkgdir}/usr/bin/${pkgname}"
}
