"""
Licensed to the Apache Software Foundation (ASF) under one
or more contributor license agreements.  See the NOTICE file
distributed with this work for additional information
regarding copyright ownership.  The ASF licenses this file
to you under the Apache License, Version 2.0 (the
"License"); you may not use this file except in compliance
with the License.  You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

Ambari Agent

"""

import sys
import os
import logging
from resource_management import *
from resource_management.libraries.functions.check_process_status import check_process_status
from resource_management.libraries.resources.hdfs_resource import HdfsResource
from resource_management.core.resources.service import Service

class DtRtsClient(Script):
  def install(self, env):
    import params
    env.set_params(params)
    self.install_datatorrent_repo()
    self.install_packages(env)
    self.add_hdfs_folder(env)
    self.add_user_homeDir(env)

  def configure(self, env, upgrade_type=None):
    import params
    env.set_params(params)
    Execute("export DT_USER_ARG={0} && DT_GROUP_ARG={1} && DT_BASE_DIR_ARG={2} && DT_GATEWAY_ADDRESS_ARG={3}".format(params.DT_USER_ARG, params.DT_GROUP_ARG, params.DT_BASE_DIR_ARG, params.DT_GATEWAY_ADDRESS_ARG))
    Execute("export DT_HADOOP_ARG={0} && DT_ENV_EXPORT_ARG={1} && DT_SITE_ARG={2} && CUSTOM_ENV_ARG={3}".format(params.DT_HADOOP_ARG, params.DT_ENV_EXPORT_ARG, params.DT_SITE_ARG, params.CUSTOM_ENV_ARG))

  def stop(self, env):
    Service('dtgateway', action='stop')

  def start(self, env):
    Service('dtgateway', action='start')

  def status(self, env):
    check_process_status('/var/run/datatorrent/dtgateway.pid')

  def install_datatorrent_repo(self):
    import platform
    distribution = platform.linux_distribution()[0].lower()
    if distribution.lower() in ['centos', 'redhat'] and not os.path.exists('/etc/yum.repos.d/datatorrent.repo'):
      Execute('wget -O /etc/yum.repos.d/datatorrent.repo https://www.datatorrent.com/downloads/repos/yum/repo/datatorrent-rts.repo 2>/dev/null || curl -o /etc/yum.repos.d/datatorrent.repo https://www.datatorrent.com/downloads/repos/yum/repo/datatorrent-rts.repo')
      Execute('wget https://www.datatorrent.com/downloads/repos/apt/keyFile 2>/dev/null || curl -sO https://www.datatorrent.com/downloads/repos/apt/keyFile')
      Execute('rpm --import keyFile')
    elif distribution.lower() in ['ubuntu'] and not os.path.exists('/etc/apt/sources.list.d/datatorrent.list'):
      Execute('echo "deb https://www.datatorrent.com/downloads/repos/apt/ /" > /etc/apt/sources.list.d/datatorrent.list')
      Execute('wget -O - https://www.datatorrent.com/downloads/repos/apt/keyFile | apt-key add - 2>/dev/null || sudo curl -o - https://www.datatorrent.com/downloads/repos/apt/keyFile | apt-key add -')
      Execute('apt-get update')

  def add_hdfs_folder(self, env):
    import params
    env.set_params(params)
    homeDir = '/user/' + params.DT_USER_ARG
    params.HdfsResource(homeDir,
                        type="directory",
                        action="create_on_execute",
                        owner=params.DT_USER_ARG,
                        group=params.DT_GROUP_ARG,
                        mode=0755,
                        recursive_chown=True,
                        recursive_chmod=True
                        )

  def add_user_homeDir(self, env):
    import params
    env.set_params(params)
    homeDir = '/home/' + params.DT_USER_ARG
    mkDir_cmd = format("mkdir -p " + homeDir + " && chown -R " + params.DT_USER_ARG + ":" + params.DT_GROUP_ARG + " " + homeDir)
    Execute(mkDir_cmd)

if __name__ == "__main__":
  DtRtsClient().execute()
