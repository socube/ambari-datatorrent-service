## Deploying Datatorrent RTS in an Ambari stack
Apache Ambari ensures easier management for Apache Hadoop clusters. You can now deploy DataTorrent RTS within the Ambari stack. Such a deployment ensures simplified management of the DataTorrent RTS setup. 
**Note**: DataTorrent RTS, powered by Apache Apex, provides a high-performing, fault-tolerant, scalable, easy-to-use data processing platform for batch and streaming workloads. It includes advanced management, monitoring, development, visualization, data ingestion, and distribution features. 
For more details, see [https://www.datatorrent.com/product/datatorrent-rts/] 

### Setting up Ambari service
Use these instructions to set up Ambari for installation, setup and management of DataTorrent RTS.

**Note**: Ensure that your installation of Apache Ambari corresponds to version 2.2.0.0 or later. Also note that service installion is tested under HDP stack only.

1. Connect to the server where Ambari is installed (Supported Ambari version: 2.2.0.0)
2. Download the Ambari service for DataTorrent RTS, by running the following commands:

    ```
    VERSION=`hdp-select status hadoop-client | sed 's/hadoop-client - \([0-9]\.[0-9]\).*/\1/'`
    sudo git clone https://github.com/DataTorrent/ambari-datatorrent-service.git /var/lib/ambari-server/resources/stacks/HDP/$VERSION/services/DATATORRENT
    ```
3. Run the following commands to restart the Ambari service:
    ```
    #sandbox
    service ambari restart

    #non sandbox
    sudo service ambari-server restart
    ```
4. In the bottom-left of the Ambari dashboard, click **Add Services** from the Actions list.
5. Select DataTorrent RTS, and click **Next**.
6. Modify the appropriate configuration properties, and click **Next**.
   ![Image](screenshots/service-installed-config.png?raw=true)
7. Click **Deploy**.

Upon successful deployment, the DataTorrent RTS service appears as a part of the Ambari stack. To start or stop this service, go to:
![Image](screenshots/service-installed.png?raw=true)


### Why deploy DataTorrent RTS as a part of Ambari
The biggest benefit of wrapping DataTorrent RTS within the Ambari service is that you can now monitor and manage this service remotely via REST APIs.
Use the following commands for monitoring and management:

	export SERVICE=Datatorrent-RTS
	export PASSWORD=admin
	export AMBARI_HOST=localhost

	#detect name of cluster
	output=`curl -u admin:$PASSWORD -i -H 'X-Requested-By: ambari'  http://$AMBARI_HOST:8080/api/v1/clusters`
	CLUSTER=`echo $output | sed -n 's/.*"cluster_name" : "\([^\"]*\)".*/\1/p'`

	#get service status
	curl -u admin:$PASSWORD -i -H 'X-Requested-By: ambari' -X GET http://$AMBARI_HOST:8080/api/v1/clusters/$CLUSTER/services/$SERVICE

	#start service
	curl -u admin:$PASSWORD -i -H 'X-Requested-By: ambari' -X PUT -d '{"RequestInfo": {"context" :"Start $SERVICE via REST"}, "Body": {"ServiceInfo": {"state": "STARTED"}}}' http://$AMBARI_HOST:8080/api/v1/clusters/$CLUSTER/services/$SERVICE

	#stop service
	curl -u admin:$PASSWORD -i -H 'X-Requested-By: ambari' -X PUT -d '{"RequestInfo": {"context" :"Stop $SERVICE via REST"}, "Body": {"ServiceInfo": {"state": "INSTALLED"}}}' http://$AMBARI_HOST:8080/api/v1/clusters/$CLUSTER/services/$SERVICE

Another benefit is that installation of custom services is simpler using Ambari blueprints. See this example to see how you can deploy custom services using Ambari blueprints: https://github.com/abajwa-hw/ambari-workshops/blob/master/blueprints-demo-security.md

### Using Datatorrent RTS
After you deploy DataTorrent RTS, use the following URL to open the DataTorrent RTS console login page:
http://*hostname*:9090
For example, http://sandbox.hortonworks.com:9090
**Note**: If you are using Oracle VM VirtualBox, you must manually forward port 9090 before logging on.

#### Configuring DataTorrent RTS
Follow these steps to configure DataTorrent RTS:

1. Use the installation wizard to complete the configuration. ![Image](screenshots/service-install-wizard.png?raw=true)

2. Import application packages from dtHub. ![Image](screenshots/application-import.png?raw=true)

3. Launch an application on the Datatorrent RTS platform. ![Image](screenshots/application-launch.png?raw=true)

4. Monitor the launched application from the Monitor tab. ![Image](screenshots/application-monitor.png?raw=true)
