#
# site.pp - defines all puppet nodes
#

node 'magento.example.com' {
  class { 'common':
  }
  class { 'lamp':
  }
  class { 'magento':
    require => Class['lamp']
  }
}
