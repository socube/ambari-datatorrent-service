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

"""
from resource_management.libraries.script.script import Script
from resource_management.libraries.resources.hdfs_resource import HdfsResource
from resource_management.libraries.functions import conf_select
from resource_management.libraries.functions import hdp_select
from resource_management.libraries.functions import get_kinit_path
from resource_management.libraries.functions.default import default

# server configurations
config = Script.get_config()

# hadoop default parameters
hadoop_conf_dir = conf_select.get_hadoop_conf_dir()
hadoop_bin_dir = hdp_select.get_hadoop_dir("bin")

DT_BASE_DIR_ARG = config['configurations']['datatorrent-rts-config']['datatorrent.install_dir']
DT_USER_ARG = config['configurations']['datatorrent-rts-config']['datatorrent.username']
DT_GROUP_ARG = config['configurations']['datatorrent-rts-config']['datatorrent.groupname']
DT_GATEWAY_ADDRESS_ARG = config['configurations']['datatorrent-rts-config']['datatorrent.gateway_address']
DT_HADOOP_ARG = config['configurations']['datatorrent-rts-config']['datatorrent.hadoop.path']
DT_ENV_EXPORT_ARG = config['configurations']['datatorrent-rts-config']['datatorrent.env_expression']
DT_SITE_ARG  = config['configurations']['datatorrent-rts-config']['datatorrent.config_file.path']
CUSTOM_ENV_ARG = config['configurations']['datatorrent-rts-config']['datatorrent.environment_file.path']
hdfs_user = config['configurations']['hadoop-env']['hdfs_user']
hdfs_principal_name = config['configurations']['hadoop-env']['hdfs_principal_name']
hdfs_user_keytab = config['configurations']['hadoop-env']['hdfs_user_keytab']
security_enabled = config['configurations']['cluster-env']['security_enabled']
kinit_path_local = get_kinit_path(default('/configurations/kerberos-env/executable_search_paths', None))

hdfs_site = config['configurations']['hdfs-site']
default_fs = config['configurations']['core-site']['fs.defaultFS']

dfs_type = default("/commandParams/dfs_type", "")

import functools
#create partial functions with common arguments for every HdfsResource call
#to create hdfs directory we need to call params.HdfsResource in code
HdfsResource = functools.partial(
  HdfsResource,
  user=hdfs_user,
  security_enabled = security_enabled,
  keytab = hdfs_user_keytab,
  kinit_path_local = kinit_path_local,
  hadoop_bin_dir = hadoop_bin_dir,
  hadoop_conf_dir = hadoop_conf_dir,
  principal_name = hdfs_principal_name,
  hdfs_site = hdfs_site,
  default_fs = default_fs
 )
