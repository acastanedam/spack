# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

# ----------------------------------------------------------------------------
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
# This is a template package file for Spack.  We've put "FIXME"
# next to all the things you'll want to change. Once you've handled
# them, you can save this file and test your package like this:
#
#     spack install mpcalloc
#
# You can edit this file again by typing:
#
#     spack edit mpcalloc
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack import *


class Mpcalloc(CMakePackage):
    """The MPC memory allocator"""

    homepage = "https://france.paratools.com/"
    url      = "https://france.paratools.com/mpcalloc-0.2.tar.gz"

    # FIXME: Add a list of GitHub accounts to
    # notify when the package is updated.
    # maintainers = ['github_user1', 'github_user2']

    version('0.2', sha256='a4a8f05d53c0c80a90020fd4043bcf807521996416aa22ed61a8e1fcf1bedc62')

    # Add dependencies if required.
    depends_on('cmake')
    depends_on('hwloc@2.2.0')
    depends_on('openpa')

    def cmake_args(self):
        # FIXME: Add arguments other than
        # FIXME: CMAKE_INSTALL_PREFIX and CMAKE_BUILD_TYPE
        # FIXME: If not needed delete this function
        args = []
        return args
