# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
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
#     spack install exatn
#
# You can edit this file again by typing:
#
#     spack edit exatn
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack.package import *


class Exatn(CMakePackage, CudaPackage):
    """FIXME: Put a proper description of your package here."""

    # FIXME: Add a proper url for your package's homepage here.
    # homepage = "https://github.com/ORNL-QCI/"
    git = "https://github.com/ORNL-QCI/exatn.git"
    # url = "https://www.example.com/example-1.2.3.tar.gz"

    # FIXME: Add a list of GitHub accounts to
    # notify when the package is updated.
    maintainers("acastanedam")

    # FIXME: Add the SPDX identifier of the project's license below.
    # See https://spdx.org/licenses/ for a list. Upon manually verifying
    # the license, set checked_by to your Github username.
    license("BSD-3-Clause license", checked_by="acastanedam")

    # FIXME: Add proper versions here.
    version("master", branch="master", submodules=True)

    # FIXME: Add dependencies if required.
    # depends_on("foo")

    variant("test", default=False)
    # variant("mpi", default=False, description="Enable MPI support")
    variant("mpi", default="none", values=("openmpi", "mpich", "none"))
    variant("blas", default="openblas", values=("intel-mkl", "blis", "openblas", "atlas"))

    depends_on("mpi", when="mpi=openmpi")
    depends_on("cuda", when="+cuda")
    depends_on("blas")

    conflicts("%gcc@9.1:", msg="gcc>8.5 is not supported")

    def cmake_args(self):
        args = [self.define_from_variant("EXATN_BUILD_TESTS", "test")]

        # Tell numpy which BLAS/LAPACK libraries we want to use.
        spec = self.spec
        if (
            spec["blas"].name == "intel-mkl"
            or spec["blas"].name == "intel-parallel-studio"
            or spec["blas"].name == "intel-oneapi-mkl"
        ):
            blas = "mkl"
        elif spec["blas"].name == "blis" or spec["blas"].name == "amdblis":
            blas = "blis"
        elif spec["blas"].name == "openblas":
            blas = "openblas"
        elif spec["blas"].name == "atlas":
            blas = "atlas"
        elif spec["blas"].name == "veclibfort":
            blas = "accelerate"
        else:
            blas = "blas"

        args.append(self.define("DBLAS_LIB", blas.upper()))
        args.append("-DBLAS_PATH={0}".format(self.spec["blas"].prefix))

        args = [self.define_from_variant("DMPI_LIB", "mpi")]
        if "+mpi" in self.spec:
            args.append("-DMPI_ROOT_DIR={0}".format(self.spec["mpi"].prefix))

        if "+cuda" in self.spec:
            args.append(self.define("CUTENSOR", True))
            args.append(self.define("CUQUANTUM", True))
            cuda_archs = spec.variants["cuda_arch"].value
            if "none" not in cuda_archs:
                args.append("-DCUDA_NVCC_FLAGS={0}".format(" ".join(self.cuda_flags(cuda_archs))))
            args.append("-DCUTENSOR_PATH={0}".format(self.spec["cuda"].prefix))
            args.append("-DCUQUANTUM_PATH={0}".format(self.spec["cuda"].prefix))
        return args

