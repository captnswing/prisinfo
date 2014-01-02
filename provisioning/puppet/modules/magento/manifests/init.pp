class magento {

  package { "php5-curl":
    ensure => latest
  }

#  database { 'magento db':
#    require => Class['mysql::server'],
#    name => "magento",
#    ensure => present,
#  }
#
#  exec { "create magento db":
#    command => ""
#  #  mysql_db: name=magento state=present login_user=root login_password=mp109
#  }

  file { "magento tar":
    path    => "/tmp/magento-1.8.1.0.tar.gz",
    ensure  => file,
    mode    => "0644",
    source  => "/vagrant/provisioning/puppet/modules/magento/files/magento-1.8.1.0.tar.gz",
    owner   => "root",
    group   => "root"
  }

  exec { "extract magento archive":
    command => "/bin/tar xzf /tmp/magento-1.8.1.0.tar.gz",
    creates => "/opt/magento/LICENSE.html",
    cwd     => "/opt",
    require => File["magento tar"],
  }

  file { "/opt/magento/app/etc":
    ensure  => directory,
    owner   => "www-data",
    group   => "www-data",
    mode    => 0644,
    recurse => true,
    require => Exec["extract magento archive"],
  }

  file { "/opt/magento/media":
    ensure  => directory,
    owner   => "www-data",
    group   => "www-data",
    mode    => 0644,
    recurse => true,
    require => Exec["extract magento archive"],
  }

  file { "/opt/magento/var":
    ensure  => directory,
    owner   => "www-data",
    group   => "www-data",
    mode    => 0644,
    recurse => true,
    require => Exec["extract magento archive"],
  }

  file { "/var/www/magento":
    ensure  => link,
    owner   => "root",
    group   => "root",
    target  => "/opt/magento"
  }

}
