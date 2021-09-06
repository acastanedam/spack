# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from os import environ

from spack import *


class Gpi2(AutotoolsPackage):
    """GPI-2 is an API for the development of scalable, asynchronous and fault
    tolerant parallel applications. It implements the GASPI specification"""

    homepage = 'http://www.gpi-site.com'
    url      = 'https://github.com/cc-hpc-itwm/GPI-2/archive/refs/tags/v1.5.0.tar.gz'
    git      = 'https://github.com/cc-hpc-itwm/GPI-2.git'

    maintainers = ['robert-mijakovic', 'arcesio castaneda']

    version('develop', branch='next')
    version('master', branch='master')
    version('1.5.0', sha256='ee299ac1c08c38c9e7871d4af745f1075570ddbb708bb62d82257244585e5183')
    version('1.4.0', sha256='3b8ffb45346b2fe56aaa7ba15a515e62f9dff45a28e6a014248e20094bbe50a1')
    version('1.3.2', sha256='83dbfb2e4bed28ef4e2ae430d30505874b4b50252e2f31dc422b3bc191a87ab0')
    version('1.3.1', sha256='414fa352e7b478442e6f5d0b51ff00deeb4fc705de805676c0e68829f3f30967')
    version('1.3.0', sha256='ffaa5c6abfbf79aec6389ab7caaa2c8a91bce24fd046d9741418ff815cd445d2')
    version('1.3.0-rc1', sha256='bfef056e72c0440b7e33a8fca3cbd6e2e45c9336736a51bb832fbfec2311ea7f')
    version('1.2.0', sha256='0a1411276aa0787382573df5e0f60cc38ca8079f2353fb7a7e8dc57050a7d2cb')
    version('1.1.0', sha256='626727565a8b78be0dc8883539b01aaff2bb3bd42395899643bc4d6cc2313773')
    version('1.0.2', sha256='b03b4ac9f0715279b2a5e064fd85047cb640a85c2361d732930307f8bbf2aeb8')
    version('1.0.1', sha256='b1341bb39e7e70334d7acf831fe7f2061376e7516b44d18b31797748c2a169a3')

    depends_on('autoconf', type='build')  # autogen.sh - autoreconf
    depends_on('automake', type='build')  # autogen.sh - automake
    depends_on('libtool',  type='build')
    depends_on('m4',       type='build')

    variant('fortran', default=False, description='Enable Fortran modules')

    variant(
        'mpi',
        values=disjoint_sets(
            ('openmpi',), ('mpich',), ('mvapich',),
        ).with_non_feature_values('none'),
        description='List of MPIs',
    )

    depends_on('openmpi', when='mpi=openmpi')
    depends_on('mpich', when='mpi=mpich')
    depends_on('mvapich', when='mpi=mvapich')

    variant(
        'fabrics',
        values=disjoint_sets(
            ('auto',), ('infiniband',), ('ethernet',),
        ).with_non_feature_values('auto', 'none'),
        description="List of fabrics that are enabled; "
        "'auto' lets gpi-2 determine",
    )

    depends_on('rdma-core', when='fabrics=infiniband')

    variant(
        'schedulers',
        values=disjoint_sets(
            ('auto',), ('loadleveler',), ('pbs',), ('slurm',)
        ).with_non_feature_values('auto', 'none'),
        description="List of schedulers for which support is enabled; "
        "'auto' lets gpi-2 determine",
    )

    depends_on('slurm', when='schedulers=slurm')

    def set_specific_cflags(self, spec):
        if spec.satisfies('@:1.3.2%gcc@10.1.0:'):
            raise RuntimeError('Gcc version must be less than 10.1')
        elif spec.satisfies('@:1.4.0%gcc@10.1.0:'):
            environ['CFLAGS'] = '-fcommon'

    # GPI-2 without autotools
    @when('@:1.3.2')
    def autoreconf(self, spec, prefix):
        touch = which('touch')
        touch('configure')
        pass

    @when('@:1.3.2')
    def configure(self, spec, prefix):
        pass

    @when('@:1.3.2')
    def build(self, spec, prefix):
        self.old_install(spec, prefix)
        pass

    @when('@:1.3.2')
    def old_install(self, spec, prefix):
        spec = self.spec

        self.set_specific_cflags(spec)

        config_args = ['-p {0}'.format(prefix)]
        if 'fabrics=ethernet' in spec:
            config_args += ['--with-ethernet']
        elif 'fabrics=infiniband' in spec:
            config_args += ['--with-infiniband']
        if 'schedulers=loadleveler' in spec:
            config_args += ['--with-ll']
        elif 'schedulers=slurm' in spec:
            raise RuntimeError('Slurm is not supported')
        if '+fortran' in spec:
            config_args += ['--with-fortran']
        if 'mpi=none' not in spec:
            config_args += ['--with-mpi']

        with working_dir(self.build_directory):
            install = which('./install.sh')
            install(*config_args)

    @when('@:1.3.2')
    def install(self, spec, prefix):
        pass

    # GPI-2 with autotools
    @when('@1.4.0:')
    def autoreconf(self, spec, prefix):
        bash = which('bash')
        bash('./autogen.sh')

    @when('@1.4.0:')
    def configure_args(self):
        spec = self.spec
        config_args = []

        self.set_specific_cflags(spec)

        config_args.extend(self.with_or_without('fortran'))
        # Mpi
        if 'mpi=none' not in spec:
            config_args += ['--with-mpi']
            env['CC'] = spec['mpi'].mpicc
            env['CXX'] = spec['mpi'].mpicxx
            env['F77'] = spec['mpi'].mpif77
            env['FC'] = spec['mpi'].mpifc
        # Fabrics
        if 'fabrics=auto' not in spec:
            config_args.extend(self.with_or_without('fabrics'))
        # Schedulers
        if 'schedulers=auto' not in spec:
            config_args.extend(self.with_or_without('schedulers'))

        return config_args

    def set_machines(self):
        with open('{0}/tests/machines'.format(self.build_directory), 'w') as mfile:
            hostname = environ['HOSTNAME']
            mfile.write('{0}\n{0}\n'.format(hostname))

    # In principle it is possible to run tests for lower versions, but
    # for them NUMA is set by default, thus the number of processes is
    # limited by the number of sockets, i.e., it there is just one,
    # the machine file can not contain more than one host
    @when('@1.4.0:')
    def check(self):
        self.set_machines()
        with working_dir('{0}/tests'.format(self.build_directory)):
            bash = which('bash')
            bash('./runtests.sh')
