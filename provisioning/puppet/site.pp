#
# site.pp - defines all puppet nodes
#

node 'magento.example.com' {
  class { 'common':
  }
  class { 'lamp':
  }
  class { 'mysql::server':
  }
  class { 'magento':
    require => [Class['lamp'], Class['mysql::server']]
  }
}
