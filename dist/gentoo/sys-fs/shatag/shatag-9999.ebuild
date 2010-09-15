# Copyright 1999-2010 Gentoo Foundation
# Distributed under the terms of the GNU General Public License v2
# $Header: $

EAPI=3
PYTHON_DEPEND="3"

inherit distutils mercurial

DESCRIPTION="A file-checksumming and deduplication tool"
HOMEPAGE="http://bitbucket.org/maugier/shatag"
EHG_REPO_URI="http://bitbucket.org/maugier/shatag"

LICENSE="GPL-3"
SLOT="0"
KEYWORDS="~amd64"
IUSE=""

DEPEND="dev-python/pyxattr
	    dev-python/argparse
		dev-python/pyyaml
        dev-lang/python[sqlite]"
RDEPEND="${DEPEND}"

DOCS="README"
S="${WORKDIR}/shatag"

pkg_setup() {
	python_set_active_version 3
}

src_install() {
	distutils_src_install
	doman man/*.?
}
