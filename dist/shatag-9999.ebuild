# Copyright 1999-2010 Gentoo Foundation
# Distributed under the terms of the GNU General Public License v2
# $Header: $

EAPI=3

inherit distutils mercurial

DESCRIPTION="A file-checksumming and deduplication tool"
HOMEPAGE="http://bitbucket.org/maugier/shatag"
EHG_REPO_URI="http://bitbucket.org/maugier/shatag"

LICENSE="GPL-3"
SLOT="0"
KEYWORDS="~amd64"
IUSE=""

DEPEND=""
RDEPEND="${DEPEND}"

DOCS="README"

src_install() {
	distutils_src_install
	doman man/*.?

}
